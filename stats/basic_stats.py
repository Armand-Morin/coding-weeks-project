from filters.gender import female
from filters.skin_color import ethnic

#Fonction renvoie le temps passé à l'ecran en seconde

def screentime(frame_nb):
    return frame_nb/24

#Fonction qui renvoie la part du film occupée par un acteur

def screenshare(character_time, runtime): # runtime_min : durée du film en minutes
    res = 100*character_time/runtime
    return round(res, 1)

#Fonction qui renvoie le temps passé à l'écran par les femmes dans un role principal

def female_screenshare(characters, runtime): #characters liste de listes de la forme [nom, photo de référence, nb de frames présent]
    female_characters = [character for character in characters if female(character[1])] # female(img) fonction à coder qui renvoit vrai si personnage est une femme, et faux sinon
    res = 0
    for character in female_characters:
        res += screenshare(character[2], runtime)
    return res

#Fonction qui renvoie le temps passé à l'écran par les minorités ethniques dans un role principal

def ethnic_screenshare(characters, runtime):
    ethnic_characters = [character for character in characters if ethnic(character[1])] # ethnic(img) fonction à coder qui renvoit faux si personnage est blanc, et vrai sinon
    res = 0
    for character in ethnic_characters:
        res += screenshare(character[2], runtime)
    return res