from aiohttp import web
import socketHandler
import threading 
import socket
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

def majCouleurs():
    # Couleurs des cases du terrain
    for joueur in joueurs :
            terrain.setColor((int) (joueur.x/resolutionPlateau[0]*terrain.larg), (int) (joueur.y/resolutionPlateau[1]*terrain.long), joueur.EQUIPE) 
            print("joueur x : ", joueur.x, "joueur y : ", joueur.y)
            #terrain.modifCompteur(joueur.x,joueur.y,joueur.EQUIPE)
    
    # Parcours le terrain et compte le nombre de couleur
    #terrain.parcoursCouleur()
    #terrain.pourcentageCouleur()
    nb_jaune = terrain.getcj() #pb obligé de créer une variable dans le main
    pourc_jaune = terrain.getpj() 
    #print("MAIN || r : ", cr, "b : ", cb, "j : ", nb_jaune, "v : ", cv,)
    #print("POUR || r : ", pr, "b : ", pb, "j : ", "%.3f" % pourc_jaune, "v : ", pv)

class BouclePrincipale(threading.Thread): 
    nb_jaune = 0 
    pourc_jaune = 0
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


if __name__ == '__main__':
    print("Initialisations...")
    boucle = BouclePrincipale()
    app = init_app()
    boucle.start() 
    print("Affichage démarré. Lancement du site...")
    web.run_app(app, port=port)
    print("resolution 0 : ", resolution[0], "resolution 1 : ", resolution[1])
    boucle.do_run = False
    print("Serveur et affichage arreté. Goodbye")