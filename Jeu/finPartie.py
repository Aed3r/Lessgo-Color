from constantes import *
from plateau import *
import pygame as pg
import os

def finPartie(fenetre):
    i = 0
    pg.draw.rect(fenetre, (255, 255, 255), pg.Rect(0, 0, getRes()[0], getRes()[1]))
    listeP = getTerrain().pourcentageCouleur()

    policeViolet=pygame.font.SysFont(None,30)
    violet = policeViolet.render(str(int(listeP[0]*100))+"%",True,(0,0,0))


    policeJaune=pygame.font.SysFont(None,30)
    jaune = policeJaune.render(str(int(listeP[1]*100))+"%",True,(0,0,0))


    policeRouge=pygame.font.SysFont(None,30)
    rouge = policeRouge.render(str(int(listeP[2]*100))+"%",True,(0,0,0))


    policeBleu=pygame.font.SysFont(None,30)
    bleu = policeBleu.render(str(int(listeP[3]*100))+"%",True,(0,0,0))

    listePolice = [violet,jaune,rouge,bleu]

    for i in range(4):
        pygame.draw.rect(fenetre, couleursPlateau[i], pygame.Rect(getRes()[0]*0.2*(i+1), (getRes()[1]*0.8)-(getRes()[1]*listeP[i]/2), 30, getRes()[1]*listeP[i]/2))
        fenetre.blit(listePolice[i],pygame.Rect(getRes()[0]*0.2*(i+1),getRes()[1]*0.8,30,-(getRes()[1]*listeP[i]/2)))