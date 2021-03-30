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
fenetre = pygame.display.set_mode(resolution, pygame.RESIZABLE)                                                                                                           #Boolean boucle principale
terrain = Terrain(200,400)

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



class affichage(threading.Thread):  
    def __init__(self):  
        threading.Thread.__init__(self)

#------------------------------------------------------------BOUCLE PRINCIPALE-----------------------------------------------------------------------------#

    def run(self):  
        t = threading.currentThread()
        terr=Terrain(round(resolution[1]/tailleCase),round(resolution[0]/tailleCase))
        terr.initTerrain()
        while getattr(t, "do_run", True):
            start = time.time() * 1000
            # Affichage du plateau et des joueurs, s'arrête avec le serveur
            #afficheTerrain(terrain)
            #fond()
            terr.afficheTerrain(fenetre)
            afficherJoueurs()
            pygame.display.flip()                                                                                      #actualise  
            end = time.time() * 1000
            sleep = (msPerFrame - (end - start))/1000.
            if (sleep > 0): 
                time.sleep(sleep)
                for joueur in joueurs :
                    terr.setColor(joueur.x/resolution[1]*terr.larg,joueur.y/resolution[0]*terr.long,joueur.EQUIPE)
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------#
        
