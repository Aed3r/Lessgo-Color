from aiohttp import web
import socketHandler
import threading 
from display import *
from constantes import *
from plateau import * 

routes = web.RouteTableDef()

# Prépare les gestionnaires web
async def init_app():
    app = web.Application()

    app['websockets'] = []
    
    app.on_shutdown.append(socketHandler.shutdown)
    app.add_routes(routes)

    return app

# Sert index.html puis prépare le gestionnaire de socket
@routes.get('/')
async def index(request):
    ws_current = web.WebSocketResponse()
    ws_ready = ws_current.can_prepare(request)
    
    if not ws_ready.ok:
        with open('web/index.html') as f:
            return web.Response(text=f.read(), content_type='text/html')
    
    return await socketHandler.request_handler(ws_current, request)

# Sert tous les fichiers javascript demandé
@routes.get('/{file}.js')
async def jsGetHandler(request):
    url = "web/{}.js".format(request.match_info['file'])
    try:
        with open(url) as f:
            return web.Response(text=f.read(), content_type='text/javascript')
    except:
        return web.Response(text="404: '" + url + "' n'existe pas")


class BouclePrincipale(threading.Thread):  
    def __init__(self):  
        threading.Thread.__init__(self)

    def run(self):  
        t = threading.currentThread()
        
        while getattr(t, "do_run", True):
            # Mise à jour des positions joueurs
            moveJoueurs()

            # Mise à jour des cases de couleur
            majCouleurs()

            # Affichage du plateau et des joueurs
            drawAll()

    def majCouleurs():
        for joueur in joueurs :
                terrain.setColor((int) (joueur.x/resolution[0]*terrain.larg), (int) (joueur.y/resolution[1]*terrain.long), joueur.EQUIPE)      

if __name__ == '__main__':
    print("Initialisations...")
    boucle = BouclePrincipale()
    app = init_app()
    boucle.start()
    print("Affichage démarré. Lancement du site...")
    web.run_app(app, port=port)
    boucle.do_run = False
    print("Serveur et affichage arreté. Goodbye")