import cv2
import numpy as np
from reportlab.pdfgen import canvas
import os

#Liste qu'on utilise dans l'exemple

liste1=[['Charlie Chaplin','30 %'],['Scarlett Johansson','25 %'],['Morgan Freeman','40 %']]

#Pour changer la taille d'une image (dim est de la forme dim=(largeur,hauteur))

def resize_image(photo,dim):
    image=cv2.imread(photo,1)
    img=cv2.resize(image,dim)
    cv2.imwrite(str('resized_')+str(photo), img)

#Nom du fichier, ne pas oublier de mettre .pdf

pdf = canvas.Canvas("Résultat.pdf")

#Titre du pdf dans l'application

pdf.setTitle("Statistiques sur la diversité")

#Affichage d'une chaîne de mots

pdf.drawCentredString(250,770,"titre")

#Création d'un cartouche pour un acteur (exemple : cartouche(400, "Morgan Freeman",'Morgan_Freeman.jpg'), pdf)

def cartouche(Y,nom,photo,statistiques,pdf):
    pdf.line(0,Y,600,Y)
    pdf.line(0,Y+100,600,Y+100)
    pdf.setFont("Courier-Bold",18)
    pdf.drawInlineImage(photo,20,Y+10)
    pdf.drawString(120,Y+10,nom)
    pdf.drawString(330,Y+10, "temps d'écran :")
    pdf.drawString(517,Y+10,statistiques)

#Sauvegarde définitive du pdf qu'on a paramétré

pdf.save()

#Fonction transformant liste de [nom de célébrité, temps d'écran] en  pdf, en ayant dans le même dossier des photos de taille 80x80 leur correspondant, femaleest le pourcentage de femmes à l'écran et ethnic le pourcentage de minorités ethniques à l'écran

def resultat(liste,female,ethnic):
    if os.path.exists("Résultat.pdf"):
        os.remove("Résultat.pdf")
    pdf1 = canvas.Canvas("Résultat.pdf")
    pdf1.setFont("Helvetica-Bold",30)
    pdf1.drawCentredString(300,800,"Respect de la diversité")
    n=1
    for i in liste:
        s=i[0].split()
        photo=resize_image(i[1],80)
        cartouche(780-n*100,i[0],photo,i[2],pdf1)
        n+=1
    pdf1.setFont("Courier-Bold",13)
    pdf1.drawString(20,730-(n-1)*100,"Pourcentage de femmes à l'écran :")
    pdf1.drawString(150,710-(n-1)*100,str(female)+str(' %'))
    pdf1.drawString(305,730-(n-1)*100,"Pourcentage de minorités à l'écran :")
    pdf1.drawString(450,710-(n-1)*100,str(ethnic)+str(' %'))
    pdf1.line(300,780-n*100,300,780-(n-1)*100)
    pdf1.line(0,780-n*100,600,780-n*100)
    pdf1.save()



#Test cartouche

def cartouche1(Y,nom,photo,statistiques):
    if os.path.exists("Résultat.pdf"):
        os.remove("Résultat.pdf")
    pdf = canvas.Canvas("Résultat.pdf")
    pdf.line(0,Y,600,Y)
    pdf.line(0,Y+100,600,Y+100)
    pdf.setFont("Courier-Bold",20)
    pdf.drawInlineImage(photo,20,Y+10)
    pdf.drawString(120,Y+10,nom)
    pdf.drawString(330,Y+10, "temps d'écran :")
    pdf.drawString(517,Y+10,statistiques)
    pdf.save()

nom="Morgan Freeman"
s=nom.split()
name=str('resized_')+str(s[0])+str('_')+str(s[1])+str('.jpg')

def exemple(name):
    print(str("a ")+str(name))
