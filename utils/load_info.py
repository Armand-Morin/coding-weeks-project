import requests
import bs4
import time
import selenium
from selenium import webdriver
import requests
from PIL import Image
import io
import hashlib
import os
import sys



if sys.platform=='win32':
    DRIVER_PATH = './chromedriverwin'
else:
    DRIVER_PATH='./chromedrivermac' #Dans Driver path il faut insérer le chemin d'accès à télecharger au lien suivant https://sites.google.com/a/chromium.org/chromedriver/home 
#(et si vous ne l'avez pas téléchargez aussi Google Chrome j'imagine)
wd = webdriver.Chrome(executable_path=DRIVER_PATH)
wd.get('https://google.com') 
search_box = wd.find_element_by_css_selector('input.gLFyf') #input box selector
search_box.send_keys('Any query')


# Fonction qui permet de charger l'url de la page wikipedia associée au film


def load_film_page(name):
    response=requests.get("https://fr.wikipedia.org/wiki/"+name)
    return response



# Fonction qui scrappe la page wikipedia afin d'obtenir les noms des acteurs principaux


def get_casting(name):
    res=[]

    #le try permet de distinguer le cas ou la page du film est ditincte du nom exact du film (par ex pour gravity il faut rajouter _(film) a la fin car ce n'est pas la seule page wikipedia portant ce titre)
    try:

        page=load_film_page(name)
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        tr_box=soup.find_all("tr")
        i=0
        acteurs=""
        while i<10 and i<len(tr_box):
            s = tr_box[i]
            th_box=s.find_all("th" ,{"scope":"row","style":"width:8em;"})
            if "Acteurs principaux" in bs4.BeautifulSoup(th_box[0].text, 'html.parser'):
                acteurs=s
            i+=1
        a_box=acteurs.find_all("a")

    #on passe au cas ou on doit rajouter le _(film)

    except:
        page=load_film_page(name+'_(film)')
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        tr_box=soup.find_all("tr")
        i=0
        acteurs=""
        while i<7 and i<len(tr_box):
            s = tr_box[i]
            th_box=s.find_all("th" ,{"scope":"row","style":"width:8em;"})
            if "Acteurs principaux" in bs4.BeautifulSoup(th_box[0].text, 'html.parser'):
                acteurs=s
            i+=1
        a_box=acteurs.find_all("a")
    for i in a_box:
        res.append(i['title'])
    return(res) #retourne une liste contenant les noms des acteurs


            
#Fonction qui a partir d'une requete, du nombre d'images souhaitées d'une connexion à un navigateur permet de renvoyer les urls des images souhaitées
#sleep between interactions coreespond à un paramètre qui permet de ne pas surcharger le navigateur de requetes



def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)    
    
    # Construit la requete google afin d'obtenir les images

    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # Charge la page

    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # On parcourt les liens renvoyant vers les images 
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)
        
        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        
        for img in thumbnail_results[results_start:number_results]:

            # on tente d'accéder à l'image à travers le lien, si on y arrive pas on passe à la suivante

            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # on extrait à l'url de l'img  

            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(30)
            return
            load_more_button = wd.find_element_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # on redescend dans la page de résulats afin de ne pas télécharger le mm lien plusieurs fois

        results_start = len(thumbnail_results)

    return image_urls



# Fonction qui permet de télécharger une image à partir de son url



def persist_image(folder_path:str,file_name:str,url:str,sleep_time=1):

    #tentative de chargement de l'image

    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")
    

    #création du répertoire cible pour enregistrer l'image et enregistrement de l'image dans ce répertoire (en lui ajoutant un identifiant quasi unique)
    try:

        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        folder_path = os.path.join(folder_path,file_name)
        if os.path.exists(folder_path):
            file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        else:
            os.mkdir(folder_path)
            file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
        return file_path
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


#Fonction qui regroupe les fonctions précédentes afin de répondre au nom d'un film par l'enregistrement d'une photo par acteur principal (qui lui servira par la suite de photo d'identité)
# et renvoie un liste de liste de trois élemnts. Cette liste de trois élements contient pour chaque acteur, son nom le chemin d'accès à sa photo et un nombre initialisé à zero qui servira par la suite


def create_character_list(film_name,sleep_time=1):
    actors=get_casting(film_name)
    res=[]
    for a in actors:
        urls=fetch_image_urls(a+' face',1,wd)
        for url in urls:
            f=persist_image("./dataset",a,url,sleep_time)
            res.append([a,f,0])
    return res

if __name__=="__main__":
    # create_character_list("Les_Huit_Salopards")
    pass