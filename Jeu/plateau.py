***REMOVED***
from constantes import *

# Compteurs de couleurs
cr = 0; cb = 0; cj = 0; cv = 0
pr = 0; pb = 0; pj = 0; pv = 0

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
        taille = (int) (resolutionPlateau[0] / tailleCase / propZoneInit)
        for i in range(taille):
            for j in range(taille):
                self.setColor(i,j,1)
                self.setColor(self.larg-i-1, j, 2)
                self.setColor(i, self.long-j-1, 3)
                self.setColor(self.larg-i-1, self.long-j-1, 4)

        self.setType(int(self.larg/2), int(self.long/2), paintMore)


    def afficheTerrain(self,fenetre):
        for i in range(self.larg):
                for j in range (self.long):
                        if(self.getColor(i,j) == 1): #bleu
                            pygame.draw.rect(fenetre,(0,0,255),pygame.Rect(i*tailleCase,j*tailleCase,tailleCase,tailleCase))    
                        elif(self.getColor(i,j) == 2): #jaune
                            pygame.draw.rect(fenetre,(240,240,0),pygame.Rect(i*tailleCase,j*tailleCase,tailleCase,tailleCase))    
                        elif(self.getColor(i,j) == 3): #rouge
                            pygame.draw.rect(fenetre,(160,11,11),pygame.Rect(i*tailleCase,j*tailleCase,tailleCase,tailleCase))    
                        elif(self.getColor(i,j) == 4): #vert
                            pygame.draw.rect(fenetre,(0,230,0),pygame.Rect(i*tailleCase,j*tailleCase,tailleCase,tailleCase))
                        else : pygame.draw.rect(fenetre,(255,255,255),pygame.Rect(i*tailleCase,j*tailleCase,tailleCase,tailleCase))
                        if(self.getType(i,j) == paintMore):
                            pygame.draw.circle(fenetre,(0,0,0),((i*tailleCase) + 10, (j*tailleCase) + 10) ,9)
    
    
    # ----- rajout paul-antoine ----- #
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

    def parcoursCouleur(self):
        global cb; global cj; global cr; global cv
        cb = 0; cj = 0; cr = 0; cv = 0
        for i in range(self.larg):
            for j in range (self.long):
                if(self.getColor(i,j) == 1): #bleu
                    cb=cb+1
                elif(self.getColor(i,j) == 2): #jaune
                    cj=cj+1
                    #print(cj)
                elif(self.getColor(i,j) == 3): #rouge
                    cr=cr+1
                elif(self.getColor(i,j) == 4): #vert
                    cv=cv+1

    def pourcentageCouleur(self):
        global pr; global pb; global pj; global pv;
        pr = 0; pb = 0; pj = 0; pv = 0
        pb=cb*100/(resolutionPlateau[0]*resolutionPlateau[1])
        pr=cr*100/(resolutionPlateau[0]*resolutionPlateau[1])
        pj=cj*100/(resolutionPlateau[0]*resolutionPlateau[1])
        pv=cv*100/(resolutionPlateau[0]*resolutionPlateau[1])
    # ----- fin rajout paul-antoine ----- #

terrain = Terrain(round(resolutionPlateau[1]/tailleCase), round(resolutionPlateau[0]/tailleCase))
