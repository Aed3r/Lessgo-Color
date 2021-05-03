from aiohttp import web
import aiohttp
import json
import joueur as j
import time
from constantes import *
import asyncio

# Liste des addresses IP des joueurs connectés
clients = []

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
                                         'resX': resolutionPlateau[0], 'resY': resolutionPlateau[1], 'col': player.getEquipe()})

    while True:
        msg = await ws_current.receive()
        if msg.type == aiohttp.WSMsgType.text:
            data = json.loads(msg.data)

            if data["action"] == None:
                continue

            if data["action"] == "deplacement" and isinstance(data["dx"], int) and isinstance(data["dy"], int):
                # On vérifie que le joueur est initialisé
                if player == None:
                    continue

                # On modifie le déplacement du joueur
                player.setDirection(data["dx"]/10, data["dy"]/10)

                # On renvoie la position actuelle
                pos = player.getPosPourcentage()
                await envoyerPaquet(ws_current, {'action': 'position', 'x': pos[0], 'y': pos[1]})
            elif data["action"] == "init":
                # On enregistre le nouveau joueur
                player = j.Joueur(request.remote, data["nom"], data["team"])
                j.ajouterJoueur(player)
                clients.append(request.remote)
        else:
            break

    return ws_current

# Vérifie que la socket est ouverte puis envoie le paquet
async def envoyerPaquet (websocket, paquet):
    if not websocket.closed:
        await websocket.send_json(paquet)

# Signifie à tous les clients
async def avertirClients(app, msg):
    for ws in app['websockets']:
        await envoyerPaquet(ws, msg)

# Avertit les clients de la fermeture du serveur
async def shutdown(app):
    print("Fermeture du serveur...")
    for ws in app['websockets']:
        await ws.close()
    app['websockets'].clear()