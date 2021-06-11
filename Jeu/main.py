from aiohttp import web
import socketHandler
import threading 
import socket
import os, signal
from constantes import *
import affichageJeu
import plateau
import ecranAttente
import menuPause as mp
import joueur
import asyncio
import finPartie

routes = web.RouteTableDef()
app = None

# Initialise la fenêtre
def initFenetre ():
   
    # Initialisation de la fenêtre                                                                                                                     
    pygame.display.set_caption("LessGo Color")                                                                                 #nom fenetre
    
    if (pleinEcran):
        return pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    else:
        return pygame.display.set_mode(getRes(), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)

fenetre = initFenetre()

# Prépare les gestionnaires web
async def init_app():
    global app
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
        with open('web/introduction.html') as f:
            return web.Response(text=f.read(), content_type='text/html')
    
    return await socketHandler.request_handler(ws_current, request)

# Sert tous les fichiers html demandé
@routes.get('/{file}.html')
async def htmlGetHandler(request):
    url = "web/{}.html".format(request.match_info['file'])
    try:
        with open(url) as f:
            return web.Response(text=f.read(), content_type='text/html')
    except:
        return web.Response(text="404: '" + url + "' n'existe pas")

# Sert tous les fichiers javascript demandé
@routes.get('/{file}.js')
async def jsGetHandler(request):
    url = "web/js/{}.js".format(request.match_info['file'])
    try:
        with open(url) as f:
            return web.Response(text=f.read(), content_type='text/javascript')
    except:
        return web.Response(text="404: '" + url + "' n'existe pas")

# Sert tous les fichiers css demandé
@routes.get('/{file}.css')
async def cssGetHandler(request):
    url = "web/css/{}.css".format(request.match_info['file'])
    try:
        with open(url) as f:
            return web.Response(text=f.read(), content_type='text/css')
    except:
        return web.Response(text="404: '" + url + "' n'existe pas")

# Sert tous les fichiers image demandé
@routes.get('/{file}.png')
async def pngGetHandler(request):
    url = "web/data/{}.png".format(request.match_info['file'])
    try:
        return web.FileResponse(url)
    except:
        return web.Response(text="404: '" + url + "' n'existe pas")

# Sert tous les fichiers json demandé
@routes.get('/{file}.json')
async def jsonGetHandler(request):
    url = "web/data/{}.json".format(request.match_info['file'])
    try:
        return web.FileResponse(url)
    except:
        return web.Response(text="404: '" + url + "' n'existe pas")

nb_jaune = 0 
pourc_jaune = 0

def majCouleurs():
    # Couleurs des cases du terrain + Power ups pour economiser une boucle
    for j in joueur.getJoueurs() :
        text = plateau.updateCase(j)
        if text != None:
            affichageJeu.definirAnnonce(text)

