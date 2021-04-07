import pygame
import threading
import time
import joueur as j
from constantes import *

# Temps de calcul alloué pour une image
msPerFrame = int(1000 / fps)

# Taille des blocs de couleurs
blockW = None
blockH = None

blur = pygame.image.load("Data/Images/blur.png")

def initValeurs():
    global blockH, blockW
    
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

def afficherNomsJoueurs(fenetre):
    offsetListes = [0, 0, 0, 0]
    for joueur in j.joueurs:
        text = police.render(joueur.getNom(), True, couleurPolice)
        e = joueur.getEquipe() # Indice d'équipe du joueur
        tailleTexte = text.get_size()
        posX = margins['left'] + e * (blockW+margins['left']) + blockW/2 - tailleTexte[0]/2
        posY = margins['top'] + offsetListes[e]

        # On ajuste le flou à la taille du texte
        nBlur = pygame.Surface(((int) (tailleTexte[0]*1.5), tailleTexte[1])).convert_alpha()
        pygame.transform.smoothscale(blur, ((int) (tailleTexte[0]*1.5), tailleTexte[1]), nBlur)

        # On affiche le flou derrière le texte
        fenetre.blit(nBlur, ((int) (posX-tailleTexte[0]*0.25), posY))
        fenetre.blit(text, (posX, posY))
        offsetListes[e] += tailleTexte[1]

def toutDessiner(fenetre):
    # Mesure du temps d'affichage de la frame
    start = time.time() * 1000

    clear(fenetre)
    afficherBlocsCouleurs(fenetre)
    afficherNomsJoueurs(fenetre)

    # Raffraichissment de la fenêtre
    pygame.display.flip()

    # Fin de la mesure du temps et attente pour afficher la prochaine frame
    end = time.time() * 1000
    sleep = (msPerFrame - (end - start))/1000.
    if (sleep > 0): 
        time.sleep(sleep)