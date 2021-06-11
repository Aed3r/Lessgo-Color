from constantes import *
from plateau import *
import pygame as pg
import os
import math

def afficherScore(fenetre, j, pos, x, y):
    score = j.getScore()
    nom = j.getNom()
    margeH = getRes()[0]*0.2

    if pos == 1:
        top = policeBold.render("#" + str(pos) + " " + nom, True, titleColor)
    else:
        top = policeMedium.render("#" + str(pos) + " " + nom, True, titleColor)
    bottom = policeThin.render(str(score) + " cases", True, titleColor)

    tailleTexte = top.get_size()
    if (tailleTexte[0] > margeH):
        top = pg.transform.smoothscale(top, (int(margeH-5), int((tailleTexte[1] / tailleTexte[0]) * (margeH-5))))

    totH = top.get_height() + bottom.get_height()
    
    fenetre.blit(top, (x-top.get_width()/2, y-totH))
    fenetre.blit(bottom, (x-bottom.get_width()/2, y-totH+top.get_height()))

    return totH + 10

def finPartie(fenetre, joueurs):
    i = 0
    pg.draw.rect(fenetre, (255, 255, 255), pg.Rect(0, 0, getRes()[0], getRes()[1]))
    listeP = getTerrain().pourcentageCouleur()
    margeH = getRes()[0]*0.2

    listeTextes = [policeMedium.render(str(int(listeP[0]*100))+"%",True,titleColor),
                   policeMedium.render(str(int(listeP[1]*100))+"%",True,titleColor),
                   policeMedium.render(str(int(listeP[2]*100))+"%",True,titleColor),
                   policeMedium.render(str(int(listeP[3]*100))+"%",True,titleColor)]

    for i in range(4):
        pg.draw.rect(fenetre, couleursPlateau[i], pygame.Rect(margeH*(i+1)-largeurBarres/2, (getRes()[1]*0.8)-(getRes()[1]*listeP[i]/2), largeurBarres, getRes()[1]*listeP[i]/2))
        fenetre.blit(listeTextes[i], (margeH*(i+1)-listeTextes[i].get_width()/2, getRes()[1]*0.8+10))

    # Top joueurs
    listeEquipes = []
    for i in range(4):
        listeEquipes.append(sorted(list(filter(lambda j: j.getEquipe() == i, joueurs)), key=lambda j:j.getScore()))
    
    for i in range(4):
        offset = (getRes()[1]*0.8)-(getRes()[1]*listeP[i]/2)-10
        for j in range(min(3, len(listeEquipes[i]))-1, -1, -1):
            offset -= afficherScore(fenetre, listeEquipes[i][j], j+1, margeH*(i+1), offset)
