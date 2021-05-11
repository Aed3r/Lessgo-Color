import pygame
import random
import os
import time
from constantes import *
import math

class Case:
    def __init__(self):
        self.color = None
        self.dirty = True

    def getColor(self):
        return self.color

    def setColor(self, newColor):
        self.color = newColor

    def isDirty(self):
        return self.dirty

    def setDirty(self, val):
        self.dirty = val

class Terrain:
    def __init__(self, long, larg):
        self.long = long
        self.larg = larg
        self.plateau = [[Case() for x in range(long)] for y in range(larg)]
        self.nbCasesColorie = [0 for i in range(4)]
        self.powerups = []
        self.initTerrain()
        self._offset = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        self._tiles = [[], [], [], []]
        # On charge tous les tiles une seule fois
        for i in range(4):
            for j in range(16):
                self._tiles[i].append(pygame.image.load(os.path.join('Data', 'Images', 'Tiles', str(i), str(j)+".png")))
        self._buffer = pygame.Surface((getResP()[0], getResP()[1]))
        self._buffer.set_alpha(effetFondu)
        self._bufferPlateau = pygame.Surface((getResP()[0], getResP()[1]))
        # On charge les images des powerups
        self._powerUpSprites = []
        for i in range(nbPowerup):
            img = pygame.image.load(os.path.join('Data', 'Images', 'Powerups', listeValeurs[i][3]+".png"))
            img = pygame.transform.smoothscale(img, (taillePowerUp, taillePowerUp))
            self._powerUpSprites.append(img)
        # On dessine le fond sur la surface
        pygame.draw.rect(self._buffer, couleurFond, pygame.Rect(0, 0, getResP()[0], getResP()[1]))
        pygame.draw.rect(self._bufferPlateau, couleurFond, pygame.Rect(0, 0, getResP()[0], getResP()[1]))

    def getCase(self, x, y):
        return self.plateau[x][y]

    def setDirty(self, x, y):
        self.plateau[x][y].setDirty(True)
        if x+1 < self.larg:
            self.plateau[x+1][y].setDirty(True)
        if x-1 >= 0:
            self.plateau[x-1][y].setDirty(True)
        if y+1 < self.long:
            self.plateau[x][y+1].setDirty(True)
        if y-1 >= 0:
            self.plateau[x][y-1].setDirty(True)

    def setColor(self, x, y, color, joueur):
        #On vérifie que la case est bien dans les limites du jeu sinon on colorie de l'autre coté !
        wrapped = False

        if x < 0:
            if wrapAround == True: 
                x = self.larg + x
            else :
                wrapped = True
        elif x >= self.larg:
            if wrapAround == True:
                x = x - self.larg
            else :
                wrapped = True
        
        if y < 0:
            if wrapAround == True:
                y = self.long + y
            else :
                wrapped = True
    
        elif y >= self.long:
            if wrapAround == True:
                y = y - self.long
            else :
                wrapped = True

        if wrapped == False:
            self.modifCompteur((x, y), color, joueur)
            self.plateau[x][y].setColor(color)
            self.setDirty(x, y)

    def setType(self, x, y, type):
        self.powerups.append({'x': x, 'y': y, 'type': type})

    def getLong(self):
        return self.long

    def getLarg(self):
        return self.larg

    def getColor(self, x, y):
        if x < 0 or x >= self.larg or y < 0 or y >= self.long:
            return None
        else:
            return self.plateau[x][y].getColor()

    def getType(self, x, y, rayon):
        for i in range(len(self.powerups)):
            p = self.powerups[i]
            if math.sqrt(math.pow(p['x']-x, 2)+math.pow(p['y']-y, 2)) <= (rayon*tailleCase)+taillePowerUp/2:
                self.powerups.pop(i)
                return p['type']
        return None

    def initTerrain(self):
        taille = (int)(getResP()[0] / tailleCase * propZoneInit)
        for i in range(taille):
            for j in range(taille):
                self.setColor(i, j, 0, None)
                self.setColor(self.larg-i-1, j, 1, None)
                self.setColor(i, self.long-j-1, 2, None)
                self.setColor(self.larg-i-1, self.long-j-1, 3, None)
        
        for i in range(powerUpsDemarage):
            self.placerPowerupAlea()

    def afficheTerrain(self, fenetre):
        for i in range(self.larg):
            for j in range(self.long):
                if self.plateau[i][j].isDirty():
                    col = self.getColor(i, j)
                    self.plateau[i][j].setDirty(False)
                    if col != None:
                        code = self._calcNeighbors(i, j)
                        if (code != 15):
                            self._buffer.blit(self._tiles[col][code], (i*tailleCase, j*tailleCase))
                        else:
                            pygame.draw.rect(self._buffer, couleursPlateau[col], pygame.Rect(i*tailleCase, j*tailleCase, tailleCase, tailleCase))
        
        self._bufferPlateau.blit(self._buffer, (0,0))
        fenetre.blit(self._bufferPlateau, (0, 0))

        # Powerup
        for p in self.powerups:
            fenetre.blit(self._powerUpSprites[p['type']], (p['x']-taillePowerUp/2, p['y']-taillePowerUp/2))          

    # Construit un code binaire en ajoutant comprenant 1 à l'indice i si le le voisin i (déterminé par self._offset) est de la même couleur que la case (x, y)
    def _calcNeighbors(self, x, y):
        code = 0
        col = self.getColor(x, y)
        for i in range(len(self._offset)):
            if self.getColor(x+self._offset[i][0], y+self._offset[i][1]) == col:
                code |= 1<<i
        return code

    def afficheProp(self,fenetre):
        listePour=self.pourcentageCouleur()
        tot=0
        i=0
        for p in listePour:
            pygame.draw.rect(fenetre,couleursPlateau[i],pygame.Rect(tot*getRes()[0],getRes()[1]-19,getRes()[0]*p,18))
            tot+=p
            i+=1
        pygame.draw.rect(fenetre,(255,255,255),pygame.Rect(tot*getRes()[0],getRes()[1]-19,getRes()[0],18))

    def modifCompteur(self, pos, color, joueur):
        colorNow = self.getColor(pos[0], pos[1])

        if colorNow == color:
            return

        if colorNow != None:
            self.nbCasesColorie[colorNow] -= 1
        
        self.nbCasesColorie[color] += 1
        if joueur != None:
            joueur.increaseScore(1)

    # Calcul les pourcentages à partir des compteurs. Renvoie une liste de réels
    def pourcentageCouleur(self):
        listePourc = []
        nbCases = self.getLong() * self.getLarg()
        for i in range(4):
            listePourc.append(self.nbCasesColorie[i]/ nbCases)
        return listePourc

    def _bresenham(self, x1, y1, x2, y2, transX, transY, inv, offX, offY, j):
        y = y1
        dX = x2-x1
        dY = y2-y1
        m = 2*dY
        err = -dX;

        for x in range(x1, x2+1):
            if inv:
                cercle_bresenham_plateau(j.rayonCouleur, y*transY+offX, x*transX+offY, j.EQUIPE, j)
                remplissage(y*transY+offX, x*transX+offY, j.EQUIPE, j)
            else:
                cercle_bresenham_plateau(j.rayonCouleur, x*transX+offX, y*transY+offY, j.EQUIPE, j)
                remplissage(x*transX+offX, y*transY+offY, j.EQUIPE, j)
            err += m
            if err >= 0:
                y += 1
                err -= 2 * dX

    def dessinerLigne(self, x1, y1, x2, y2, j):
        dX = x2-x1
        dY = y2-y1

        if dX < 0:
            if dY < 0: # Bas gauche 
                if abs(dX) > abs(dY): # 5 
                    self._bresenham(0, 0, -dX, -dY, -1, -1, 0, x1, y1, j)
                else: # 6 
                    self._bresenham(0, 0, -dY, -dX, -1, -1, 1, x1, y1, j)
            else: # Haut gauche 
                if abs(dX) > abs(dY): # 4 
                    self._bresenham(0, 0, -dX, dY, -1, 1, 0, x1, y1, j)
                else: # 3 
                    self._bresenham(0, 0, dY, -dX, 1, -1, 1, x1, y1, j)
        else:
            if dY < 0: # Bas droite 
                if abs(dX) > abs(dY): # 8 
                    self._bresenham(0, 0, dX, -dY, 1, -1, 0, x1, y1, j)
                else: # 7 
                    self._bresenham(0, 0, -dY, dX, -1, 1, 1, x1, y1, j)
            else: # Haut droite 
                if abs(dX) > abs(dY): # 1 
                    self._bresenham(0, 0, dX, dY, 1, 1, 0, x1, y1, j)
                else: # 2 
                    self._bresenham(0, 0, dY, dX, 1, 1, 1, x1, y1, j)
    
    def placerPowerupAlea(self):
        resolution = getRes()
        taille = (int)(resolution[0] * propZoneInit)
        type = random.randrange(nbPowerup)
        bienPlace =  False
        
        while bienPlace == False:
            x = random.randrange(resolution[0])
            y = random.randrange(resolution[1])
            bienPlace = True
            #On vérifie le placement du powerup
            if (x<taille and y<taille) or (x < taille and y > resolution[1] - taille) or (x > resolution[0] - taille and y < taille) or (x > resolution[0] - taille and y > resolution[1] - taille) :
                bienPlace = False

            #On vérifie si le powerup est sur un autre si il est bien placé
            if bienPlace == True:
                for p in self.powerups:
                    if(p['x'] == x and p['y'] == y):
                        bienPlace = False
        
        self.setType(x, y, type)

        #for i in range(taille):
         #   for j in range(taille):
          #      self.setColor(i, j, 0)
           #     self.setColor(self.larg-i-1, j, 1)
            #    self.setColor(i, self.long-j-1, 2)
             #   self.setColor(self.larg-i-1, self.long-j-1, 3)

