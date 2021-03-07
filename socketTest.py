# examples/server_simple.py
from aiohttp import web

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
        with open('index.html') as f:
            return web.Response(text=f.read(), content_type='text/html')

    await ws_current.prepare(request)

    name = get_random_name()
    log.info('%s joined.', name)

    await ws_current.send_json({'action': 'connect', 'name': name})

    for ws in request.app['websockets'].values():
        await ws.send_json({'action': 'join', 'name': name})
    request.app['websockets'][name] = ws_current

    while True:
        msg = await ws_current.receive()

        if msg.type == aiohttp.WSMsgType.text:
            for ws in request.app['websockets'].values():
                if ws is not ws_current:
                    await ws.send_json(
                        {'action': 'sent', 'name': name, 'text': msg.data})
        else:
            break
    
    del request.app['websockets'][name]
    log.info('%s disconnected.', name)
    for ws in request.app['websockets'].values():
        await ws.send_json({'action': 'disconnect', 'name': name})
    
    return ws_current

if __name__ == '__main__':
    app = init_app()
    web.run_app(app)