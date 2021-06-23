from aiohttp import web
import aiohttp
import json
import joueur as j
import time
import constantes as cst
import asyncio
import random
import threading

# Liste des addresses IP des joueurs connectés
clients = set()

# Cooldown des joueurs
msCooldown = cst.defaultCooldown

# Ping moyen
avgPing = -1
nPings = 0
mutex = threading.Lock()

# Attend et répond aux requêtes client
# Une fonction par client
async def request_handler(ws_current, request):
    player = None

    await ws_current.prepare(request)
    request.app['websockets'].append(ws_current)

    # On vérifie si le joueur ne s'est pas connecté auparavant
    # Au début du jeu les données du joueur sont également partagé ici
    if request.remote in clients:
        # On envoie la position initiale du joueur, ainsi que la taille de l'écran
        player = j.getJoueur(request.remote)
        await envoyerPaquet(ws_current, {'action': 'init', 'x': player.getPos()[0], 'y': player.getPos()[1],
                                         'resX': cst.getResP()[0], 'resY': cst.getResP()[1], 'team': player.getEquipe(),
                                         'color': cst.couleursPlateau[player.getEquipe()], 'coolDown': msCooldown,
                                         'nom': player.getNom(), 'score': player.getScore()})

    while True:
        msg = await ws_current.receive()
        if msg.type == aiohttp.WSMsgType.text:
            try:
                data = json.loads(msg.data)

                if data["action"] == None:
                    continue

                if data["action"] == "deplacement" and isinstance(data["dx"], int) and isinstance(data["dy"], int):
                    # On vérifie que le joueur est initialisé
                    if player == None:
                        continue

                    # On calcule le ping moyen
                    calcPingMoyen(data["ping"])

                    # On modifie le déplacement du joueur
                    player.setDirection(data["dx"]/10, data["dy"]/10)

                    # On renvoie la position et le powerup actuel
                    pos = player.getPosPourcentage()
                    await envoyerPaquet(ws_current, {'action': 'update', 'x': pos[0], 'y': pos[1], 'pu': player.getPowerups()})
                elif data["action"] == "init":
                    # On enregistre le nouveau joueur
                    if player is None:
                        player = j.Joueur(request.remote, data["nom"], data["team"])
                        j.ajouterJoueur(player)
                        clients.add(request.remote)
                    else:
                        player.init(data["nom"], data["team"])
                        player.setStillPlaying(True)

                    # On envoie le cooldown actuel
                    await envoyerPaquet(ws_current, {'action': 'newCooldown', 'coolDown': msCooldown})

                    # Si le jeu est lancé on demande au client de charger la manette
                    if cst.jeuLance:
                        await envoyerPaquet(ws_current, {'action': 'go'})
                elif data["action"] == "stresstest":
                    # On calcule le ping moyen
                    calcPingMoyen(data["ping"])

                    # On renvoie une réponse aléatoire
                    val1 = random.randint(0, 100000)
                    val2 = random.randint(0, 100000)

                    await envoyerPaquet(ws_current, {'action': 'stresstest', 'val1': val1, 'val2': val2})
            except:
                alert("Mauvais paquet '" + msg.data + "' du joueur '" + str(request.remote) + "'")
        else:
            break

    return ws_current

# Affiche le message msg dans le terminal en couleur rouge
def alert(msg):
    print("\033[A\033[A\033[31m" + msg + "\033[39m\n\n")
    changeCooldown(0)

# Calcule et affiche le nouveau piong ainsi que la moyenne des pings précédents
def calcPingMoyen (newPing):
    global avgPing, nPings, mutex

    mutex.acquire()
    if (newPing != -1): 
        nPings += 1
        avgPing += (newPing - avgPing) / nPings

        # On affiche le résultat
        if (nPings == 1):
            print("cooldown: " + str(msCooldown) + "ms\nsheeeeesh")
        print("\033[Aping: " + str(newPing) + "ms avg: " + str(round(avgPing)) + "ms                 ")
    mutex.release()

# Vérifie que la socket est ouverte puis envoie le paquet
async def envoyerPaquet (websocket, paquet):
    if not websocket.closed:
        try:
            await websocket.send_json(paquet)
        except Exception:
            return

# Envoie à tous les clients le paquet msg
async def avertirClients(app, msg):
    for ws in app['websockets']:
        await envoyerPaquet(ws, msg)

# Effectue le changement de cooldown définie par change
def changeCooldown(change):
    global msCooldown
    msCooldown += change

    if (msCooldown < 0):
        msCooldown = 0
    
    print("\033[A\033[Acooldown: " + str(msCooldown) + "ms                          \n")

    return msCooldown

# Remet le ping moyen à 0. A utiliser après changement du cooldown
def resetAveragePing():
    global mutex, avgPing, nPings
    mutex.acquire()
    avgPing = -1
    nPings = 0
    mutex.release()
    print("\033[A\033[A\033[A")

def getCooldown():
    return msCooldown

# Avertit les clients de la fermeture du serveur
async def shutdown(app):
    print("Fermeture du serveur...")
    for ws in app['websockets']:
        await ws.close()
    app['websockets'].clear()