from aiohttp import web
import aiohttp
import json
import joueur as j

# Liste des addresses IP des joueurs connectés
clients = []

# Attend et répond aux requêtes client
async def request_handler(ws_current, request):
    player = null

    await ws_current.prepare(request)
    request.app['websockets'].append(ws_current)

    # On vérifie si le joueur ne s'est pas connecté auparavant
    if request.remote in clients:
        # On envoie la position initiale du joueur, ainsi que la taille de l'écran
        await ws_current.send_json(({'action': 'init', 'x': j.x, 'y': j.y,
                            'resX': resolutionPlateau[0], 'resY': resolutionPlateau[1]}))
        player = j.getJoueur(request.remote)

    while True:
        if msg.type == aiohttp.WSMsgType.text:
            msg = await ws_current.receive()

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
                await ws_current.send_json(({'action': 'position', 'x': pos[0], 'y': pos[1]}))
            elif data["action"] == "init":
                # On enregistre le nouveau joueur
                player = j.Joueur(request.remote, data["nom"], data["team"])
                j.ajouterJoueur(player)
                clients.append(request.remote)
        else:
            break

    return ws_current

def avertirClients(app):
    for ws in app['websockets']:
        await ws.send_json({'action': 'go'})

# Avertit les clients de la fermeture du serveur
async def shutdown(app):
    print("Fermeture du serveur...")
    for ws in app['websockets']:
        await ws.close()
    app['websockets'].clear()
