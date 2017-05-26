PiRobot
=======

Bienvenue sur le projet PiRObot !

Ce projet à pour objectif la fabrication d'un robot mobile, capable de voir, entendre, 
et pourquoi pas, d'interragir avec son environnement ...

Matériel utilisé :
------------------

* RaspberryPi3 avec sa carteSD, box, alim, clavier, souris, etc... :
-> https://www.amazon.fr/gp/product/B01CD5VC92/ref=oh_aui_detailpage_o06_s00?ie=UTF8&psc=1
-> https://www.amazon.fr/gp/product/B003WIRFDM/ref=oh_aui_detailpage_o05_s00?ie=UTF8&psc=1
-> https://www.amazon.fr/gp/product/B01DDFFOYK/ref=oh_aui_detailpage_o06_s01?ie=UTF8&psc=1

* Carte d'extention Batterie pour rendre le Rpi autonome en alim :
-> https://www.amazon.fr/gp/product/B06VVMHPFR/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1 

* Caméra IR-Cut :
-> https://www.amazon.fr/gp/product/B06XTKVPZN/ref=oh_aui_detailpage_o02_s00?ie=UTF8&psc=1

* DongleUSB Wifi (afin d'avoir une connexion Internet si la première interfacte wifi est en point d'acces) :

* Kit apprentissage bien utile, quelques capteurs intéressants :
-> https://www.amazon.fr/gp/product/B01N0TKCJN/ref=oh_aui_detailpage_o02_s01?ie=UTF8&psc=1

* L298N Double pont H DC Driver :
-> https://www.amazon.fr/gp/product/B071RN2NNK/ref=oh_aui_detailpage_o00_s00?ie=UTF8&psc=1

* Chassis TYCO Rebound (batterie HS, peut importe il faudra trouver une alternative):
-> http://www.ebay.com/bhp/tyco-rebound

* un smartphone, tablette.


Utilitaires Windows sur le PC :
-------------------------------
 
-> SDFormater (formatage carte SD : options = erase et resize ON) 

-> Etcher (écriture image sur la carteSD)

-> Putty (SSH client)


Installation Logicielle :
--------------------------

* Raspbian Jessie (impérativement la même version si vous utilisez l'écran 3.5 pouces...):

-> RASPBIAN JESSIE WITH PIXEL Image with PIXEL desktop based on Debian Jessie
   Version:April 2017; Release date:2017-04-10; Kernel version:4.4

-> Installation classique (NE PAS MAJ avec apt-get update / upgrade si vous utilisez l'écran 3.5 pouces !)



Installer la Caméra :
---------------------

Déballez et montez la caméra avec ses diodes IR, branchez la au Raspberry à l'aide de la nappe fournie.

Activez la caméra via votre écran ou par la console :
(si vous n'avez pas encore installé Puttyn il est grand temps !)

```
sudo raspi-config
```

et activez la caméra, rebootez.

Nous allons avoir besoin de streamer la vidéo vers une interface web, pour cela nous utiliserons Mjpg-streamer
(https://github.com/jacksonliam/mjpg-streamer)

```
sudo apt-get install cmake libjpeg8-dev
cd mjpg-streamer-experimental
make
sudo make install
```

Pour lancer la vidéo :

```
cd mjpg-streamer/mjpg-streamer-experimental
export LD_LIBRARY_PATH=.
./mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so"
```

Vous pouvez accéder à la page qui hébèrge votre vidéo à l'adresse <IP du Raspberry>:8080

Ctrl+C pour stopper la vidéo.

Afin de pouvoir démarrer le service en une seule ligne de commande :

Pour déplacer le dossier d'installation :

````
sudo cp mjpg_streamer /usr/local/bin
sudo cp output_http.so input_file.so input_uvc.so /usr/local/lib/
sudo cp -R www /usr/local/www
```

Et Afin de pouvoir démarrer le service en une seule ligne de commande :

```
sudo nano /etc/init.d/livestream.sh
```

Copiez tout ce contenu :

```
#!/bin/sh
# /etc/init.d/livestream.sh
### BEGIN INIT INFO
# Provides:          livestream.sh
# Required-Start:    $network
# Required-Stop:     $network
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: mjpg_streamer for webcam
# Description:       Streams /dev/video0 to http://IP/?action=stream
### END INIT INFO
f_message(){
        echo "[+] $1"
}

# Carry out specific functions when asked to by the system
case "$1" in
        start)
                f_message "Starting mjpg_streamer"
                /usr/local/bin/mjpg_streamer -b -i "/usr/local/lib/?????/input_raspicam.so -r 1280x720" -o "/usr/local/lib/output_http.so -w /usr/local/www -c username:password"
                sleep 2
                f_message "mjpg_streamer started"
                ;;
        stop)
                f_message "Stopping mjpg_streamer…"
                killall mjpg_streamer
                f_message "mjpg_streamer stopped"
                ;;
        restart)
                f_message "Restarting daemon: mjpg_streamer"
                killall mjpg_streamer
                /usr/local/bin/mjpg_streamer -b -i "/usr/local/lib/?????/input_raspicam.so -r 1280x720" -o "/usr/local/lib/output_http.so -w /usr/local/www -c username:password"
                sleep 2
                f_message "Restarted daemon: mjpg_streamer"
                ;;
        status)
                pid=`ps -A | grep mjpg_streamer | grep -v "grep" | grep -v mjpg_streamer. | awk ‘{print $1}’ | head -n 1`
                if [ -n "$pid" ];
                then
                        f_message "mjpg_streamer is running with pid ${pid}"
                        f_message "mjpg_streamer was started with the following command line"
                        cat /proc/${pid}/cmdline ; echo ""
                else
                        f_message "Could not find mjpg_streamer running"
                fi
                ;;
        *)
                f_message "Usage: $0 {start|stop|status|restart}"
                exit 1
                ;;
