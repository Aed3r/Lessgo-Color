import pygame
import random
import os
import time
from constantes import *

class Case:
    def __init__(self):
        self.color = None

    def getColor(self):
        return self.color

    def setColor(self, newColor):
        self.color = newColor


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
        self._buffer = pygame.Surface((resolutionPlateau[0], resolutionPlateau[1]))
        # On charge les images des powerups
        self._powerUpSprites = []
        for i in range(nbPowerup):
            self._powerUpSprites.append(pygame.image.load(os.path.join('Data', 'Images', 'Powerups', listeValeurs[i][3])))
        # On dessine le fond sur la surface
        pygame.draw.rect(self._buffer, couleurFond, pygame.Rect(0, 0, resolutionPlateau[0], resolutionPlateau[1]))

    def getCase(self, x, y):
        return self.plateau[x][y]

    def setColor(self, x, y, color):
        #On vérifie que la case est bien dans les limites du jeu sinon on colorie de l'auter coté !
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
            self.modifCompteur((x, y), color)
            self.plateau[x][y].setColor(color)

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

    def getType(self, x, y):
        for p in self.powerups:
            if (x > p['x']-15 and x < p['x']+15 and y > p['y'] - 15 and p['y'] + 15):
                self.powerups.remove(p)
                return p['type']
        return None

    def initTerrain(self):
        taille = (int)(resolutionPlateau[0] / tailleCase * propZoneInit)
        for i in range(taille):
            for j in range(taille):
                self.setColor(i, j, 0)
                self.setColor(self.larg-i-1, j, 1)
                self.setColor(i, self.long-j-1, 2)
                self.setColor(self.larg-i-1, self.long-j-1, 3)

    def afficheTerrain(self, fenetre):
        for i in range(self.larg):
            for j in range(self.long):
                col = self.getColor(i, j)
                if col != None:
                    code = self._calcNeighbors(i, j)
                    self._buffer.blit(self._tiles[col][code], (i*tailleCase, j*tailleCase))
        
        fenetre.blit(self._buffer, (0, 0))

        # Powerup
        for p in self.powerups:
            fenetre.blit(self._powerUpSprites[p['type']], (p['x']-15, p['y']-15))             

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
            pygame.draw.rect(fenetre,couleursPlateau[i],pygame.Rect(tot*resolution[0],resolution[1]-19,resolution[0]*p,18))
            tot+=p
            i+=1
        pygame.draw.rect(fenetre,(255,255,255),pygame.Rect(tot*resolution[0],resolution[1]-19,resolution[0],18))

    def modifCompteur(self, pos, color):
        colorNow = self.getColor(pos[0], pos[1])

        if colorNow != None :
            self.nbCasesColorie[colorNow] -= 1
        
        self.nbCasesColorie[color] += 1

    # Calcul les pourcentages à partir des compteurs. Renvoie une liste de réels
    def pourcentageCouleur(self):
        listePourc = []
        nbCases = self.getLong() * self.getLarg()
        for i in range(4):
            listePourc.append(self.nbCasesColorie[i]/ nbCases)
        return listePourc

    def _bresenham(self, x1, y1, x2, y2, transX, transY, inv, offX, offY, col):
        y = y1
        dX = x2-x1
        dY = y2-y1
        m = 2*dY
        err = -dX;

        for x in range(x1, x2+1):
            if inv:
                self.setColor(y*transY+offX, x*transX+offY, col)
            else:
                self.setColor(x*transX+offX, y*transY+offY, col)
            err += m
            if err >= 0:
                y += 1
                err -= 2 * dX

    def dessinerLigne(self, x1, y1, x2, y2, col):
        dX = x2-x1
        dY = y2-y1

        if dX < 0:
            if dY < 0: # Bas gauche 
                if abs(dX) > abs(dY): # 5 
                    self._bresenham(0, 0, -dX, -dY, -1, -1, 0, x1, y1, col)
                else: # 6 
                    self._bresenham(0, 0, -dY, -dX, -1, -1, 1, x1, y1, col)
            else: # Haut gauche 
                if abs(dX) > abs(dY): # 4 
                    self._bresenham(0, 0, -dX, dY, -1, 1, 0, x1, y1, col)
                else: # 3 
                    self._bresenham(0, 0, dY, -dX, 1, -1, 1, x1, y1, col)
        else:
            if dY < 0: # Bas droite 
                if abs(dX) > abs(dY): # 8 
                    self._bresenham(0, 0, dX, -dY, 1, -1, 0, x1, y1, col)
                else: # 7 
                    self._bresenham(0, 0, -dY, dX, -1, 1, 1, x1, y1, col)
            else: # Haut droite 
                if abs(dX) > abs(dY): # 1 
                    self._bresenham(0, 0, dX, dY, 1, 1, 0, x1, y1, col)
                else: # 2 
                    self._bresenham(0, 0, dY, dX, 1, 1, 1, x1, y1, col)
    
    def placerPowerupAlea(self):
        taille = (int)(resolutionPlateau[0] * propZoneInit)
        type = random.randrange(nbPowerup)
        x = random.randrange(taille, resolutionPlateau[0] - taille)
        y = random.randrange(taille, resolutionPlateau[1] - taille)
        
        self.setType(x, y, type)


terrain = None
def initTerrain():
    global terrain
    terrain = Terrain(round(resolutionPlateau[1]/tailleCase), round(resolutionPlateau[0]/tailleCase))

def getTerrain():
    global terrain
    return terrain

def cercle_bresenham_plateau(r, xc, yc, couleur):
    x = 0
    y = r
    d = 1 -r
    while y >= x:
        terrain.setColor(x + xc, y+ yc, couleur)
        terrain.setColor(y + xc, x+ yc, couleur)
        terrain.setColor(-x + xc, y+ yc, couleur)
        terrain.setColor(-y + xc, x+ yc, couleur)
        terrain.setColor(x + xc, -y + yc, couleur)
        terrain.setColor(y + xc, -x + yc, couleur)
        terrain.setColor(-x + xc, -y + yc, couleur)
        terrain.setColor(-y + xc, -x + yc, couleur)
        if d < 0: 
            d = d + 2*x + 3
        else:
            d = d + 2*(x-y) + 5
            y -= 1
        x += 1



def updateCase(j):
    posCase1 = ((int) (j.oldX/resolutionPlateau[0]*terrain.getLarg()), (int) (j.oldY/resolutionPlateau[1]*terrain.getLong()))
    posCase2 = ((int) (j.x/resolutionPlateau[0]*terrain.getLarg()), (int) (j.y/resolutionPlateau[1]*terrain.getLong()))
    
    terrain.dessinerLigne(posCase1[0], posCase1[1], posCase2[0], posCase2[1], j.EQUIPE)
    if j.rayonCouleur > 0:
        cercle_bresenham_plateau(j.rayonCouleur, posCase1[0], posCase1[1], j.EQUIPE)
        if j.rayonCouleur > 1:
            for r in range(j.rayonCouleur):
                cercle_bresenham_plateau(r, posCase1[0], posCase1[1], j.EQUIPE)
    j.drawn = True

    #Si le joueur passe sur un PowerUp il le récupère  
    p = terrain.getType(j.x, j.y)
    if (p != None):
        j.setPowerUp(p)