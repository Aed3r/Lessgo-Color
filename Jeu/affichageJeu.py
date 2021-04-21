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

def chrono(fenetre):
    global tDebut
    if (tDebut == None):
       tDebut = time.time()
    else :
        tActuelle=time.time()
        t0=tActuelle-tDebut
        police=pygame.font.SysFont(None,80)
        text = police.render (str(int(t0)),1,(0,0,0))
        fenetre.blit(text, (pygame.display.Info().current_w/2, 50))
        pygame.display.flip()                                                

def drawAll(fenetre):
    # Mesure du temps d'affichage de la frame
    start = time.time() * 1000

    # Affichage du terrain
    terrain.afficheTerrain(fenetre)

    # Affiche les proportions des zones coloriées
    terrain.afficheProp(fenetre)
    
    # Affichage des joueurs
    afficherJoueurs(fenetre)

    # Fin de la mesure du temps et attente pour afficher la prochaine frame
    end = time.time() * 1000
    sleep = (msPerFrame - (end - start))/1000.
    if (sleep > 0): 
        time.sleep(sleep)

    chrono(fenetre)