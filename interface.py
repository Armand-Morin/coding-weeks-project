import programmes.screentime as ethn
import programmes.film_genre as emot

def launch(name):
    if radValues.get()==1:
        characters = ethn.get_screentime(name, name+str('.mov'))
        ethn.final(characters)
    if radValues.get()==2:
        var = emot.get_emotions(name+str('.mov'))
        print(var)
    

from tkinter import *
from tkinter import ttk

fenetre = Tk()
fenetre.geometry("350x250")

#création d'un champ de texte
champ_label1 = Label(fenetre, text="Veuillez saisir le nom du film", font=("", 16))
champ_label1.pack()

champ_label2 = Label(fenetre, text="mettre une majuscule à chaque mot", font=("", 16))
champ_label2.pack()

champ_label3 = Label(fenetre, text="et un _ pour les espaces", font=("", 16))
champ_label3.pack()

#création d'une zone à remplir avec du texte
nom = StringVar()
ligne_texte = Entry(fenetre, textvariable=nom, width=30)
ligne_texte.pack(pady=5)

#création de boutons exclusifs (radiobutton)
radValues = IntVar()
champ_label3 = Label(fenetre, text="Veillez choisir quelles informations obtenir: ", font=("", 10))
champ_label3.pack()
r1=ttk.Radiobutton(fenetre, text="Statistiques sur la diversité (temps à l'écran, diversité, parité)", variable=radValues, value=1)
r2=ttk.Radiobutton(fenetre, text="Émotions dans le film", variable=radValues, value=2)

r1.pack()
r2.pack()

#création d'un bouton entrée
bouton= ttk.Button(fenetre, text="Entrer", width=15, command=lambda:launch(nom.get()))
bouton.pack(pady=15)


fenetre.mainloop()
