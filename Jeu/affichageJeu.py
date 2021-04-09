***REMOVED***
import threading
import time
import joueur
from plateau import *
from constantes import *

# Temps de calcul alloué pour une image
msPerFrame = int(1000 / fps)

def afficherJoueurs(fenetre):
    for j in joueur.getJoueurs():
        pygame.draw.circle(fenetre, j.getCouleur(), j.getPos(), playerSize)                                                                  

def drawAll(fenetre):
    # Mesure du temps d'affichage de la frame
    start = time.time() * 1000

    # Affichage du terrain
    terrain.afficheTerrain(fenetre)

    # Affichage des joueurs
    afficherJoueurs(fenetre)

    # Fin de la mesure du temps et attente pour afficher la prochaine frame
    end = time.time() * 1000
    sleep = (msPerFrame - (end - start))/1000.
    if (sleep > 0): 
        time.sleep(sleep)