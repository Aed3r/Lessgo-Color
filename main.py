from aiohttp import web
import socketHandler

# Prépare les gestionnaires web
async def init_app():
    app = web.Application()

    app['websockets'] = []
    
    app.on_shutdown.append(socketHandler.shutdown)
    app.router.add_get('/', index)

    return app

# Sert index.html puis prépare le gestionnaire de socket
async def index(request):
    ws_current = web.WebSocketResponse()
    ws_ready = ws_current.can_prepare(request)
    
    if not ws_ready.ok:
        with open('index.html') as f:
            return web.Response(text=f.read(), content_type='text/html')
    
    return await socketHandler.request_handler(ws_current, request)

if __name__ == '__main__':
    app = init_app()
    web.run_app(app, host='127.0.0.1', port=80)