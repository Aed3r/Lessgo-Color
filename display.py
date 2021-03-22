import pygame
import threading
import time
from joueur import *
from plateau import *
from constantes import *

                                                                                                                     
pygame.init()                                                                                                         #initialise les module pygame
pygame.display.set_caption("SPLAT_PGMOT")                                                                             #nom fenetre
info = pygame.display.Info()                                                                                          #recupere l'information de la machine en cours
#resolution = (info.current_w,info.current_h)                                                                          #resolution de l'ecrant a partir de info
#fenetre = pygame.display.set_mode(resolution,pygame.FULLSCREEN)                                                       #FULLSCREEN
fenetre = pygame.display.set_mode(resolution, pygame.RESIZABLE)                                                                                                           #Boolean boucle principale
tailleCase = 20
terrain = Terrain(200,400)

#------------------------------------------------------------FONCTION--------------------------------------------------------------------------------------#

def afficherJoueurs():
    joueurs.sort(key=comparJoueur) # Trie les joueurs suivant leurs ordonnées 
    for joueur in joueurs:
        joueur.move()
        pygame.draw.circle(fenetre, joueur.COLOR, [joueur.x, joueur.y], 5)

def fond():                                                                                                              #Fonction initialise fond du terrain
    fenetre.fill((210,210,210))                                                                                           #couleur fond
    pygame.draw.rect(fenetre,(100,0,0),pygame.Rect(0,0,200,200))                                                          #haut gauche rouge
    pygame.draw.rect(fenetre,(0,100,0),pygame.Rect(resolution[0]-200,0,200,200))                                         #haut droit vert
    pygame.draw.rect(fenetre,(0,0,100),pygame.Rect(0,resolution[1]-200,200,200))                                         #bas gauche bleu
    pygame.draw.rect(fenetre,(100,100,0),pygame.Rect(resolution[0]-200,resolution[1]-200,200,200))                      #bas droit jaune

def joueur(x,y):                                                                                                         #Fonction dessine un joueur en X,Y
    pygame.draw.circle(fenetre,(0,0,0),[x, y], 5)                                                                         #joueur representer par un cercle

def afficheTerrain(terrain):
    for i in range(terrain.larg):
            for j in range (terrain.long):
                    if(terrain.getColor(i,j) == 1):
                          pygame.draw.rect(fenetre,(255,255,255),pygame.Rect(i*tailleCase,j*tailleCase,tailleCase,tailleCase))    
                    elif(terrain.getColor(i,j) == 2):
                          pygame.draw.rect(fenetre,(100,000,0),pygame.Rect(i*tailleCase,j*tailleCase,tailleCase,tailleCase))

def initTerrain(terrain):
     for i in range(terrain.larg):
            for j in range (terrain.long):
                if((i+j)%2 == 0):
                    terrain.setColor(i,j,1)
                else :
                    terrain.setColor(i,j,2)


class affichage(threading.Thread):  
    def __init__(self):  
        threading.Thread.__init__(self)
        initTerrain(terrain)

#------------------------------------------------------------BOUCLE PRINCIPALE-----------------------------------------------------------------------------#

    def run(self):  
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            # Affichage du plateau et des joueurs, s'arrête avec le serveur
            #afficheTerrain(terrain)
            fond()
            afficherJoueurs()
            pygame.display.flip()                                                                                               #actualise
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------#
        
