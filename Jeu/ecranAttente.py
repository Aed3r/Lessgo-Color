import pygame as pg
import threading
import time
import joueur as j
import constantes as cst
import os
import math
import UI.animation as anim

# Temps de calcul alloué pour une image
msPerFrame = int(1000 / cst.fps)

# Taille des blocs de couleurs
blockW = None
blockH = None
ico = None
icoOG = None
pixelMargins = {}

# Animations
startT = time.time() * 1000
blocsBuffer = []
qrImgOG = pg.image.load(os.path.join('Data', 'Images', 'serverlink.png'))
qrImg = None

# Doit être appelé avant les autres fonction pour initialiser les variables nécessitant la globale getRes()
def initValeurs():
    global blockW, blockH, ico, icoOG, pixelMargins, blocsBuffer
    
    # MAJ des marges en fonction de la taille d'écran
    pixelMargins['left'] = cst.margins['left'] / 100 * cst.getRes()[0]
    pixelMargins['right'] = cst.margins['right'] / 100 * cst.getRes()[0]
    pixelMargins['top'] = cst.margins['top'] / 100 * cst.getRes()[1]
    pixelMargins['bottom'] = cst.margins['bottom'] / 100 * cst.getRes()[1]

    # Taille des blocs de couleurs
    newBlockW = (cst.getRes()[0] - (pixelMargins['left'] * 5)) / 4
    newBlockH = cst.getRes()[1] - pixelMargins['top'] - pixelMargins['bottom']

    if len(blocsBuffer) > 0 and (newBlockW != blockW or newBlockH != blockH):
        for i in range(5):
            blocsBuffer[i] = pg.Surface((newBlockW, newBlockH), pg.SRCALPHA)

        # Code QR
        scaleQR()
        
    blockW = newBlockW
    blockH = newBlockH

    # Icône
    # https://www.flaticon.com/free-icon/user_1077114?term=user&page=1&position=1&page=1&position=1&related_id=1077114&origin=search
    if (icoOG == None):
        icoOG = pg.image.load(os.path.join('Data', 'Images', 'user.png')).convert_alpha() # Récupération

        # buffers des blocs de couleurs
        for i in range(5):
            blocsBuffer.append(pg.Surface((blockW, blockH), pg.SRCALPHA))
        
        # Code QR
        scaleQR()

    ico = pg.transform.smoothscale(icoOG, (int(cst.getRes()[1]*cst.tailleCompteur), int(cst.getRes()[1]*cst.tailleCompteur))) # Redimensionnement

def scaleQR():
    global qrImg, qrImgOG
    tQR = (int) (min(cst.getRes()[0]-pixelMargins["left"]-pixelMargins["right"], cst.getRes()[1]-pixelMargins["top"]-pixelMargins["bottom"]))
    qrImg = pg.transform.smoothscale(qrImgOG, (tQR, tQR))

def clear (fenetre):
    pg.draw.rect(fenetre, cst.couleurFond, pg.Rect(0, 0, cst.getRes()[0], cst.getRes()[1]))

def afficherBlocsCouleurs():
    global blocsBuffer

    for i in range(4):
        # Fond
        blocsBuffer[i].set_colorkey(cst.couleurFond)
        # Rectangle 1 (sert à adoucir les bords)
        pg.draw.rect(blocsBuffer[i], cst.couleursPlateau[i] + (50,), pg.Rect(0, 0, blockW, blockH), 0, 7)
        # Rectangle 2
        pg.draw.rect(blocsBuffer[i], cst.couleursPlateau[i], pg.Rect(0, 0, blockW, blockH), 0, 10)

def afficherNomsJoueurs():
    global blocsBuffer
    offsetListes = [0, 0, 0, 0]

    for joueur in j.joueurs:
        if not joueur.getStillPlaying():
            continue

        if not cst.afficherBotsStats and joueur.isBot():
            continue
        
        e = joueur.getEquipe() # Indice d'équipe du joueur

        # Préparation de la couleur de texte (inverse du bloc)
        couleurBloc = cst.couleursPlateau[e]
        couleurPolice = (255-couleurBloc[0], 255-couleurBloc[1], 255-couleurBloc[2])

        # Préparation de la surface du texte avec redimensionnement si besoin
        text = cst.policeMedium.render(joueur.getNom(), True, couleurPolice)
        tailleTexte = text.get_size()
        if (tailleTexte[0] > blockW):
            text = pg.transform.smoothscale(text, (int(blockW-10), int((tailleTexte[1] / tailleTexte[0]) * (blockW-10))))
        
        # Préparation de l'emplacement du texte
        tailleTexte = text.get_size()
        posX = blockW/2 - tailleTexte[0]/2

        # On vérifie que la liste ne dépasse pas
        if (offsetListes[e] + tailleTexte[1] > blockH):
            # On bouge la liste de noms vers le haut
            extra = offsetListes[e] + tailleTexte[1] - blockH # Ce qui dépasse du bloc
            blocsBuffer[e].blit(blocsBuffer[e], (5, 0), pg.Rect(5, extra, blockW-10, blockH-extra))
            offsetListes[e] -= extra
            # On enlève le fond
            pg.draw.rect(blocsBuffer[e], cst.couleursPlateau[e], pg.Rect(5, offsetListes[e]-10, blockW, extra))

        # Affichage du texte
        blocsBuffer[e].blit(text, (posX, offsetListes[e]))

        offsetListes[e] += tailleTexte[1]

