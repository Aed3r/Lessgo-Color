from constantes import *
import pygame as pg
import pygame
import os

def finPartie(fenetre,terrain):
    pg.draw.rect(fenetre, (255, 255, 255), pg.Rect(0, 0, resolution[0], resolution[1]))
    listeP = terrain.pourcentageCouleur()

    policeBleu=pygame.font.SysFont(None,80)
    bleu = policeBleu.render(str(int(listeP[0]*100)+"%"),True,(0,0,0))
    fenetre.blit(bleu, (pygame.display.Info().current_w/2, 100))

    policeRouge=pygame.font.SysFont(None,80)
    rouge = policeRouge.render(str(int(listeP[1]*100)+"%"),True,(0,0,0))
    fenetre.blit(rouge, (pygame.display.Info().current_w/2, 200))
    
    policeJaune=pygame.font.SysFont(None,80)
    jaune = policeJaune.render(str(int(listeP[2]*100)+"%"),True,(0,0,0))
    fenetre.blit(jaune, (pygame.display.Info().current_w/2, 300))

    policeVert=pygame.font.SysFont(None,80)
    vert = policeVert.render(str(int(listeP[3]*100)+"%"),True,(0,0,0))
    fenetre.blit(jaune, (pygame.display.Info().current_w/2, 400))

    pygame.display.flip()                                  
             