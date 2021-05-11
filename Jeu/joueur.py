#Classe servant a instancier des joueurs

import time
import math
from constantes import *

joueurs = []

# Placements initiaux
global spawn

class Joueur(object): 

    def __init__(self, id, nom, equipe):
        global spawn

        self.rayonCouleur = defRayonCouleur
        self.vitesse = defVitesse
        self.nom = nom
        self.PowerUp = [] # Liste de PowerUp (Tuples contenant le PU et le moment ou il a été appliqué)
        self.score = 0

        # Vecteur direction définie par le joueur
        self.dX = 0
        self.dY = 0

        #definition des constantes
        self.ID = id
        self.EQUIPE = equipe

        #On assigne une couleur au joueur selon son équipe et on le place dans la zone de son équipe
        self.COLOR = couleursJoueurs[equipe]

        # Position
        self.x = spawn[equipe][0]
        self.y = spawn[equipe][1]

        # Utilisé à l'affichage
        self.oldX = self.x
        self.oldY = self.y

        # Vitesse de déplacement
        self.hSpeed = 0
        self.vSpeed = 0
        
        # Dernieres collisions
        self.collisions = set()



    def move(self):
        #On vérifie si on doit enlever un powerup
        for pu in self.PowerUp:
            if(time.time() - pu[1] >= listeValeurs[pu[0]][2]): #Si le powerup est la depuis plus longtemps que ses paramètres le permettent
                self.vitesse -= listeValeurs[pu[0]][0]
                self.rayonCouleur -= listeValeurs[pu[0]][1]
                self.PowerUp.remove(pu)

        if (collisions):
            # Accélération selon l'entrée du joueur
            self.hSpeed += (self.dX * self.vitesse) / 10
            self.vSpeed += (self.dY * self.vitesse) / 10

            # Réduction de la vitesse au cours du temps
            self.hSpeed *= 0.99
            self.vSpeed *= 0.99

            # Cap de vitesse horizontale
            ratio = 1
            if self.hSpeed > vitesseMax * self.vitesse:
                ratio = self.hSpeed / vitesseMax * self.vitesse
            if self.hSpeed < -vitesseMax * self.vitesse:
                ratio = self.hSpeed / -vitesseMax * self.vitesse
            self.hSpeed /= ratio
            self.vSpeed /= ratio

            # Cap de vitesse verticale
            ratio = 1
            if self.vSpeed > vitesseMax * self.vitesse:
                ratio = self.vSpeed / vitesseMax * self.vitesse
            if self.vSpeed < -vitesseMax * self.vitesse:
                ratio = self.vSpeed / -vitesseMax * self.vitesse
            self.hSpeed /= ratio
            self.vSpeed /= ratio
            
            # Application du vecteur déplacement
            self.x += int(self.hSpeed)
            self.y += int(self.vSpeed)
        else:
            self.x = int(self.x + self.dX * self.vitesse)
            self.y = int(self.y + self.dY * self.vitesse)

        rayon = self.getRayon() * tailleCase

        # Vérification de dépassement des bordures
        if (wrapAround):
            if (self.x >= getResP()[0] ): self.x = 1
            if (self.x <= 0): self.x = getResP()[0] - 1
            if (self.y >= getResP()[1] ): self.y = 1
            if (self.y <= 0): self.y = getResP()[1] - 1
        elif (collisions):
            if (self.x+rayon >= getResP()[0] ): 
                self.x = getResP()[0] - rayon - 1
                self.hSpeed *= -1
            if (self.x-rayon < 0): 
                self.x = rayon
                self.hSpeed *= -1
            if (self.y+rayon >= getResP()[1] ): 
                self.y = getResP()[1] - rayon - 1
                self.vSpeed *= -1
            if (self.y-rayon < 0): 
                self.y = rayon
                self.vSpeed *= -1
        else:
            if (self.x+rayon >= getResP()[0] ): self.x = getResP()[0] - rayon - 1
            if (self.x-rayon < 0): self.x = rayon
            if (self.y+rayon >= getResP()[1] ): self.y = getResP()[1] - rayon - 1
            if (self.y-rayon < 0): self.y = rayon

    def setDirection(self, dx, dy):
        self.dX = dx
        self.dY = dy
        
    def getRayon(self):
        return self.nom

    def getPos(self):
        return (round(self.x), round(self.y))

    #Applique les valeurs du powerup Pu, attend la durée du powerup et puis rétabli les valeurs précédentes
    def setPowerUp(self, pu):
        if pu < nbPowerup:
            self.vitesse += listeValeurs[pu][0]
            self.rayonCouleur += listeValeurs[pu][1]
            self.PowerUp.append((pu, time.time()))
        elif pu < nbPowerup + nbSpecial:
            equipePowerUp(pu, self.EQUIPE)
            
    def getPosPourcentage(self):
        return (self.x / getResP()[0], self.y / getResP()[1])

    def getEquipe(self):
        return self.EQUIPE

    def getNom(self):
        return self.nom

    def getCouleur(self):
        return self.COLOR

    def getID (self):
        return self.ID

    # Renvoie une liste descriptive des powerups actifs
    def getPowerups(self):
        pu = list(map(lambda x: x[0], self.PowerUp)) # On récupère les powerup actifs
        puNames = list(map(lambda x: listeValeurs[x][3], pu)) # On remplace par des noms
        return puNames

    # Renvoie le rayon d'affichage du joueur
    def getRayon(self):
        return self.rayonCouleur

    # Renvoie true si le joueur courant et j2 ont été en collision dans le passé
    def haveCollided(self, j2):
        return j2.getID() in self.collisions

    # Enlève j2 des joueurs étant actuellement en collision avec le joueur courant
    def _unsetColliding(self, j2):
        self.collisions.discard(j2.getID())
        j2.collisions.discard(self.getID())
    
    # Ajoute j2 aux joueurs actuellement en collision avec le joueur courant
    def _setColliding(self, j2):
        self.collisions.add(j2.getID())
        j2.collisions.add(self.getID())

    # Vérifie s'il y a eu collision avec j2
    def _areColliding (self, j2):
        return math.sqrt(math.pow(j2.getPos()[0]-self.getPos()[0], 2)+math.pow(j2.getPos()[1]-self.getPos()[1], 2)) <= (j2.getRayon()*tailleCase)+(self.getRayon()*tailleCase)

    # Modifie les déplacemenent du joueur courant et de j2 s'il entre en collision
    def handleCollision (self, j2):
        if self.getID() != j2.getID():
            if self._areColliding(j2): 
                if not self.haveCollided(j2):
                    # Nouveaux vecteurs directions
                    self.hSpeed, j2.hSpeed = j2.hSpeed - self.hSpeed/2, self.hSpeed - j2.hSpeed/2
                    self.vSpeed, j2.vSpeed = j2.vSpeed - self.vSpeed/2, self.vSpeed - j2.vSpeed/2

                    # Séparation
                    self._setColliding(j2)
            else:
                self._unsetColliding(j2)

    # Incrémente le score du joueur de x points
    def increaseScore(self, x):
        self.score += x

    # Renvoie le score du joueur
    def getScore(self):
        return self.score

