import pygame
import threading
import time
from joueur import *
from constantes import *

# Temps de calcul alloué pour une image
msPerFrame = int(1000 / fps)

def afficherBlocsCouleurs():
    


def drawAll():
    # Mesure du temps d'affichage de la frame
    start = time.time() * 1000

    # Affichage du terrain
    terrain.afficheTerrain(fenetre)

    # Affichage des joueurs
    afficherJoueurs()

    # Raffraichissment de la fenêtre
    pygame.display.flip()

    # Fin de la mesure du temps et attente pour afficher la prochaine frame
    end = time.time() * 1000
    sleep = (msPerFrame - (end - start))/1000.
    if (sleep > 0): 
        time.sleep(sleep)