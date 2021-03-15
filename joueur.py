#Classe servant a instancier des joueurs
import pygame

joueurs = []

# TODO: tenir vecteur direction en plus de la position
class Joueur(object): 
    def __init__(self, id, equipe, x = 0, y = 0):
        super().__init__()
        #Definition des variables
        self.x = x
        self.y = y
        self.dead = False
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
    def translation(self, dx, dy):
        self.x += dx
        self.y += dy
    def isDead(self):
        return self.dead
    def setDead(self, valeur):
        self.dead = valeur
    def afficher(self, fenetre):
        if self.isDead():
            self.x = -1
            self.y = -1
        else:
            pygame.draw.circle(fenetre, self.COLOR, [self.x, self.y], 5)

# Gestion du tableau de joueurs (ajout, enlever, placement initial suivant équipe, affichage)
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
                    j.x = 12
                    j.y = 12
                elif j.EQUIPE == 2:
                    j.x = 1900
                    j.y = 12
                elif j.EQUIPE == 3:
                    j.x = 1900
                    j.y = 1000
                elif j.EQUIPE == 4:
                    j.x = 12
                    j.y = 1000
    def afficher(self, fenetre):
        for i in range(4):
            for j in self.lekip[i]:
                j.afficher(fenetre)