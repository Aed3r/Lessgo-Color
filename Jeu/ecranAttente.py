import pygame as pg
import threading
import time
import joueur as j
from constantes import *
from UI.bouton import *

# Temps de calcul alloué pour une image
msPerFrame = int(1000 / fps)

# Taille des blocs de couleurs
blockW = None
blockH = None

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
    pg.draw.rect(fenetre, (255, 255, 255), pg.Rect(0, 0, resolution[0], resolution[1]))

def afficherBlocsCouleurs(fenetre):
    for i in range(4):
        pg.draw.rect(fenetre, couleursPlateau[i], pg.Rect(margins['left'] + i * (blockW+margins['left']), 
                                                                  margins['top'], 
                                                                  blockW, 
                                                                  blockH))

def afficherNomsJoueurs(fenetre):
    offsetListes = [0, 0, 0, 0]
    for joueur in j.joueurs:
        e = joueur.getEquipe() # Indice d'équipe du joueur

        # Préparation de la couleur de texte (inverse du bloc)
        couleurBloc = couleursPlateau[e]
        couleurPolice = (255-couleurBloc[0], 255-couleurBloc[1], 255-couleurBloc[2])

        # Préparation de la surface du texte avec redimensionnement si besoin
        text = policeNoms.render(joueur.getNom(), True, couleurPolice)
        tailleTexte = text.get_size()
        if (tailleTexte[0] > blockW):
            text = pg.transform.smoothscale(text, (int(blockW-10), int((tailleTexte[1] / tailleTexte[0]) * (blockW-10))))
        
        # Préparation de l'emplacement du texte
        tailleTexte = text.get_size()
        posBloc = margins['left'] + e * (blockW+margins['left'])
        posX = posBloc + blockW/2 - tailleTexte[0]/2
        posY = margins['top']

        # Affichage du texte
        if (offsetListes[e] + tailleTexte[1] < blockH):
            fenetre.blit(text, (posX, posY + offsetListes[e]))
        else:
            # On bouge la liste de noms vers le haut
            extra = offsetListes[e] + tailleTexte[1] - blockH # Ce qui dépasse du bloc
            tempSurface = pg.Surface((blockW, blockH-extra))
            tempSurface.blit(fenetre, (0, 0), pg.Rect(posBloc, posY+extra, blockW, blockH-extra))
            fenetre.blit(tempSurface, (posBloc, posY))
            offsetListes[e] -= extra
            # On enlève le fond
            pg.draw.rect(fenetre, couleursPlateau[e], pg.Rect(posBloc, posY+offsetListes[e], blockW, extra))
            # Texte
            fenetre.blit(text, (posX, posY + blockH - tailleTexte[1]))

        offsetListes[e] += tailleTexte[1]

def afficherTitre (fenetre):
    textSurface = policeTitres.render("En attente de joueurs...", True, (49, 51, 53));
    tailleTexte = textSurface.get_size()
    fenetre.blit(textSurface, (resolution[0]/2-tailleTexte[0]/2, margins['top']/2-tailleTexte[1]/2))


showMenu = False

def setMenu():
    global showMenu
    showMenu = not showMenu



def toutDessiner(fenetre):
    global showMenu, rectBouton

    # Mesure du temps d'affichage de la frame
    start = time.time() * 1000

    clear(fenetre)
    afficherBlocsCouleurs(fenetre)
    afficherNomsJoueurs(fenetre)
    afficherTitre(fenetre)

    if (showMenu):
        afficherMenu(fenetre)
    else:
        rectBouton = None

    # Fin de la mesure du temps et attente pour afficher la prochaine frame
    end = time.time() * 1000
    sleep = (msPerFrame - (end - start))/1000.
    if (sleep > 0): 
        time.sleep(sleep)