#Classe servant a instancier des joueurs

from constantes import *

joueurs = []

class Joueur(object): 

    def __init__(self, id, equipe, x = 0, y = 0):
        super().__init__()
        #Definition des variables
        self.x = x
        self.y = y
        self.dead = False
        self.dX = 0
        self.dY = 0
        #definition des constantes
        self.ID = id
        self.EQUIPE = equipe
        #On assigne une couleur au joueur selon son équipe
        if equipe == 1:
            self.COLOR = (0, 127, 255)
        elif equipe == 2:
            self.COLOR = (255, 255, 0)
        elif equipe == 3:
            self.COLOR = (187, 11, 11)
        elif equipe == 4:
            self.COLOR = (0,255,0) 
        else:
            print("ATTENTION MAUVAISE EQUIPE POUR LE JOUEUR", id)
            self.COLOR = (0,0,0)

    def move(self):
        self.x = int(self.x+self.dX)
        self.y = int(self.y+self.dY)

        # Vérification de dépassement des bordures
        if (self.x > resolution[0] ): self.x = 0
        if (self.x < 0): self.x = resolution[0]
        if (self.y > resolution[1] ): self.y = 0
        if (self.y < 0): self.y = resolution[1]

    def isDead(self):
        return self.dead

    def setDead(self, valeur):
        self.dead = valeur

    def setDirection (self, dx, dy):
        self.dX = dx
        self.dY = dy

def placementInitial (j):
    if j.EQUIPE == 1:
        j.x = 100
        j.y = 100
    elif j.EQUIPE == 2:
        j.x = resolution[0] - 100
        j.y = 100
    elif j.EQUIPE == 3:
        j.x = resolution[0] - 100
        j.y = resolution[1] - 100
    elif j.EQUIPE == 4:
        j.x = 100
        j.y = resolution[1] - 100

def comparJoueur(j):
    return j.y

def ajouterJoueur(joueur):
   placementInitial(joueur)
   joueurs.append(joueur)






# Gestion du tableau de joueurs (ajout, enlever, placement initial suivant équipe, affichage)
# deprecated
class ListeJoueurs(object):

    def __init__(self):
        super().__init__()
        self.ekip1 = []
        self.ekip2 = []
        self.ekip3 = []
        self.ekip4 = []
        #Liste des listes de chaque équipe
        self.lekip = [self.ekip1, self.ekip2, self.ekip3, self.ekip4]

    def ajouter(self, j):
        if j.EQUIPE == 1:
            self.lekip[0].append(j)
        elif j.EQUIPE == 2:
            self.lekip[1].append(j)
        elif j.EQUIPE == 3:
            self.lekip[2].append(j)
        elif j.EQUIPE == 4:
            self.lekip[3].append(j)

    def enlever(self, j):
        if j.EQUIPE == 1:
            self.lekip[0].remove(j)
        elif j.EQUIPE == 2:
            self.lekip[1].remove(j)
        elif j.EQUIPE == 3:
            self.lekip[2].remove(j)
        elif j.EQUIPE == 4:
            self.lekip[3].remove(j)

    def placementJoueurs(self):
        for i in range(4):  
            for j in self.lekip[i]:
                if j.EQUIPE == 1:
                    j.x = placex1
                    j.y = placey1
                elif j.EQUIPE == 2:
                    j.x = placex2
                    j.y = placey2
                elif j.EQUIPE == 3:
                    j.x = placex3
                    j.y = placey3
                elif j.EQUIPE == 4:
                    j.x = placex4
                    j.y = placey4

    def afficher(self, fenetre):
        fenetre.fill((80,80,80)) #couleur fenetre
        for i in range(4):
            for j in self.lekip[i]:
                j.afficher(fenetre)
