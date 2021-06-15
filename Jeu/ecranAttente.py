import pygame as pg
import threading
import time
import joueur as j
from constantes import *
from UI.bouton import *
import os
import math

# Temps de calcul alloué pour une image
msPerFrame = int(1000 / fps)

# Taille des blocs de couleurs
blockW = None
blockH = None
ico = None
icoOG = None
pixelMargins = {}

# Animations
startT = time.time() * 1000
blocsBuffer = []

# Doit être appelé avant les autres fonction pour initialiser les variables nécessitant la globale getRes()
def initValeurs():
    global blockH, blockW, ico, icoOG, pixelMargins
    
    # MAJ des marges en fonction de la taille d'écran
    pixelMargins['left'] = margins['left'] / 100 * getRes()[0]
    pixelMargins['right'] = margins['right'] / 100 * getRes()[0]
    pixelMargins['top'] = margins['top'] / 100 * getRes()[1]
    pixelMargins['bottom'] = margins['bottom'] / 100 * getRes()[1]

    # Taille des blocs de couleurs
    blockW = (getRes()[0] - (pixelMargins['left'] * 5)) / 4
    blockH = getRes()[1] - pixelMargins['top'] - pixelMargins['bottom']

    # buffers des blocs de couleurs
    for i in range(4):
        blocsBuffer.append(pygame.Surface((blockW, blockH)))

    # Icône
    # https://www.flaticon.com/free-icon/user_1077114?term=user&page=1&position=1&page=1&position=1&related_id=1077114&origin=search
    if (icoOG == None):
        icoOG = pygame.image.load(os.path.join('Data', 'Images', 'user.png')).convert_alpha() # Récupération

    ico = pygame.transform.smoothscale(icoOG, (int(getRes()[1]*tailleCompteur), int(getRes()[1]*tailleCompteur))) # Redimensionnement

def clear (fenetre):
    pg.draw.rect(fenetre, (255, 255, 255), pg.Rect(0, 0, getRes()[0], getRes()[1]))

def afficherBlocsCouleurs():
    global blocsBuffer

    for i in range(4):
        pg.draw.rect(blocsBuffer[i], couleursPlateau[i], pg.Rect(0, 0, blockW, blockH))

def afficherNomsJoueurs():
    global blocsBuffer
    offsetListes = [0, 0, 0, 0]

    for joueur in j.joueurs:
        e = joueur.getEquipe() # Indice d'équipe du joueur

        # Préparation de la couleur de texte (inverse du bloc)
        couleurBloc = couleursPlateau[e]
        couleurPolice = (255-couleurBloc[0], 255-couleurBloc[1], 255-couleurBloc[2])

        # Préparation de la surface du texte avec redimensionnement si besoin
        text = policeMedium.render(joueur.getNom(), True, couleurPolice)
        tailleTexte = text.get_size()
        if (tailleTexte[0] > blockW):
            text = pg.transform.smoothscale(text, (int(blockW-10), int((tailleTexte[1] / tailleTexte[0]) * (blockW-10))))
        
        # Préparation de l'emplacement du texte
        tailleTexte = text.get_size()
        posX = blockW/2 - tailleTexte[0]/2
        posY = 0

        # Affichage du texte
        if (offsetListes[e] + tailleTexte[1] < blockH):
            blocsBuffer[e].blit(text, (posX, posY + offsetListes[e]))
        else:
            # On bouge la liste de noms vers le haut
            extra = offsetListes[e] + tailleTexte[1] - blockH # Ce qui dépasse du bloc
            tempSurface = pg.Surface((blockW, blockH-extra))
            tempSurface.blit(blocsBuffer[e], (0, 0), pg.Rect(posBloc, posY+extra, blockW, blockH-extra))
            blocsBuffer[e].blit(tempSurface, (posBloc, posY))
            offsetListes[e] -= extra
            # On enlève le fond
            pg.draw.rect(blocsBuffer[e], couleursPlateau[e], pg.Rect(posBloc, posY+offsetListes[e], blockW, extra))
            # Texte
            blocsBuffer[e].blit(text, (posX, posY + blockH - tailleTexte[1]))

        offsetListes[e] += tailleTexte[1]

