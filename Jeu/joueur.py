#Classe servant a instancier des joueurs

from constantes import *

joueurs = []

# Placements initaux
spawnXOffset = resolutionPlateau[0] * propZoneInit / 2
spawnYOffset = resolutionPlateau[1] * propZoneInit / 2
spawn = [(spawnXOffset, spawnYOffset),
         (resolutionPlateau[0] - spawnXOffset, spawnYOffset),
         (spawnXOffset, resolutionPlateau[1] - spawnYOffset),
         (resolutionPlateau[0] - spawnXOffset, resolutionPlateau[1] - spawnYOffset)]

class Joueur(object): 

    def __init__(self, id, nom, equipe):
        super().__init__()
        #Definition des variables
        self.dead = False
        self.dX = 0
        self.dY = 0
        self.rayonCouleur = defRayonCouleur
        self.vitesse = defVitesse
        self.nom = nom

        #definition des constantes
        self.ID = id
        self.EQUIPE = equipe

        #On assigne une couleur au joueur selon son équipe et on le place dans la zone de son équipe
        self.COLOR = couleursJoueurs[equipe]
        self.x = spawn[equipe][0]
        self.y = spawn[equipe][1]

    def move(self):
        # Application du vecteur déplacement
        self.x = int(self.x + self.dX) * self.vitesse
        self.y = int(self.y + self.dY) * self.vitesse

        # Vérification de dépassement des bordures
        if (self.x >= resolutionPlateau[0] ): self.x = 1
        if (self.x <= 0): self.x = resolutionPlateau[0] - 1
        if (self.y >= resolutionPlateau[1] ): self.y = 1
        if (self.y <= 0): self.y = resolutionPlateau[1] - 1

    def isDead(self):
        return self.dead

    def setDead(self, valeur):
        self.dead = valeur

    def setDirection(self, dx, dy):
        self.dX = dx
        self.dY = dy
        
    def getRayon(self):
        return self.nom

    def setPowerUp(self, pu):
        if(pu != neutral & pu <= nbPowerup):
            self.rayonCouleur += listeValeurs[pu][0]
            self.rayonCouleur += listeValeurs[pu][1]
            
    def getPosPourcentage(self):
        return (self.x / resolutionPlateau[0], self.y / resolutionPlateau[1])

    def getEquipe(self):
        return self.EQUIPE

    def getNom(self):
        return self.nom

def comparJoueur(j):
    return j.y

def ajouterJoueur(joueur):
    global joueurs
    joueurs.append(joueur)

def moveJoueurs():
    global joueurs
    #joueurs.sort(key=comparJoueur) # Trie les joueurs suivant leurs ordonnées 
    for joueur in joueurs:
        joueur.move()

def getJoueurs():
    global joueurs
    return joueurs