# Boucle s'occupant des gestions de l'affichage, des entrées et du déroulement du jeu
class BouclePrincipale(threading.Thread): 
    def __init__(self):  
        threading.Thread.__init__(self)

    def run(self):  
        global fenetre
        
        t = threading.currentThread()
        altPressed = False
        etatJeu = "attente" # "jeu", "fin"
        pause = False
        cooldownChange = 0
        
        while getattr(t, "do_run", True):
            # Affiche l'écran d'attente
            if etatJeu == "attente":
                ecranAttente.toutDessiner(fenetre)
            elif etatJeu == "fin":
                # Afficher ecran fin de jeu
                finPartie.finPartie(fenetre, joueur.getJoueurs())
            # S'occupe de l'affichage du jeu et de la gestion des joueurs
            elif etatJeu == "jeu":
                if not pause:
                    # Mise à jour des positions joueurs
                    joueur.moveJoueurs()

                    # Mise à jour des cases de couleur
                    majCouleurs()

                # Affichage du plateau et des joueurs
                if affichageJeu.drawAll(fenetre, pause):
                    etatJeu = "fin"
                    terminerJeu()
            
            # Affiche (potentiellement) un menu
            mp.afficherMenu(fenetre)

            # Raffraichissment de la fenêtre
            pygame.display.flip()

            # Gestionnaire des entrées
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Arrête le serveur et l'affichage
                    os.kill(os.getpid(), signal.SIGINT)
                elif event.type == pygame.KEYDOWN:
                    # Alt-F4
                    if event.key == pygame.K_LALT:
                        altPressed = True
                    elif event.key == pygame.K_F4 and altPressed:
                        os.kill(os.getpid(), signal.SIGINT)
                    # Menu pause
                    elif event.key == pygame.K_ESCAPE:
                        pause = mp.toggle(etatJeu)
                    # Modification du cooldown
                    elif event.key == pygame.K_UP and altPressed:
                        cooldownChange = 1
                    elif event.key == pygame.K_DOWN and altPressed:
                        cooldownChange = -1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LALT:
                        altPressed = False
                    elif (event.key == pygame.K_UP or event.key == pygame.K_DOWN) and cooldownChange != 0:
                        avertirClients(avertirClients({'action': 'newCooldown', 'coolDown': socketHandler.getCooldown()}))
                        socketHandler.resetAveragePing()
                        cooldownChange = 0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Gestion des clics dans le menu de pause
                    e = mp.verifClic(event.pos)
                    if e != None:
                        # Un bouton a été appuyé
                        if e == LANCERJEU:
                            # Si le bouton 'lancer jeu' a été appuyé on lance la boucle principale
                            lancerJeu()
                            etatJeu = "jeu"
                            pygame.display.set_mode(getRes(), 0)
                        elif e == QUITTERJEU:
                            # On quitte
                            os.kill(os.getpid(), signal.SIGINT)
                        elif e == REDEMJEU:
                            # On relance le jeu sans passer par le menu d'attente
                            initJeu()
                        elif e == REVATTENTE:
                            # On revient au menu d'attente
                            etatJeu = "attente"
                            pygame.display.set_mode(getRes(), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)

                            # On avertit les clients
                            avertirClients({'action': 'attente'})
                        elif e == INITTIMER:
                            # On remet le timer à zéro sans toucher la partie en cours
                            affichageJeu.initChrono()
                        elif e == FINIRJEU:
                            # On termine la partie prématurément
                            etatJeu = "fin"
                            terminerJeu()
                        # On cache le menu pause
                        mp.toggle(None)
                        pause = False
                elif event.type == pygame.VIDEORESIZE:
                    # Redimmensionnement
                    setRes(event.size)
                    fenetre=pygame.display.set_mode(event.size, pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
                
            if (cooldownChange != 0):
                socketHandler.changeCooldown(cooldownChange)


# Initialise ou réinitialise le jeu
def initJeu():

    # On initialise le terrain
    plateau.initTerrain()

    # On initialise le chrono
    affichageJeu.initChrono()

    # On initialise les joeurs
    joueur.initJoueurs()

# Lance le jeu "correctement", cad en venant de l'écran d'attente
def lancerJeu():
    # On initialise le jeu
    initJeu()

    # On avertit les clients
    avertirClients({'action': 'go'})

# Envoie un message à tous les clients
def avertirClients(msg):
    global app
    coroutine = socketHandler.avertirClients(app, msg)
    asyncio.run(coroutine)

# Avertit les clients de la fin du jeu
def terminerJeu():
    maxV = 0
    maxI = -1
    i = 0
    for p in plateau.getTerrain().pourcentageCouleur():
        if p > maxV:
            maxV = p
            maxI = i
        i += 1
    avertirClients({'action': 'fin', 'winner': maxI})

if __name__ == '__main__':
    print("Initialisations...")
    boucle = BouclePrincipale()
    app = init_app()
    boucle.start() 
    print("Résolution : ", getRes())
    print("Affichage démarré. Lancement du site...")
    web.run_app(app, port=port)
    boucle.do_run = False
    print("Serveur et affichage arreté. Goodbye")
