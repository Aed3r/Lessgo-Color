from aiohttp import web
import aiohttp
import json
from joueur import *

nb_connections = 0

# Attend et répond aux requêtes client
async def request_handler(ws_current, request):
    global nb_connections
    global joueurs

    nb_connections += 1
    num_connection = nb_connections

    j = Joueur(num_connection, "Placeholder #" + str(num_connection), (nb_connections-1)%4)
    ajouterJoueur(j)

    print ("[" + str(num_connection) + "] Nouvelle connexion", end="... ")
    await ws_current.prepare(request)

    #for ws in request.app['websockets'].values():
    #    await ws.send_json({'action': 'join', 'name': name})
    request.app['websockets'].append(ws_current)

    await ws_current.send_json(({'action': 'init', 'x': j.x, 'y': j.y, 
                                 'resX': resolutionPlateau[0], 'resY': resolutionPlateau[1]}))
    print("Initialisation réussi.")

    while True:
        msg = await ws_current.receive();

        if msg.type == aiohttp.WSMsgType.text:
            data = json.loads(msg.data)

            j.setDirection(data["dx"]/10, data["dy"]/10)

            pos = j.getPosPourcentage()
            await ws_current.send_json(({'action': 'position', 'x': pos[0], 'y': pos[1]}))
        else:
            break
    
    return ws_current

# Avertit les clients de la fermeture du serveur
async def shutdown(app):
    print("Fermeture du serveur.")
    for ws in app['websockets']:
        await ws.close()
    app['websockets'].clear()
