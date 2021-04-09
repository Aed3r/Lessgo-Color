from aiohttp import web
import socketHandler
import threading 
import socket
import os, signal
from constantes import *
import affichageJeu
from plateau import * 
import ecranAttente
import UI.menuPause as mp
import joueur

routes = web.RouteTableDef()

# Initialise la fenêtre
def initFenetre ():
    global resolution 
    
    # Initialisation de la fenêtre                                                                                                                     
    pygame.display.set_caption("SPLAT_PGMOT")                                                                                 #nom fenetre
        
    return pygame.display.set_mode(resolution, pygame.FULLSCREEN if pleinEcran else pygame.RESIZABLE)

fenetre = initFenetre()

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

nb_jaune = 0 
pourc_jaune = 0

def majCouleurs():
    # Couleurs des cases du terrain
    for j in joueur.getJoueurs() :
            terrain.modifCompteur(j.x,j.y,j.EQUIPE)
            terrain.setColor((int) (j.x/resolutionPlateau[0]*terrain.larg), (int) (j.y/resolutionPlateau[1]*terrain.long), j.EQUIPE) 
            
    
    # Parcours le terrain et compte le nombre de couleur
        #terrain.pourcentageCouleur() calcul les pourcentages
        # exemple récupération compteur/pourcentage
            # nb_jaune = terrain.getcj() 
            #pourc_jaune = terrain.getpj() 

# Boucle lancé initialement en attendant les joueurs
class BoucleAttente(threading.Thread): 
    def __init__(self):  
        threading.Thread.__init__(self)

    def run(self):  
        ecranAttente.initValeurs()
        t = threading.currentThread()
        altPressed = False
        jeuLance = False
        
        while getattr(t, "do_run", True):
            # S'occupe de l'affichage du jeu et de la gestion des joueurs
            if jeuLance:
                # Mise à jour des positions joueurs
                joueur.moveJoueurs()

                # Mise à jour des cases de couleur
                majCouleurs()

                # Affichage du plateau et des joueurs
                affichageJeu.drawAll(fenetre)
            # Affiche l'écran d'attente
            else:
                ecranAttente.toutDessiner(fenetre)

            # Affiche (potentiellement) un menu
            mp.afficherMenu(fenetre)

            # Raffraichissment de la fenêtre
            pygame.display.flip()

            # Ferme le jeu si le bouton 'fermé' ou alt+F4 sont appuyé
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Arrête le serveur et l'affichage
                    os.kill(os.getpid(), signal.SIGINT)
                elif event.type == pygame.KEYDOWN:
                    # Alt-F4
                    if event.mod == pygame.KMOD_ALT:
                        altPressed = True
                        print("alt pressed")
                    if event.key == pygame.K_F4 and altPressed:
                        os.kill(os.getpid(), signal.SIGINT)
                    elif event.key == pygame.K_ESCAPE:
                        # Menu pause
                        if not jeuLance:
                            mp.toggleAttente(policeTitres)
                elif event.type == pygame.KEYUP:
                    if event.mod == pygame.KMOD_ALT:
                        altPressed = False
                        print("alt let go")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Si le bouton 'lancer jeu' a été appuyé on lance la boucle principale
                    if not jeuLance and mp.verifClic(event.pos) != None:
                        # On cache le menu de l'écran d'attente
                        mp.toggleAttente(None)

                        # On lance le jeu
                        jeuLance = True


if __name__ == '__main__':
    print("Initialisations...")
    boucle = BoucleAttente()
    app = init_app()
    boucle.start() 
    print("Résolution : ", resolution)
    print("Affichage démarré. Lancement du site...")
    web.run_app(app, port=port)
    boucle.do_run = False
    print("Serveur et affichage arreté. Goodbye")