def afficherTitre (fenetre):
    textSurface = cst.policeBold.render(cst.ENATTENTE, True, cst.titleColor)
    tailleTexte = textSurface.get_size()
    fenetre.blit(textSurface, (cst.getRes()[0]/2-tailleTexte[0]/2, pixelMargins['top']/2-tailleTexte[1]/2))

ico = None

def afficherCompteJoueurs (fenetre):
    # Icône
    tailleIco = ico.get_size()
    fenetre.blit(ico, (cst.getRes()[0]-tailleIco[0]-cst.margeCompteur, cst.margeCompteur))

    # Compteur
    textSurface = cst.policeBold.render(str(j.getNombreJoueurs()), True, cst.titleColor)
    tailleTexte = textSurface.get_size()
    newHeight = cst.getRes()[1]*cst.tailleCompteur
    textSurface = pg.transform.smoothscale(textSurface, 
                    (int((tailleTexte[0]/tailleTexte[1])*newHeight), int(newHeight)))
    fenetre.blit(textSurface, (cst.getRes()[0]-tailleIco[0]-tailleTexte[0]-cst.margeCompteur, cst.margeCompteur))

def animate (fenetre):
    global startT, blocsBuffer, qrImg

    execT = (time.time() * 1000 - startT) % (cst.dureeListes + cst.dureeQR)

    if execT < cst.dureeQR: # Code QR
        if execT < cst.dureeQR - cst.animAttenteDuree: # Fade in
            qrImg.set_alpha(anim.sineWave(cst.animAttenteDuree, 255, execT))
        else: # Fade out
            qrImg.set_alpha(255-anim.sineWave(cst.animAttenteDuree, 255, execT-(cst.dureeQR-cst.animAttenteDuree)))
        
        fenetre.blit(qrImg, (cst.getRes()[0] / 2 - qrImg.get_width()/2, pixelMargins['top']))
    else: # Blocs de couleurs avec listes
        if execT < cst.dureeQR + cst.dureeListes - cst.animAttenteDuree - 3*cst.delaiAttenteBlocs: # Slide in progressif de chaque bloc avec délai
            posBlocs = [pixelMargins['top']+blockH+pixelMargins['bottom']-anim.sineWave(cst.animAttenteDuree, blockH+pixelMargins['bottom'], execT-cst.dureeQR-cst.delaiAttenteBlocs*0),
                        pixelMargins['top']+blockH+pixelMargins['bottom']-anim.sineWave(cst.animAttenteDuree, blockH+pixelMargins['bottom'], execT-cst.dureeQR-cst.delaiAttenteBlocs*1),
                        pixelMargins['top']+blockH+pixelMargins['bottom']-anim.sineWave(cst.animAttenteDuree, blockH+pixelMargins['bottom'], execT-cst.dureeQR-cst.delaiAttenteBlocs*2),
                        pixelMargins['top']+blockH+pixelMargins['bottom']-anim.sineWave(cst.animAttenteDuree, blockH+pixelMargins['bottom'], execT-cst.dureeQR-cst.delaiAttenteBlocs*3)]
        else: # Slide out progressif
            posBlocs = [pixelMargins['top']+anim.sineWave(cst.animAttenteDuree, blockH+pixelMargins['bottom'], execT-(cst.dureeQR+cst.dureeListes-cst.animAttenteDuree-cst.delaiAttenteBlocs*0)),
                        pixelMargins['top']+anim.sineWave(cst.animAttenteDuree, blockH+pixelMargins['bottom'], execT-(cst.dureeQR+cst.dureeListes-cst.animAttenteDuree-cst.delaiAttenteBlocs*1)),
                        pixelMargins['top']+anim.sineWave(cst.animAttenteDuree, blockH+pixelMargins['bottom'], execT-(cst.dureeQR+cst.dureeListes-cst.animAttenteDuree-cst.delaiAttenteBlocs*2)),
                        pixelMargins['top']+anim.sineWave(cst.animAttenteDuree, blockH+pixelMargins['bottom'], execT-(cst.dureeQR+cst.dureeListes-cst.animAttenteDuree-cst.delaiAttenteBlocs*3))]

        for i in range(4):
            fenetre.blit(blocsBuffer[i], (pixelMargins['left'] + i * (blockW+pixelMargins['left']), posBlocs[i]))
        


def toutDessiner(fenetre):
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