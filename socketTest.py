from aiohttp import web
import aiohttp

## Creates a new Aiohttp Web Application
app = web.Application()

## aiohttp endpoint
async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws

## We bind our aiohttp endpoint to our app
## router
app.router.add_get('/', index)
app.add_routes([web.get('/ws', websocket_handler)])

## We kick off our server
if __name__ == '__main__':
    web.run_app(app)