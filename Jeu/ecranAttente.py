import pygame
import threading
import time
from joueur import *
from constantes import *

# Temps de calcul alloué pour une image
msPerFrame = int(1000 / fps)

# MAJ des marges en fonction de la taille d'écran
margins['left'] = margins['left'] / 100 * resolution[0]
margins['right'] = margins['right'] / 100 * resolution[0]
margins['top'] = margins['top'] / 100 * resolution[1]
margins['bottom'] = margins['bottom'] / 100 * resolution[1]

# Taille des blocs de couleurs
blockW = (resolution[0] - (margins['left'] * 5)) / 4
blockH = resolution[1] - margins['top'] - margins['bottom']

def clear (fenetre):
    pygame.draw.rect(fenetre, (255, 255, 255), pygame.Rect(0, 0, resolution[0], resolution[1]))

def afficherBlocsCouleurs(fenetre):
    for i in range(4):
        pygame.draw.rect(fenetre, couleursPlateau[i], pygame.Rect(margins['left'] + i * (blockW+margins['left']), 
                                                                  margins['top'], 
                                                                  blockW, 
                                                                  blockH))

def toutDessiner(fenetre):
    # Mesure du temps d'affichage de la frame
    start = time.time() * 1000

    clear(fenetre)
    afficherBlocsCouleurs(fenetre)

    # Raffraichissment de la fenêtre
    pygame.display.flip()

    # Fin de la mesure du temps et attente pour afficher la prochaine frame
    end = time.time() * 1000
    sleep = (msPerFrame - (end - start))/1000.
    if (sleep > 0): 
        time.sleep(sleep)