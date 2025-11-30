import socket
import network
import machine

# --- Configuration du point d'accès WiFi ---
nom_wifi = "PicoW_DaBe"
mot_de_passe = "123456789"

# connection au pin de la led du pico
del_led = machine.Pin("LED", machine.Pin.OUT)
del_led.off()   # commencer ÉTEINT
etat_del = False   # suivre l'état actuel

# creation et configuration du reseau wifi: ap
ap = network.WLAN(network.AP_IF)
ap.config(essid=nom_wifi, password=mot_de_passe)
ap.active(True)

while not ap.active():
    pass

# affiche les information du reseau
print("Point d'accès actif")
print(ap.ifconfig()) 

# --- Génération de page HTML ---
def page_html(etat):
    return f"""<!DOCTYPE html>
<html>
<head>
    <title>Contrôle de la DEL – Pico W</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="text-align:center; font-family:sans-serif; margin-top:50px;">
    <h1 style="font-size:50px;">Contrôle de la DEL – Pico W</h1>
    <p style="font-size:40px;">DEL actuellement : <b>{etat}</b></p>
    <form action="/" method="get">
        <button name="del" value="on" type="submit" style="font-size:40px; padding:20px 50px;">ALLUMER</button>
        <button name="del" value="off" type="submit" style="font-size:40px; padding:20px 50px;">ÉTEINDRE</button>
    </form>
</body>
</html>
"""

# --- Configuration du serveur socket ---
adresse = socket.getaddrinfo("0.0.0.0", 8080)[0][-1]
serveur = socket.socket()
serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serveur.bind(adresse)
serveur.listen(1)

print("Serveur en écoute sur", adresse)

# --- Boucle principale ---
while True:
    client, adresse_client = serveur.accept()
    requete = client.recv(1024).decode()
    print("Requête:", requete)

    # --- Analyse du paramètre GET ---
    if "del=on" in requete:
        del_led.on()
        etat_del = True
        print("LED ALLUMÉE")
    elif "del=off" in requete:
        del_led.off()
        etat_del = False
        print("LED ÉTEINTE")
    else:
        print("*** Requête inattendue ***")

    # --- Envoi de la page HTML ---
    page = page_html("ALLUMÉE" if etat_del else "ÉTEINTE")
    client.send("HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n")
    client.send(page.encode("utf-8"))
    client.close()