def cercle_bresenham_plateau(r, xc, yc, couleur, joueur):
    x = 0
    y = r
    d = 1 -r
    while y >= x:
        terrain.setColor(x + xc, y+ yc, couleur, joueur)
        terrain.setColor(y + xc, x+ yc, couleur, joueur)
        terrain.setColor(-x + xc, y+ yc, couleur, joueur)
        terrain.setColor(-y + xc, x+ yc, couleur, joueur)
        terrain.setColor(x + xc, -y + yc, couleur, joueur)
        terrain.setColor(y + xc, -x + yc, couleur, joueur)
        terrain.setColor(-x + xc, -y + yc, couleur, joueur)
        terrain.setColor(-y + xc, -x + yc, couleur, joueur)
        if d < 0: 
            d = d + 2*x + 3
        else:
            d = d + 2*(x-y) + 5
            y -= 1
        x += 1

def remplissage(x, y, couleur, joueur):
    if terrain.getColor(x, y) != couleur:
        terrain.setColor(x, y, couleur, joueur)
        remplissage(x+1,y,couleur, joueur)
        remplissage(x-1,y,couleur, joueur)
        remplissage(x,y+1,couleur, joueur)
        remplissage(x,y-1,couleur, joueur)

terrain = None
def initTerrain():
    global terrain
    terrain = Terrain(round(getResP()[1]/tailleCase), round(getResP()[0]/tailleCase))

def getTerrain():
    global terrain
    return terrain

def updateCase(j):
    posCase1 = ((int) (j.oldX/getResP()[0]*terrain.getLarg()), (int) (j.oldY/getResP()[1]*terrain.getLong()))
    posCase2 = ((int) (j.x/getResP()[0]*terrain.getLarg()), (int) (j.y/getResP()[1]*terrain.getLong()))

    j.oldX = j.x
    j.oldY = j.y
    
    terrain.dessinerLigne(posCase1[0], posCase1[1], posCase2[0], posCase2[1], j)

    #Si le joueur passe sur un PowerUp il le récupère  
    p = terrain.getType(j.x, j.y, j.getRayon())
    if (p != None):
        j.setPowerUp(p)