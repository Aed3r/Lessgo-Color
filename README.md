```
 _                                 ____      _            
| |    ___  ___ ___  __ _  ___    / ___|___ | | ___  _ __ 
| |   / _ \/ __/ __|/ _` |/ _ \  | |   / _ \| |/ _ \| '__|
| |__|  __/\__ \__ \ (_| | (_) | | |__| (_) | | (_) | |   
|_____\___||___/___/\__, |\___/   \____\___/|_|\___/|_|   
                    |___/                               
```
# What is this project ?
Lessgo Color is a third year University project made by :
 - Gustav Hubert
 - Osman Simsek
 - Paul-Antoine Bernard
 - Marwan Ait Addi
 - Thomas vendeville

The objective was to create a game that was playable by a large number of player (40 to 50 players) on the same screen
and to then host a game night in a cinema to have people come and play our games.

# What technologies have been used ?
We used python 3.8.5 for the server and the html/css/js stack for client side interactions,
the connection between the client and the server is handled by a high efficiency router, 
we used WebSockets via the AIOHTTP package to handle server-client interactions and 
Pygame to display things on the screen, everything else is scratch built using only the standard
libraries.

# How can i try it ?
Simply clone the source code into a folder and run the following command : `./jeu.sh`
it will run a bash script that will put you in the correct folder and run the main.py
if you can't run bash scripts on you operating system then got to the `Jeu` folder and run
the main.py file with python3.