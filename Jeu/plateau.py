import pygame
import random
import os
import time
import constantes as cst
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
        # On charge tous les tiles une seule fois et on les redimensionne
        for i in range(4):
            for j in range(16):
                self._tiles[i].append(pygame.image.load(os.path.join('Data', 'Images', 'Tiles', str(i), str(j)+".png")))
                self._tiles[i][j] = pygame.transform.smoothscale(self._tiles[i][j], (round(cst.tailleCase*cst.scale), round(cst.tailleCase*cst.scale)))
        self._buffer = pygame.Surface((cst.getResP()[0], cst.getResP()[1]))
        self._buffer.set_alpha(cst.effetFondu)
        self._bufferPlateau = pygame.Surface((cst.getResP()[0], cst.getResP()[1]))
        # On charge les images des powerups
        self._powerUpSprites = []
        for i in range(cst.nbPowerup + cst.nbSpecial):
            img = pygame.image.load(os.path.join('Data', 'Images', 'Powerups', cst.listeValeurs[i][3]+".png"))
            img = pygame.transform.smoothscale(img, (round(cst.taillePowerUp*cst.scale), round(cst.taillePowerUp*cst.scale)))
            self._powerUpSprites.append(img)
        # On dessine le fond sur la surface
        pygame.draw.rect(self._buffer, cst.couleurFond, pygame.Rect(0, 0, cst.getResP()[0], cst.getResP()[1]))
        pygame.draw.rect(self._bufferPlateau, cst.couleurFond, pygame.Rect(0, 0, cst.getResP()[0], cst.getResP()[1]))

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
            if cst.wrapAround == True: 
                x = self.larg + x
            else :
                wrapped = True
        elif x >= self.larg:
            if cst.wrapAround == True:
                x = x - self.larg
            else :
                wrapped = True
        
        if y < 0:
            if cst.wrapAround == True:
                y = self.long + y
            else :
                wrapped = True
    
        elif y >= self.long:
            if cst.wrapAround == True:
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
            if math.sqrt(math.pow(p['x']-x, 2)+math.pow(p['y']-y, 2)) <= (rayon*cst.tailleCase)+cst.taillePowerUp/2:
                self.powerups.pop(i)
                return p['type']
        return None

    def initTerrain(self):
        taille = (int)((cst.getResP()[0]*cst.scale) / cst.tailleCase * cst.propZoneInit)
        for i in range(taille):
            for j in range(taille):
                self.setColor(i, j, 0, None)
                self.setColor(self.larg-i-1, j, 1, None)
                self.setColor(i, self.long-j-1, 2, None)
                self.setColor(self.larg-i-1, self.long-j-1, 3, None)
        
        for i in range(cst.powerUpsDemarage):
            self.placerPowerupAlea(False)
        
        self.setType(cst.getResP()[0]/2, cst.getResP()[1]/2, 3)

    def afficheTerrain(self, fenetre):
        for i in range(self.larg):
            for j in range(self.long):
                if self.plateau[i][j].isDirty():
                    col = self.getColor(i, j)
                    self.plateau[i][j].setDirty(False)
                    if col != None:
                        code = self._calcNeighbors(i, j)
                        if (code != 15):
                            self._buffer.blit(self._tiles[col][code], (i*round(cst.tailleCase*cst.scale), j*round(cst.tailleCase*cst.scale)))
                        else:
                            pygame.draw.rect(self._buffer, cst.couleursPlateau[col], pygame.Rect(i*round(cst.tailleCase*cst.scale), j*round(cst.tailleCase*cst.scale), round(cst.tailleCase*cst.scale), round(cst.tailleCase*cst.scale)))
        
        self._bufferPlateau.blit(self._buffer, (0,0))
        fenetre.blit(self._bufferPlateau, (0, 0))

        # Powerup
        for p in self.powerups:
            fenetre.blit(self._powerUpSprites[p['type']], (p['x']-(cst.taillePowerUp*cst.scale)/2, p['y']-(cst.taillePowerUp*cst.scale)/2))          

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
            pygame.draw.rect(fenetre,cst.couleursPlateau[i],pygame.Rect(tot*cst.getRes()[0],cst.getRes()[1]-19,cst.getRes()[0]*p,18))
            tot+=p
            i+=1
        pygame.draw.rect(fenetre,cst.couleurFond,pygame.Rect(tot*cst.getRes()[0],cst.getRes()[1]-19,cst.getRes()[0],18))

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
        err = -dX

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
    
    def placerPowerupAlea(self, gold):
        resolution = (cst.getResP()[0], cst.getResP()[1])
        taille = (int)(resolution[0] * cst.propZoneInit * cst.scale)
        if gold:
            typePU = random.randrange(cst.nbPowerup, cst.nbPowerup+cst.nbSpecial)
        else:
            typePU = random.randrange(cst.nbPowerup)
        bienPlace =  False
        
        while bienPlace == False:
            x = random.randrange(resolution[0])
            y = random.randrange(resolution[1])
            bienPlace = True
            #On vérifie le placement du powerup
            if (x<taille and y<taille) or (x < taille and y > resolution[1] - taille) or (x > resolution[0] - taille and y < taille) or (x > resolution[0] - taille and y > resolution[1] - taille) or y > resolution[1] - cst.tailleBarre - (cst.taillePowerUp/2):
                bienPlace = False

            #On vérifie si le powerup est sur un autre si il est bien placé
            if bienPlace == True:
                for p in self.powerups:
                    if(p['x'] == x and p['y'] == y):
                        bienPlace = False
        
        self.setType(x, y, typePU)

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
    if terrain.getColor(x, y) != couleur and x > 0 and y > 0 and x < terrain.getLarg() and y < terrain.getLong():
        terrain.setColor(x, y, couleur, joueur)
        remplissage(x+1,y,couleur, joueur)
        remplissage(x-1,y,couleur, joueur)
        remplissage(x,y+1,couleur, joueur)
        remplissage(x,y-1,couleur, joueur)
terrain = None

def initTerrain():
    global terrain
    terrain = Terrain(round((cst.getResP()[1]/cst.scale)/cst.tailleCase), round((cst.getResP()[0]/cst.scale)/cst.tailleCase))

def getTerrain():
    global terrain
    return terrain

def updateCase(j):
    posCase1 = ((int) (j.oldX/cst.getResP()[0]*terrain.getLarg()), (int) (j.oldY/cst.getResP()[1]*terrain.getLong()))
    posCase2 = ((int) (j.x/cst.getResP()[0]*terrain.getLarg()), (int) (j.y/cst.getResP()[1]*terrain.getLong()))

    j.oldX = j.x
    j.oldY = j.y
    
    terrain.dessinerLigne(posCase1[0], posCase1[1], posCase2[0], posCase2[1], j)

    if cst.botPowerUpsPickup or not j.isBot():
        #Si le joueur passe sur un PowerUp il le récupère  
        p = terrain.getType(j.x, j.y, j.getRayon()*cst.scale)
        if (p != None):
            j.setPowerUp(p)
            if (cst.listeValeurs[p][3].endswith("Gold")):
                if cst.listeValeurs[p][3] == "paintMoreGold":
                    text = "Bonus de coloriage pour "
                if cst.listeValeurs[p][3] == "gottaGoFastGold":
                    text = "Bonus de vitesse pour "

                text += "l'équipe " + cst.nomsEquipes[j.getEquipe()] + " !"

                return text
            else:
                return None
