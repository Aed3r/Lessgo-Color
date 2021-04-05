from aiohttp import web
import socketHandler
import threading 
import socket
from display import *
from constantes import *
from plateau import * 

#récupère l'adresse ip (classe C)
def get_ip():
    #création d'une socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        # connexion classe A
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

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
        with open('web/index.html') as f:
            return web.Response(text=f.read(), content_type='text/html')
    
    return await socketHandler.request_handler(ws_current, request)

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
            for joueur in joueurs :
                terrain.setColor((int) (joueur.x/resolution[0]*terrain.larg), (int) (joueur.y/resolution[1]*terrain.long), joueur.EQUIPE)   
            # Affichage du plateau et des joueurs
            drawAll()
            # Parcours le terrain et compte le nombre de couleur
            terrain.parcoursCouleur()
            terrain.pourcentageCouleur()
            nb_jaune = terrain.getcj() #pb obligé de créer une variable dans le main
            pourc_jaune = terrain.getpj() 
            print("MAIN || r : ", cr, "b : ", cb, "j : ", nb_jaune, "v : ", cv,)
            print("POUR || r : ", pr, "b : ", pb, "j : ", "%.3f" % pourc_jaune, "v : ", pv,)
            

if __name__ == '__main__':
    print("Initialisations...")
    boucle = BouclePrincipale()
    app = init_app()
    boucle.start() 
    print("Affichage démarré. Lancement du site...")
    print("--- ip : ", get_ip(), " --- ")
    web.run_app(app, port=port)
    print("resolution 0 : ", resolution[0], "resolution 1 : ", resolution[1])
    boucle.do_run = False
    print("Serveur et affichage arreté. Goodbye")