# Fonction de comparaison entre joueurs. Utile pour le trie
def comparJoueur(j):
    return j.y

# Ajoute le joueur j passé en paramètres et renvoie son numéro
def ajouterJoueur(j):
    global joueurs
    joueurs.append(j)

# Avance tous les joueurs suivant leurs déplacements dX et dY
def moveJoueurs():
    global joueurs
    #joueurs.sort(key=comparJoueur) # Trie les joueurs suivant leurs ordonnées 
    for joueur in joueurs:
        joueur.move()

        if (collisions):
            # On vérifie s'il y a eu collision
            for j2 in joueurs:
                joueur.handleCollision(j2)

# Renvoi la liste de tous les joueurs
def getJoueurs():
    global joueurs
    return joueurs

# Renvoie le joueur indentifié par id
def getJoueur(id):
    global joueurs
    return next(j for j in joueurs if j.getID() == id)

# Renvoi le nombre de joueurs s'ayant connectés
def getNombreJoueurs():
    global joueurs
    return len(joueurs)

# Réinitialise les joueurs
def initJoueurs():
    initSpawnPoints()
    for joueur in joueurs:
        joueur.__init__(joueur.getID(), joueur.getNom(), joueur.getEquipe())

# Applique un powerup a toute l'équipe donnée en paramètre
def equipePowerUp(pu, equipe):
    global joueurs
    for joueur in joueurs:
        if joueur.EQUIPE == equipe:
            joueur.vitesse += listeValeurs[pu][0]
            joueur.rayonCouleur += listeValeurs[pu][1]
            joueur.PowerUp.append((pu, time.time()))

def initSpawnPoints():
    global spawn
    spawnXOffset = getResP()[0] * propZoneInit / 2
    spawnYOffset = getResP()[1] * propZoneInit / 2
    spawn = [(spawnXOffset, spawnYOffset),
            (getResP()[0] - spawnXOffset, spawnYOffset),
            (spawnXOffset, getResP()[1] - spawnYOffset),
            (getResP()[0] - spawnXOffset, getResP()[1] - spawnYOffset)]

initSpawnPoints()