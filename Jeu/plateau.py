import pygame
import os
import time
from constantes import *

class Case:
    def __init__(self, startingType):
        self.type = startingType
        self.color = None

    def getType(self):
        return self.type

    def getColor(self):
        return self.color

    def setType(self, newType):
        self.type = newType

    def setColor(self, newColor):
        self.color = newColor

    def __repr__(self):
        return repr([self.color, self.type])


class Terrain:
    def __init__(self, long, larg):
        self.long = long
        self.larg = larg
        self.plateau = [[Case(0) for x in range(long)] for y in range(larg)]
        self.nbCasesColorie = [0 for i in range(4)]
        self.initTerrain()
        self._offset = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        self._tiles = [[], [], [], []]
        # On charge tous les tiles une seule fois
        for i in range(4):
            for j in range(16):
                self._tiles[i].append(pygame.image.load(os.path.join('Data', 'Images', 'Tiles', str(i), str(j)+".png")))
        self._buffer = pygame.Surface((resolutionPlateau[0], resolutionPlateau[1]))
        # On dessine le fond sur la surface
        pygame.draw.rect(self._buffer, couleurFond, pygame.Rect(0, 0, resolutionPlateau[0], resolutionPlateau[1]))

    def getCase(self, x, y):
        return self.plateau[x][y]

    def setColor(self, x, y, color):
        self.modifCompteur((x, y), color)
        self.plateau[x][y].setColor(color)

    def setType(self, x, y, type):
        self.plateau[x][y].setType(type)

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
        return self.plateau[x][y].getType()

    def initTerrain(self):
        taille = (int)(resolutionPlateau[0] / tailleCase * propZoneInit)
        for i in range(taille):
            for j in range(taille):
                self.setColor(i, j, 0)
                self.setColor(self.larg-i-1, j, 1)
                self.setColor(i, self.long-j-1, 2)
                self.setColor(self.larg-i-1, self.long-j-1, 3)

        self.setType(int(self.larg/2), int(self.long/2), paintMore)

    def afficheTerrain(self, fenetre):
        for i in range(self.larg):
            for j in range(self.long):
                col = self.getColor(i, j)
                if col != None:
                    code = self._calcNeighbors(i, j)
                    self._buffer.blit(self._tiles[col][code], (i*tailleCase, j*tailleCase))
        
                # if(self.getType(i,j) == paintMore):
                #pygame.draw.circle(fenetre,(0,0,0),((i*tailleCase) + 10, (j*tailleCase) + 10) ,9)
        fenetre.blit(self._buffer, (0, 0))

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
            pygame.draw.rect(fenetre,couleursPlateau[i-1],pygame.Rect(tot*resolution[0],resolution[1]-19,resolution[0]*p,18))
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

terrain = None
def initTerrain():
    global terrain
    terrain = Terrain(round(resolutionPlateau[1]/tailleCase), round(resolutionPlateau[0]/tailleCase))

def getTerrain():
    global terrain
    return terrain

def updateCase(j):
    posCase = ((int) (j.x/resolutionPlateau[0]*terrain.getLarg()), (int) (j.y/resolutionPlateau[1]*terrain.getLong()))
    terrain.setColor(posCase[0], posCase[1], j.EQUIPE)