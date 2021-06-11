from aiohttp import web
import aiohttp
import json

nb_connections = 0

async def init_app():

    app = web.Application()

    app['websockets'] = {}

    app.on_shutdown.append(shutdown)

    app.router.add_get('/', index)

    return app

async def shutdown(app):
    for ws in app['websockets'].values():
        await ws.close()
    app['websockets'].clear()

async def index(request):
    ws_current = web.WebSocketResponse()
    ws_ready = ws_current.can_prepare(request)
    
    if not ws_ready.ok:
        with open('indexVieux.html') as f:
            return web.Response(text=f.read(), content_type='text/html')
    
    global nb_connections
    nb_connections += 1
    num_connection = nb_connections

    print ("[" + str(num_connection) + "] Nouvelle connexion. Ouverture du websocket...");

    await ws_current.prepare(request)
    print ("[" + str(num_connection) + "] Websocket ouvert. Envoi du paquet initial...");

    x = 0
    y = 0

    #for ws in request.app['websockets'].values():
    #    await ws.send_json({'action': 'join', 'name': name})
    #request.app['websockets'][name] = ws_current

    await ws_current.send_json(({'action': 'position', 'x': x, 'y': y}))

    print ("[" + str(num_connection) + "] Paquet envoyé. Attente de réponses...")

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

if __name__ == '__main__':
    app = init_app()
    web.run_app(app)