esac
exit 0
```

et enfin :

```
sudo chmod 755 /etc/init.d/livestream.sh

sudo update-rc.d livestream.sh defaults
```

La dernière commande ajoute mjpg-streamer au Boot.

Pour gérer le service :

```
sudo service livestream.sh start
sudo service livestream.sh stop
sudo service livestream.sh restart
```



Installer un Dongle Wifi :
--------------------------

Le but de cette opération est de rendre le robot utilisable en conditions connectée et déconnectée.

L'interface wlan0 sera le point d'accès pour le smartphone qui va piloter le tout.
L'interface supplémentaire (dongle) wlan1 sera l'accès Internet.

Avant tout branchez le dongle, attribuez lui une IP fixe dans votre Box et routez le port TCP 8000 dessus.
Dans mon exemple 192.168.0.14

nous allons maintenant configurer l'interface wlan0 :

D'abbord une IP statique :

```
 sudo nano /etc/network/interfaces
```

Commentez (# au début de la ligne) toutes les lignes mentionnant wlan0 et wpa
à l'exception de "allow hotplug wlan0" 
et ajoutez ces lignes au bas du fichier :

iface wlan0 inet static
address 192.168.3.1
netmask 255.255.255.0

Redémarrez

Installation du serveur DHCP :

```
sudo apt-get install isc-dhcp-server

# ignorez les éventuelles erreurs, puis

sudo nano /etc/dhcp/dhcpd.conf
```

Commentez (#) les lignes faisant mention de "option domain-name"

#option domain-name "example.org";
#option domain-name-servers ns1.example.org, ns2.example.org;

Dé-commentez (enlever #) "authoritative;"

#If this DHCP server is the official DHCP server for the local
#network, the authoritative directive should be uncommented.
authoritative;

Et enfin, en bas du fichier, ajoutez :

subnet 192.168.3.0 netmask 255.255.255.0 {
range 192.168.3.10 192.168.3.50;
option broadcast-address 192.168.3.255;
option routers 192.168.3.1;
default-lease-time 600;
max-lease-time 7200;
option domain-name "local";
option domain-name-servers 8.8.8.8, 8.8.4.4;
}

Sauvegardez (Ctrl + X) et quittez (o, entrée)

Faites de l'interface wlan0 l'interface par défaut sur serveur DHCP :

```
sudo nano /etc/default/isc-dhcp-server
```

Changez INTERFACES="" en "NTERFACES="wlan0"

Sauvez, Quittez.

Relancez le serveur DHCP :

```
sudo service isc-dhcp-server restart
```

Installer et configurer Hostpad

```
sudo apt-get install hostapd

