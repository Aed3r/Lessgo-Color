from aiohttp import web
import aiohttp
import json

nb_connections = 0

# Attend et répond aux requêtes client
async def request_handler(ws_current, request):
    global nb_connections
    nb_connections += 1
    num_connection = nb_connections

    x = 0
    y = 0

    print ("[" + str(num_connection) + "] Nouvelle connexion. Ouverture du websocket...");
    await ws_current.prepare(request)
    print ("[" + str(num_connection) + "] Websocket ouvert. Envoi du paquet initial...");

    #for ws in request.app['websockets'].values():
    #    await ws.send_json({'action': 'join', 'name': name})
    request.app['websockets'].append(ws_current)
    print(request.app['websockets'])

    await ws_current.send_json(({'action': 'position', 'x': x, 'y': y}))

    print ("[" + str(num_connection) + "] Paquet envoyé. Attente de requêtes...")

    while True:
        msg = await ws_current.receive();

        if msg.type == aiohttp.WSMsgType.text:
            print ("[" + str(num_connection) + "] Paquet reçu: " + msg.data)
            data = json.loads(msg.data)
            x += data["offX"];
            y += data["offY"];
            print ("[" + str(num_connection) + "] Envoi de la position: (" + str(x) + ", " + str(y) + ")")
            await ws_current.send_json(({'action': 'position', 'x': x, 'y': y}))
        else:
            break
    
    return ws_current

# Avertit les clients de la fermeture du serveur
async def shutdown(app):
    print("Fermeture du serveur.")
    for ws in app['websockets']:
        await ws.close()
    app['websockets'].clear()