def afficherTitre (fenetre):
    global titleColor
    textSurface = policeBold.render(ENATTENTE, True, titleColor);
    tailleTexte = textSurface.get_size()
    fenetre.blit(textSurface, (getRes()[0]/2-tailleTexte[0]/2, pixelMargins['top']/2-tailleTexte[1]/2))

ico = None

def afficherCompteJoueurs (fenetre):
    global titleColor

    # Icône
    tailleIco = ico.get_size()
    fenetre.blit(ico, (getRes()[0]-tailleIco[0]-margeCompteur, margeCompteur))

    # Compteur
    textSurface = policeBold.render(str(j.getNombreJoueurs()), True, titleColor);
    tailleTexte = textSurface.get_size()
    newHeight = getRes()[1]*tailleCompteur
    textSurface = pygame.transform.smoothscale(textSurface, 
                    (int((tailleTexte[0]/tailleTexte[1])*newHeight), int(newHeight)))
    fenetre.blit(textSurface, (getRes()[0]-tailleIco[0]-tailleTexte[0]-margeCompteur, margeCompteur))

# Renvoi une valeur incrémentée selon la progression d'une courbe sinus au moment t
def sineWave (duree, destination, t):
    if t <= 0:
        return 0
    elif t >= duree:
        return destination
    else:
        return math.sin(t * ((2 * math.pi) / (duree*4))) * destination

def animate (fenetre):
    global startT, blocsBuffer

    execT = (time.time() * 1000 - startT) % (dureeListes + dureeQR)

    if execT < dureeListes:
        if execT < dureeListes - animationDuration - 3*delaiBlocs:
            posBlocs = [pixelMargins['top']+blockH+pixelMargins['bottom']-sineWave(animationDuration, blockH+pixelMargins['bottom'], execT-delaiBlocs*0),
                        pixelMargins['top']+blockH+pixelMargins['bottom']-sineWave(animationDuration, blockH+pixelMargins['bottom'], execT-delaiBlocs*1),
                        pixelMargins['top']+blockH+pixelMargins['bottom']-sineWave(animationDuration, blockH+pixelMargins['bottom'], execT-delaiBlocs*2),
                        pixelMargins['top']+blockH+pixelMargins['bottom']-sineWave(animationDuration, blockH+pixelMargins['bottom'], execT-delaiBlocs*3)]
        else:
            posBlocs = [pixelMargins['top']+sineWave(animationDuration, blockH+pixelMargins['bottom'], execT-(dureeListes-animationDuration-delaiBlocs*0)),
                        pixelMargins['top']+sineWave(animationDuration, blockH+pixelMargins['bottom'], execT-(dureeListes-animationDuration-delaiBlocs*1)),
                        pixelMargins['top']+sineWave(animationDuration, blockH+pixelMargins['bottom'], execT-(dureeListes-animationDuration-delaiBlocs*2)),
                        pixelMargins['top']+sineWave(animationDuration, blockH+pixelMargins['bottom'], execT-(dureeListes-animationDuration-delaiBlocs*3))]

        for i in range(4):
            fenetre.blit(blocsBuffer[i], (pixelMargins['left'] + i * (blockW+pixelMargins['left']), posBlocs[i]))


def toutDessiner(fenetre):
    global showMenu, rectBouton

    # Mesure du temps d'affichage de la frame
    start = time.time() * 1000

    initValeurs()

    clear(fenetre)
    afficherBlocsCouleurs()
    afficherNomsJoueurs()
    animate(fenetre)
    afficherTitre(fenetre)
    afficherCompteJoueurs(fenetre)

    # Fin de la mesure du temps et attente pour afficher la prochaine frame
    end = time.time() * 1000
    sleep = (msPerFrame - (end - start))/1000.
    if (sleep > 0): 
        time.sleep(sleep)