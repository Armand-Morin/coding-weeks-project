from tensorflow import keras
from keras_vggface.vggface import VGGFace
from keras_vggface import utils
from keras.preprocessing import image
import os
import cv2
import numpy as np
import progressbar as pb


def crop(img,x,y,w,h):
    return img[y:y+h,x:x+w]

#Fonction qui détecte un ou plusieurs visages dans une photo 

def recognition1(img):
    face_cascade = cv2.CascadeClassifier('./face_detect/haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 1)
    if faces != []:
        res = [0]*len(faces)
        for k in range(0,len(faces)):
            (x,y,w,h) = faces[k]
            res[k] = crop(img,x,y,w,h)
        return res
    else:
        return(['no face detected'])


#Fonction qui détecte levisage principal dans une photo (afin d'éviter les bugs et qu'on se retrouve avec une photo de main en guise d'identification d'un personnage principal)


def recognition_character(img):
    face_cascade = cv2.CascadeClassifier('./face_detect/haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 1)
    try :
        (x,y,w,h)=faces[0]
    except:
        print("No face detected")
    res=crop(img,x,y,w,h)
    return res


def load_model():
    model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
    return model

#fonction qui prend en argument un nom de dossier et renvoie ses fichiers ou dossiers internes sous forme d'une liste

def get_filenames(file):
    dossiers=os.listdir('./'+file)
    res=[]
    for d in dossiers:
        res+=['./'+file+'/'+d]
    return res

#Fonction qui à l'aide du modèle entrainé renvoie l'embedding correspondant aux images rentrées)
#On y rajoute un module qui permet de suivre de facon plus ou moins précise l'avancée dans l'exécution du programme
#Retourne la liste des embeddings de chaque fichiers

def get_embeddings(filenames):
    widgets = ['          Neural model progression: ', pb.Percentage(), ' ', 
            pb.Bar(marker=pb.RotatingMarker()), ' ', pb.ETA()]
    timer = pb.ProgressBar(widgets=widgets, maxval=9).start()
    face=[cv2.imread(f) for f in filenames]
    timer.update(1)
    print(" ")
    print("Recognizing faces...")

    #reconnaissance des visages

    face=[recognition1(image) for image in face]
    timer.update(2)

    #Remise en forme de la liste afin d'appliquer predict

    face=[img for list_img in face for img in list_img] # flatten list
    timer.update(3)
    face=[cv2.resize(img,(224,224)) for img in face]
    timer.update(4)
    samples=[np.asarray(f,dtype=np.float32) for f in face]
    timer.update(5)
    samples=[np.expand_dims(x, axis=0) for x in samples]
    timer.update(6)
    samples=[utils.preprocess_input(x, version=2) for x in samples]
    timer.update(7)
    model=load_model()
    timer.update(8)
    print(" ")
    "Predicting..."
    res=[model.predict(s) for s in samples]
    timer.update(9)
    timer.finish()
    return res

#Fonction qui renvoie la distance euclidienne entre deux vecteurs

def distance(a,b):
    res=0
    for i in range(len(a)):
        res+=(a[i]-b[i])**2
    res=res**(0.5)
    return res

#Fonction qui renvoie les embeddings pour l'identification des personnages principaux (embeddings de reference donc en utilisant recognition_character)

def get_charac_embed(characters):
    filenames = [character[1] for character in characters]
    face=[cv2.imread(f) for f in filenames]
    face=[recognition_character(image) for image in face]
    face=[cv2.resize(img,(224,224)) for img in face]
    samples=[np.asarray(f,dtype=np.float32) for f in face]
    samples=[np.expand_dims(x, axis=0) for x in samples]
    samples=[utils.preprocess_input(x, version=2) for x in samples]
    model=load_model()
    res=[model.predict(s) for s in samples]
    return res

#Fonction qui a partir des visages tirés d'une frame trouve le visage parmi ceux des personnages principaux qui lui ressemble le plus alors le nombre de frame 
# dans lequel apparait le peronnage correspondant est incrémenté


def frame_charac_count(characters, film_embed, charac_embed):
    n=len(film_embed)
    l = len(charac_embed)

    #Parcours des frames

    for i in range(n):
        m=90 #Définition du seuil à partir duquel on considère que deux visages sont suffisament proches pour qu'on les identifie 
        ppv=-1

        #Parours classique dans la recherche d'un minimum 

        for j in range(l):
            if m>distance(film_embed[i][0],charac_embed[j][0]) and i!=j:
                m=distance(film_embed[i][0],charac_embed[j][0])
                ppv=j
        if ppv != -1:
            characters[ppv][2]+=1

