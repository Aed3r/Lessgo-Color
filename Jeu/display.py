***REMOVED***
import threading
import time
from joueur import *
from plateau import *
from constantes import *

                                                                                                                     
***REMOVED***                                                                                                         #initialise les module pygame
pygame.display.set_caption("SPLAT_PGMOT")                                                                             #nom fenetre
info = pygame.display.Info()                                                                                          #recupere l'information de la machine en cours
#resolution = (info.current_w, info.current_h)                                                                          #resolution de l'ecrant a partir de info
#fenetre = pygame.display.set_mode(resolution,pygame.FULLSCREEN)                                                       #FULLSCREEN
fenetre = pygame.display.set_mode(resolution, pygame.RESIZABLE)
msPerFrame = int(1000 / fps)

#------------------------------------------------------------FONCTION--------------------------------------------------------------------------------------#

def afficherJoueurs():
    joueurs.sort(key=comparJoueur) # Trie les joueurs suivant leurs ordonnées 
    for joueur in joueurs:
        joueur.move()
        pygame.draw.circle(fenetre, joueur.COLOR, [joueur.x, joueur.y], playerSize)

#def fond():                                                                                                              #Fonction initialise fond du terrain
#    fenetre.fill((210,210,210))                                                                                           #couleur fond
#    pygame.draw.rect(fenetre,(100,0,0),pygame.Rect(0,0,200,200))                                                          #haut gauche rouge
#    pygame.draw.rect(fenetre,(0,100,0),pygame.Rect(resolution[0]-200,0,200,200))                                         #haut droit vert
#    pygame.draw.rect(fenetre,(0,0,100),pygame.Rect(0,resolution[1]-200,200,200))                                         #bas gauche bleu
#    pygame.draw.rect(fenetre,(100,100,0),pygame.Rect(resolution[0]-200,resolution[1]-200,200,200))                      #bas droit jaune

def joueur(x,y):                                                                                                         #Fonction dessine un joueur en X,Y
    pygame.draw.circle(fenetre,(0,0,0),[x, y], 5)                                                                         #joueur représenté par un cercle



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