sudo nano /etc/hostapd/hostapd.conf
```

Ajoutez les lignes suivantes en bas du fichier :

interface=wlan0
driver=nl80211
ssid=PiRobot
hw_mode=g
channel=6
beacon_int=100
dtim_period=2
max_num_sta=40
rts_threshold=2347
fragm_threshold=2346
auth_algs=1
wpa=1
wpa_passphrase=raspberry
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP

Dire à Hostpad ou se trouve ce fichier conf :

```
sudo nano /etc/default/hostapd
```

Décommentez et modifier la ligne suivante (ajout adresse fichier.conf) :

DAEMON_CONF="/etc/hostapd/hostapd.conf"

Maintenant nous devons configurer le routage entre nos deux interfaces wifi :

```
sudo nano /etc/sysctl.conf
```

Décommentez si nécéssaire la ligne "net.ipv4.ip_forward=1"

Quittez et lancez la commande suivante pour activer le forwarding :

```
sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
```

et entrez les commandes suivantes dans la console : 

```
sudo iptables -t nat -A POSTROUTING -o wlan1 -j MASQUERADE
sudo iptables -A FORWARD -i wlan1 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o wlan1 -j ACCEPT
```
sauvegarder avec :

```
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
```

nous modifions une dernière fois le fichier "interfaces" :

```
sudo nano /etc/network/interfaces
```

ajoutez la ligne à la fin :

pre-up iptables-restore < /etc/iptables.ipv4.nat

Pour finir nous allons installer dnsmasq afin de pouvoir utiliser les ports en mode déconnecté
et modifier son fichier de config :

```
sudo apt-get install dnsmasq

sudo nano /etc/dnsmasq.conf
```
ajouter à la fin :

#Pi3Hotspot Config
#stop DNSmasq from using resolv.conf
no-resolv
#Interface to use
interface=wlan0
bind-interfaces
dhcp-range=192.168.3.10,192.168.3.50,12h

Sauvez (Ctrl + X) et quittez (o et entrée)

redémarrez (sudo reboot)

Tester avec et sans connexion, vous devriez garder accès à votre raspberry avec et sans le dongle sur 192.168.3.1
Avec le dongle vous pouvez y accéder sur son IP locale ou Publique, les forwardings (type :8000 ou :8080) fonctionnent.



Installer WebIOPi :
-------------------

WebIOPi est un utilitaire qui va permettre à une page web hébergée sur le raspberry de communiquer avec un script Python.
Cela va nous permettre de créer notre interface et controler des ports GPIO.

Commencez par installer WiringPi :

```
git clone git://git.drogon.net/wiringPi
cd ~/wiringPi
git pull origin
./build
```


Puis WebIOPi :
(https://github.com/doublebind/raspi)

```
wget http://sourceforge.net/projects/webiopi/files/WebIOPi-0.7.1.tar.gz
tar xvzf WebIOPi-0.7.1.tar.gz
cd WebIOPi-0.7.1
wget https://raw.githubusercontent.com/doublebind/raspi/master/webiopi-pi2bplus.patch
patch -p1 -i webiopi-pi2bplus.patch
sudo ./setup.sh
cd /etc/systemd/system/
sudo wget https://raw.githubusercontent.com/doublebind/raspi/master/webiopi.service
sudo systemctl start webiopi
sudo systemctl enable webiopi
```

WebIOPi est à présent installé et fonctionnel, essayez de vous rendre sur <ip du raspberry>:8000
Vous devriez tomber sur une interface listant vos ports Gpio (par défaut : user = webiopi, pass = raspberry).

Ajouter cette balise dans le Head de index.html : <meta name="mobile-web-app-capable" content="yes">

Afin de controller les moteurs, nous allons utiliser un L298N Double pont H DC Driver.
Il faudra lui envoyer les infos de pilotage de moteurs sur 4 fils (2 moteurs, marche avant et marche arrière).

Le signal envoyé sera de type PWM (Pulse With Modulation) de sorte que chaque pin/cable controle une direction par moteur, 
avec modulation de la tention appliquée au moteur selon l'input des joystics.

Après avoir longtemps galéré avec Webiopi et le Python (faire passer une variable numérique du javascript au python semble 
compliqué...), j'ai finalement compris qu'il était possible de tout faire depuis le Javascript intégré dans la page Html
(même gerer les pins en PWM !!)

A ce stade, la vidéo, les photos et l'IR fonctionnent via macro dans le script python et tout le pilotage moteur dans le Javascript...
Tout fonctionne...




