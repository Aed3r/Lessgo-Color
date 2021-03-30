import pygame
from constantes import *

class Case:
    def __init__(self,startingColor,startingType):
        self.type=startingType
        self.color=startingColor
    
    def getType(self):
        return self.type

    def getColor(self):
        return self.color

    def setType(self,newType):  
        self.type=newType
    
    def setColor(self,newColor):
        self.color=newColor
    
    def __repr__(self):
        return repr([self.color,self.type])


class Terrain:
    def __init__(self,long,larg):
        self.long=long
        self.larg=larg
        self.plateau = [[ Case(0,0) for x in range(long)] for y in range(larg)]
        self.initTerrain()
    
    def getCase(self,x,y):
        return self.plateau[x][y]

    def setColor(self,x,y,color):
        self.plateau[x][y].setColor(color)

    def setType(self,x,y,type):
        self.plateau[x][y].setType(type)
    
    def getLong(self):
        return self.long
    
    def getLarg(self):
        return self.larg
    
    def getColor(self,x,y):
        return self.plateau[x][y].getColor()
    
    def getType(self,x,y):
        return self.plateau[x][y].getType()

    def initTerrain(self):
        taille = (int) (resolution[0] / tailleCase / propZoneInit)
        for i in range(taille):
            for j in range(taille):
                self.setColor(i,j,1)
                self.setColor(self.larg-i-1, j, 2)
                self.setColor(i, self.long-j-1, 3)
                self.setColor(self.larg-i-1, self.long-j-1, 4)


    def afficheTerrain(self,fenetre):
        for i in range(self.larg):
                for j in range (self.long):
                        if(self.getColor(i,j) == 1):
                            pygame.draw.rect(fenetre,(0,0,255),pygame.Rect(i*tailleCase,j*tailleCase,tailleCase,tailleCase))    
                        elif(self.getColor(i,j) == 2):
                            pygame.draw.rect(fenetre,(240,240,0),pygame.Rect(i*tailleCase,j*tailleCase,tailleCase,tailleCase))    
                        elif(self.getColor(i,j) == 3):
                            pygame.draw.rect(fenetre,(160,11,11),pygame.Rect(i*tailleCase,j*tailleCase,tailleCase,tailleCase))    
                        elif(self.getColor(i,j) == 4):
                            pygame.draw.rect(fenetre,(0,230,0),pygame.Rect(i*tailleCase,j*tailleCase,tailleCase,tailleCase))
                        else : pygame.draw.rect(fenetre,(255,255,255),pygame.Rect(i*tailleCase,j*tailleCase,tailleCase,tailleCase))

terrain = Terrain(round(resolution[1]/tailleCase), round(resolution[0]/tailleCase))