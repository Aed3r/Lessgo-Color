import pygame
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
                    col = couleursPlateau[col]
                else:
                    col = couleurFond # Blanc
                pygame.draw.rect(fenetre, col, pygame.Rect(
                    i*tailleCase, j*tailleCase, tailleCase, tailleCase))                   

                # if(self.getType(i,j) == paintMore):
                #pygame.draw.circle(fenetre,(0,0,0),((i*tailleCase) + 10, (j*tailleCase) + 10) ,9)

    def afficheProp(self,fenetre):
        listePour=self.pourcentageCouleur()
        tot=0
        i=0
        for p in listePour:
            pygame.draw.rect(fenetre,couleursPlateau[i],pygame.Rect(tot*resolution[0],resolution[1]-19,resolution[0]*p,18))
            tot+=p
            i+=1
        pygame.draw.rect(fenetre,(255,255,255),pygame.Rect(tot*resolution[0],resolution[1]-19,resolution[0],18))



    # ----- Accesseurs compteurs proportion de couleurs ----- #

    def getcb(self):
        return cb

    def getcj(self):
        return cj

    def getcr(self):
        return cr

    def getcv(self):
        return cv

    def getpb(self):
        return pb

    def getpj(self):
        return pj

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


terrain = Terrain(round(resolutionPlateau[1]/tailleCase), round(resolutionPlateau[0]/tailleCase))
