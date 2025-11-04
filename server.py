import socket
import network
import time
file = open("index.html", "r")  # pagina ce va fi livrata 
html = file.read()              # fiser livrat de server
file.close()

wlan = network.WLAN(network.STA_IF) # conectare la router
wlan.active(True)
wlan.connect('DIGI-4Khj','123456789') 
time.sleep(2)

sta_if = network.WLAN(network.STA_IF)
print('Serverul WEB va fi la adresa:\n')
print(sta_if.ifconfig()[0])          # vizualizare IP

ip = socket.getaddrinfo('0.0.0.0', 80)[0][-1] # insusire adresa server
server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ip)                           # 
server.listen(1)                          # server ascultator

while True:
    cl, addr = server.accept()            # identifica IP client
    cl_file = cl.makefile('rwb', 0)       # lecura cerere de la client
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
    trimite = html        # poate include JS +...
    
#   cl.send('Fiser header pentru browser diferit de cel implicit'')
    cl.send(trimite)     # livreaza  index.html 
    cl.close()