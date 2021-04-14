import pygame
from constantes import *

# Compteurs de couleurs
cr = 0
cb = 0
cj = 0
cv = 0
pr = 0
pb = 0
pj = 0
pv = 0


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
        self.initTerrain()

    def getCase(self, x, y):
        return self.plateau[x][y]

    def setColor(self, x, y, color):
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

        self.setType(int(self.larg/2), int(self.long/2), gottaGoFast)

    def afficheTerrain(self, fenetre):
        for i in range(self.larg):
            for j in range(self.long):
                col = self.getColor(i, j)
                if col != None:
                    col = couleursPlateau[col]
                else:
                    col = (255, 255, 255) # Blanc
                pygame.draw.rect(fenetre, col, pygame.Rect(
                    i*tailleCase, j*tailleCase, tailleCase, tailleCase))                   

                if(self.getType(i,j) > 0 & self.getType(i, j) < nbPowerup):
                    pygame.draw.circle(fenetre,(0,0,0),((i*tailleCase) + 10, (j*tailleCase) + 10) ,tailleCase/2)

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

    def getpr(self):
        return pr

    def getpv(self):
        return pv
    # ----- Fin accesseurs compteurs proportion de couleurs ----- #

    def modifCompteur(self, x, y, color):
        global cb
        global cj
        global cr
        global cv
        colorNow = self.getColor(
            (int)(x/resolutionPlateau[0]*self.larg), (int)(y/resolutionPlateau[1]*self.long))

        if(colorNow == 1 and cb >= 0):  # bleu
            cb = cb-1
        elif(colorNow == 2 and cj >= 0):  # jaune
            cj = cj-1
            # print(cj)
        elif(colorNow == 3 and cr >= 0):  # rouge
            cr = cr-1
        elif(colorNow == 4 and cv >= 0):  # vert
            cv = cv-1

        if(color == 1):  # bleu
            cb = cb+1
        elif(color == 2):  # jaune
            cj = cj+1
            # print(cj)
        elif(color == 3):  # rouge
            cr = cr+1
        elif(color == 4):  # vert
            cv = cv+1

    # Calcul les pourcentages à partir des compteurs
    def pourcentageCouleur(self):
        global pr
        global pb
        global pj
        global pv
        pr = 0
        pb = 0
        pj = 0
        pv = 0
        pb = cb*100/(resolutionPlateau[0]*resolutionPlateau[1])
        pr = cr*100/(resolutionPlateau[0]*resolutionPlateau[1])
        pj = cj*100/(resolutionPlateau[0]*resolutionPlateau[1])
        pv = cv*100/(resolutionPlateau[0]*resolutionPlateau[1])


terrain = Terrain(round(resolutionPlateau[1]/tailleCase), round(resolutionPlateau[0]/tailleCase))
