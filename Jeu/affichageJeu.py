import pygame
import threading
import time
import joueur
from plateau import *
from constantes import *

tDebut = None

# Temps de calcul alloué pour une image
msPerFrame = int(1000 / fps)

def afficherJoueurs(fenetre):
    for j in joueur.getJoueurs():
        pygame.draw.circle(fenetre, j.getCouleur(), j.getPos(), playerSize)   

# Renvoie True si la partie est finie, False sinon
def chrono(fenetre):
    global tDebut
    
    if (tDebut == None):
       tDebut = time.time() + tempsPartie
    else :
        tActuelle=time.time()
        t0=tDebut - tActuelle
        t0 = int(t0)
        minute= str(t0//60)
        seconde = str(t0%60)
        if (t0 == 0):
            print("Partie FINI")
            return True
        text = policeTitres.render (minute + ":" + seconde,1,(0,0,0))
        fenetre.blit(text, (resolution[0]/2 - text.get_width()/2, 50))    
        return False                                          

def drawAll(fenetre):
    # Mesure du temps d'affichage de la frame
    start = time.time() * 1000

    # Affichage du terrain
    terrain.afficheTerrain(fenetre)

    # Affiche les proportions des zones coloriées
    terrain.afficheProp(fenetre)
    
    # Affichage des joueurs
    afficherJoueurs(fenetre)

    # Affichage du chrono
    gameDone = chrono(fenetre)

    # Fin de la mesure du temps et attente pour afficher la prochaine frame
    end = time.time() * 1000
    sleep = (msPerFrame - (end - start))/1000.
    if (sleep > 0): 
        time.sleep(sleep)

    return gameDone