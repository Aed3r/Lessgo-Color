import constantes as cst
import plateau
import pygame as pg
import os
import math
import UI.animation as anim
import time

# Animations
blocsBuffer = pg.Surface((1000, 1000), pg.SRCALPHA)

def afficherScores(fenetre, j, pos, x, y, alpha):
    score = j.getScore()
    nom = j.getNom()
    margeH = cst.getRes()[0]*0.2

    if pos == 1:
        top = cst.policeBold.render("#" + str(pos) + " " + nom, True, cst.titleColor)
    else:
        top = cst.policeMedium.render("#" + str(pos) + " " + nom, True, cst.titleColor)
    bottom = cst.policeThin.render(str(score) + " cases", True, cst.titleColor)

    tailleTexte = top.get_size()
    if (tailleTexte[0] > margeH):
        top = pg.transform.smoothscale(top, (int(margeH-5), int((tailleTexte[1] / tailleTexte[0]) * (margeH-5))))

    totH = top.get_height() + bottom.get_height()

    top.set_alpha(alpha)
    bottom.set_alpha(alpha)
    
    fenetre.blit(top, (x-top.get_width()/2, y-totH))
    fenetre.blit(bottom, (x-bottom.get_width()/2, y-totH+top.get_height()))

    return totH + 10

def initFin():
    global startT
    startT = time.time() * 1000

def finPartie(fenetre, joueurs):
    global startT
    i = 0
    pg.draw.rect(fenetre, cst.couleurFond, pg.Rect(0, 0, cst.getRes()[0], cst.getRes()[1]))
    listeP = plateau.getTerrain().pourcentageCouleur()
    margeH = cst.getRes()[0]*0.2

    execT = time.time() * 1000 - startT

    listeTextes = [cst.policeMedium.render(str(int(listeP[0]*100))+"%",True,cst.titleColor),
                   cst.policeMedium.render(str(int(listeP[1]*100))+"%",True,cst.titleColor),
                   cst.policeMedium.render(str(int(listeP[2]*100))+"%",True,cst.titleColor),
                   cst.policeMedium.render(str(int(listeP[3]*100))+"%",True,cst.titleColor)]

    sortedP = sorted(listeP, reverse=True)
    order = [None] * 4
    step = 0
    done = []
    for i in range(4):
        if sortedP[i] in done:
            continue
        for j in range(4):
            if sortedP[i] == listeP[j]:
                order[j] = step
                done.append(sortedP[i])
        step += 1

    alpha = [anim.sineWave(cst.animFinDuree, 255, execT-cst.delaiFinBlocs*((step-1)-order[0])),
             anim.sineWave(cst.animFinDuree, 255, execT-cst.delaiFinBlocs*((step-1)-order[1])),
             anim.sineWave(cst.animFinDuree, 255, execT-cst.delaiFinBlocs*((step-1)-order[2])),
             anim.sineWave(cst.animFinDuree, 255, execT-cst.delaiFinBlocs*((step-1)-order[3]))]

    for i in range(4):
        listeTextes[i].set_alpha(alpha[i])
        blocsBuffer.fill((0,0,0,0))
        pg.draw.rect(blocsBuffer, cst.couleursPlateau[i]+(alpha[i], ), pg.Rect(0, 0, cst.largeurBarres, cst.getRes()[1]*listeP[i]/2))
        blocsBuffer.set_alpha(alpha[i])
        fenetre.blit(blocsBuffer, (margeH*(i+1)-cst.largeurBarres/2, (cst.getRes()[1]*0.8)-(cst.getRes()[1]*listeP[i]/2)))
        fenetre.blit(listeTextes[i], (margeH*(i+1)-listeTextes[i].get_width()/2, cst.getRes()[1]*0.8+10))

    # Top joueurs
    listeEquipes = []
    for i in range(4):
        # On récupère les joueurs de chaque équipe et on les trie selon leurs scores
        listeEquipes.append(sorted(list(filter(lambda j: j.getEquipe() == i, joueurs)), key=lambda j:j.getScore(), reverse=True))
    
    for i in range(4):
        offset = (cst.getRes()[1]*0.8)-(cst.getRes()[1]*listeP[i]/2)-10
        for j in range(min(3, len(listeEquipes[i]))-1, -1, -1):
            offset -= afficherScores(fenetre, listeEquipes[i][j], j+1, margeH*(i+1), offset, alpha[i])
