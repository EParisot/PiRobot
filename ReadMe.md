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

* Ecran 3.5 pouces LCD TFT (optionel) :
-> https://www.amazon.fr/gp/product/B06X191RX7/ref=oh_aui_detailpage_o02_s00?ie=UTF8&psc=1

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

Installer l'écran :
-------------------

(https://github.com/goodtft/LCD-show/blob/master/README.md)

```
git clone https://github.com/goodtft/LCD-show.git
chmod -R 755 LCD-show

# Pour configurer l'affichage sur l'écran 3.5 pouces :
cd LCD-show/
sudo ./LCD35-show

# A l'avenir, pour revenir à l'affichage HDMI :
cd LCD-show/
sudo ./LCD-hdmi
```

Le système redémarre, l'écran devrait afficher à l'horizontale après quelques secondes...
La zone tactile elle n'est pas encore étalonnée et surtout les axes sont inversés...

```
cd LCD-show
sudo dpkg -i -B xserver-xorg-input-evdev_1%3a2.10.3-1_armhf.deb
sudo cp -rf /usr/share/X11/xorg.conf.d/10-evdev.conf /usr/share/X11/xorg.conf.d/45-evdev.conf
sudo reboot
```

Tout devrait maintenant fonctionner, à vous de régler l'ecran selon vos besoins, je reste à l'horizontale...

Reste à étalonner l'ecran :

```
sudo apt-get install -y xinput-calibrator
sudo DISPLAY=:0.0 xinput_calibrator
```

Avec un stylet, touchez le centre des croix indiquées à l'écran
A la fin, vous devriez obtenir ce type de données à l'écran :

Doing dynamic recalibration:
Setting new calibration data: 3919, 208, 236, 3913 (valeurs indicatives)

Nous allons devoir copier ces données dans le fichier 99-calibration.conf :

```
sudo nano /etc/X11/xorg.conf.d/99-calibration.conf
```

Les valeurs à modifier apparaissent :

Section "InputClass"
Identifier	"calibration"
MatchProduct	"ADS7846 Touchscreen"
Option	"Calibration"	"160 3723 3896 181"
Option	"SwapAxes"	"1"
EndSection

dans l'exemple cela va donner :

Section "InputClass"
Identifier	"calibration"
MatchProduct	"ADS7846 Touchscreen"
Option	"Calibration"	"3919 208 236 3913"
Option	"SwapAxes"	"1"
EndSection

Sauvegarder et quittez (ctrl+X) et redémarrez.

Voila l'écran est Installé et fonctionnel, reste à lui trouver une utilité ! ;)


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
cd mjpg-streamer-experimental
export LD_LIBRARY_PATH=.
./mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so"
```

Vous pouvez accéder à la page qui hébèrge votre vidéo à l'adresse <IP du Raspberry>:8080

Ctrl+C pour stopper la vidéo.


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

WebIOPi est un utilitaire qui va permettre a une page web hébergée sur le raspberry de communiquer avec un script Python.
Cela va nous permettre de créer notre interface et controler des ports GPIO.

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

Afin de controller les moteurs, nous allons utiliser un cervomoteur L298N Double pont H DC Driver.
Nous allons voir tout ca avec le script Python mais pour l'instant, créons notre page web d'interface.

J'ai choisi d'utiliser NippleJs pour mes joysticks, d'ou le script...

le index.html :

```
<html>

<head>

        <meta charset="utf-8" />
        <link rel="stylesheet" href="style.css" />
		
        <title>Robot Control</title>
		
 
    </script>
		
		
		<style>
		body {
			overflow	: hidden;
			padding		: 0;
			margin		: 0;
			background: #BBB url(http://192.168.0.14:8080/?action=stream) no-repeat center ;
			background-size: cover;

		}				 
		
		
		 #zone_joystick1 {
		 
		 position : absolute;
		 bottom : 0px;
		 left : 0px;
		 width : 20%;
		 height : 60%;
		 border: 1px solid lime;
		 }
		 
		 #zone_joystick2 {
		 
		 position : absolute;
		 bottom : 0px;
		 right : 0px;
		 width : 20%;
		 height : 60%;
		 border: 1px solid lime;
		 }
		 
		 #result_joystick1 {
		 
		 position : absolute;
		 bottom : 0px;
		 right : 0px;
		 }
		 
		#result_joystick2 {
		 
		 position : absolute;
		 bottom : 0px;
		 left : 0px;
		 }
		
		#toggles {
		
		 display: flex;
		 flex-direction: column;
		 justify-content : flex-end;
		 align-items: center;
		 position : absolute;
		 bottom : 0px;
		 left : 30%;
		 right : 30%;
		 width : 40%;
		 border: 1px solid lime;
		
		}
		
		#toggle {
	    display: flex;
		}
		
		p {
		 font-size: 20px;
		 }
		
		/* The switch - the box around the slider */
		.switch {
		  position: relative;
		  margin: 12px;
		  display: inline-block;
		  width: 60px;
		  height: 34px;
		}

		/* Hide default HTML checkbox */
		.switch input {display:none;}

		/* The slider */
		.slider {
		  position: absolute;
		  cursor: pointer;
		  top: 0;
		  left: 0;
		  right: 0;
		  bottom: 0;
		  background-color: #ccc;
		  -webkit-transition: .4s;
		  transition: .4s;
		}

		.slider:before {
		  position: absolute;
		  content: "";
		  height: 26px;
		  width: 26px;
		  left: 4px;
		  bottom: 4px;
		  background-color: white;
		  -webkit-transition: .4s;
		  transition: .4s;
		}

		input:checked + .slider {
		  background-color: #21f243;
		}

		input:focus + .slider {
		  box-shadow: 0 0 1px #21f243;
		}

		input:checked + .slider:before {
		  -webkit-transform: translateX(26px);
		  -ms-transform: translateX(26px);
		  transform: translateX(26px);
		}

		/* Rounded sliders */
		.slider.round {
		  border-radius: 34px;
		}

		.slider.round:before {
		  border-radius: 50%;
		}
		</style>

</head>

<body>


<div id="toggles">

<div id="toggle">
<p>Caméra : </p>
<label class="switch">
  <input type="checkbox">
  <div class="slider round"></div>
</label>
</div>

<div id="toggle">
<p>Nocturne : </p>
<label class="switch">
  <input type="checkbox">
  <div class="slider round"></div>
</label>
</div>

</div>

<div id="zone_joystick1"><div id="result_joystick1"></div></div>
<div id="zone_joystick2"><div id="result_joystick2"></div></div>



<script src="nipplejs.min.js"></script>
<script>

	// premier Joystick
	var joystick1 = nipplejs.create({
			zone: document.getElementById('zone_joystick1'),
			mode: 'static',
			size: 200,
			position: {left: '50%', top: '50%'},
			color: 'lime'
	});

	joystick1.on('plain:up', function (evt, data) 
	{
		joystick1.on('start move', function (evt, data) 
	    {			
	 		var position1 = data.distance;						
			var outputEl	= document.getElementById('result_joystick1');				
			outputEl.innerHTML	= ' dy 1 : ' + position1; 			
		})
	});
	
	joystick1.on('plain:down', function (evt, data) 
	{
		joystick1.on('start move', function (evt, data) 
	    {			
	 		var position1 = - data.distance;						
			var outputEl	= document.getElementById('result_joystick1');				
			outputEl.innerHTML	= ' dy 1 : ' + position1; 			
		})
	});
									
	joystick1.on('end', function (evt, data) 
	{
		var position1 = 0;
		var outputEl	= document.getElementById('result_joystick1');				
		outputEl.innerHTML	= ' dy 1 : ' + position1;		
	});      

	

	// second Joystick	
	var joystick2 = nipplejs.create({
			zone: document.getElementById('zone_joystick2'),
			mode: 'static',
			size: 200,
			position: {left: '50%', top: '50%'},
			color: 'lime'
	});
	
    joystick2.on('plain:up', function (evt, data) 
	{
		joystick2.on('start move', function (evt, data) 
	    {			
	 		var position2 = data.distance;						
			var outputE2	= document.getElementById('result_joystick2');				
			outputE2.innerHTML	= ' dy 2 : ' + position2; 			
		})
	});
	
	joystick2.on('plain:down', function (evt, data) 
	{
		joystick2.on('start move', function (evt, data) 
	    {			
	 		var position2 = - data.distance;						
			var outputE2	= document.getElementById('result_joystick2');				
			outputE2.innerHTML	= ' dy 2 : ' + position2; 			
		})
	});
		
	joystick2.on('end', function (evt, data) 
	{
		var position2 = 0;
		var outputE2	= document.getElementById('result_joystick2');				
		outputE2.innerHTML	= ' dy 2 : ' + position2;		
	});  
	
</script>

</body>

</html>
```

et le scriptJS (renomez votre fichier en nipplejs.min.js):

```
!function(t){if("object"==typeof exports&&"undefined"!=typeof module)module.exports=t();else if("function"==typeof define&&define.amd)define([],t);else{var e;e="undefined"!=typeof window?window:"undefined"!=typeof global?global:"undefined"!=typeof self?self:this,e.nipplejs=t()}}(function(){function t(){}function e(t,i){return this.identifier=i.identifier,this.position=i.position,this.frontPosition=i.frontPosition,this.collection=t,this.defaults={size:100,threshold:.1,color:"white",fadeTime:250,dataOnly:!1,restOpacity:.5,mode:"dynamic",zone:document.body},this.config(i),"dynamic"===this.options.mode&&(this.options.restOpacity=0),this.id=e.id,e.id+=1,this.buildEl().stylize(),this.instance={el:this.ui.el,on:this.on.bind(this),off:this.off.bind(this),show:this.show.bind(this),hide:this.hide.bind(this),add:this.addToDom.bind(this),remove:this.removeFromDom.bind(this),destroy:this.destroy.bind(this),resetDirection:this.resetDirection.bind(this),computeDirection:this.computeDirection.bind(this),trigger:this.trigger.bind(this),position:this.position,frontPosition:this.frontPosition,ui:this.ui,identifier:this.identifier,id:this.id,options:this.options},this.instance}function i(t,e){var n=this;return n.nipples=[],n.idles=[],n.actives=[],n.ids=[],n.pressureIntervals={},n.manager=t,n.id=i.id,i.id+=1,n.defaults={zone:document.body,multitouch:!1,maxNumberOfNipples:10,mode:"dynamic",position:{top:0,left:0},catchDistance:200,size:100,threshold:.1,color:"white",fadeTime:250,dataOnly:!1,restOpacity:.5},n.config(e),"static"!==n.options.mode&&"semi"!==n.options.mode||(n.options.multitouch=!1),n.options.multitouch||(n.options.maxNumberOfNipples=1),n.updateBox(),n.prepareNipples(),n.bindings(),n.begin(),n.nipples}function n(t){var e=this;e.ids={},e.index=0,e.collections=[],e.config(t),e.prepareCollections();var i;return c.bindEvt(window,"resize",function(t){clearTimeout(i),i=setTimeout(function(){var t,i=c.getScroll();e.collections.forEach(function(e){e.forEach(function(e){t=e.el.getBoundingClientRect(),e.position={x:i.x+t.left,y:i.y+t.top}})})},100)}),e.collections}var o,r=!!("ontouchstart"in window),s=!!window.PointerEvent,d=!!window.MSPointerEvent,a={touch:{start:"touchstart",move:"touchmove",end:"touchend"},mouse:{start:"mousedown",move:"mousemove",end:"mouseup"},pointer:{start:"pointerdown",move:"pointermove",end:"pointerup"},MSPointer:{start:"MSPointerDown",move:"MSPointerMove",end:"MSPointerUp"}},p={};s?o=a.pointer:d?o=a.MSPointer:r?(o=a.touch,p=a.mouse):o=a.mouse;var c={};c.distance=function(t,e){var i=e.x-t.x,n=e.y-t.y;return Math.sqrt(i*i+n*n)},c.angle=function(t,e){var i=e.x-t.x,n=e.y-t.y;return c.degrees(Math.atan2(n,i))},c.findCoord=function(t,e,i){var n={x:0,y:0};return i=c.radians(i),n.x=t.x-e*Math.cos(i),n.y=t.y-e*Math.sin(i),n},c.radians=function(t){return t*(Math.PI/180)},c.degrees=function(t){return t*(180/Math.PI)},c.bindEvt=function(t,e,i){t.addEventListener?t.addEventListener(e,i,!1):t.attachEvent&&t.attachEvent(e,i)},c.unbindEvt=function(t,e,i){t.removeEventListener?t.removeEventListener(e,i):t.detachEvent&&t.detachEvent(e,i)},c.trigger=function(t,e,i){var n=new CustomEvent(e,i);t.dispatchEvent(n)},c.prepareEvent=function(t){return t.preventDefault(),t.type.match(/^touch/)?t.changedTouches:t},c.getScroll=function(){var t=void 0!==window.pageXOffset?window.pageXOffset:(document.documentElement||document.body.parentNode||document.body).scrollLeft,e=void 0!==window.pageYOffset?window.pageYOffset:(document.documentElement||document.body.parentNode||document.body).scrollTop;return{x:t,y:e}},c.applyPosition=function(t,e){e.x&&e.y?(t.style.left=e.x+"px",t.style.top=e.y+"px"):(e.top||e.right||e.bottom||e.left)&&(t.style.top=e.top,t.style.right=e.right,t.style.bottom=e.bottom,t.style.left=e.left)},c.getTransitionStyle=function(t,e,i){var n=c.configStylePropertyObject(t);for(var o in n)if(n.hasOwnProperty(o))if("string"==typeof e)n[o]=e+" "+i;else{for(var r="",s=0,d=e.length;s<d;s+=1)r+=e[s]+" "+i+", ";n[o]=r.slice(0,-2)}return n},c.getVendorStyle=function(t,e){var i=c.configStylePropertyObject(t);for(var n in i)i.hasOwnProperty(n)&&(i[n]=e);return i},c.configStylePropertyObject=function(t){var e={};e[t]="";var i=["webkit","Moz","o"];return i.forEach(function(i){e[i+t.charAt(0).toUpperCase()+t.slice(1)]=""}),e},c.extend=function(t,e){for(var i in e)e.hasOwnProperty(i)&&(t[i]=e[i]);return t},c.safeExtend=function(t,e){var i={};for(var n in t)t.hasOwnProperty(n)&&e.hasOwnProperty(n)?i[n]=e[n]:t.hasOwnProperty(n)&&(i[n]=t[n]);return i},c.map=function(t,e){if(t.length)for(var i=0,n=t.length;i<n;i+=1)e(t[i]);else e(t)},t.prototype.on=function(t,e){var i,n=this,o=t.split(/[ ,]+/g);n._handlers_=n._handlers_||{};for(var r=0;r<o.length;r+=1)i=o[r],n._handlers_[i]=n._handlers_[i]||[],n._handlers_[i].push(e);return n},t.prototype.off=function(t,e){var i=this;return i._handlers_=i._handlers_||{},void 0===t?i._handlers_={}:void 0===e?i._handlers_[t]=null:i._handlers_[t]&&i._handlers_[t].indexOf(e)>=0&&i._handlers_[t].splice(i._handlers_[t].indexOf(e),1),i},t.prototype.trigger=function(t,e){var i,n=this,o=t.split(/[ ,]+/g);n._handlers_=n._handlers_||{};for(var r=0;r<o.length;r+=1)i=o[r],n._handlers_[i]&&n._handlers_[i].length&&n._handlers_[i].forEach(function(t){t.call(n,{type:i,target:n},e)})},t.prototype.config=function(t){var e=this;e.options=e.defaults||{},t&&(e.options=c.safeExtend(e.options,t))},t.prototype.bindEvt=function(t,e){var i=this;return i._domHandlers_=i._domHandlers_||{},i._domHandlers_[e]=function(){"function"==typeof i["on"+e]?i["on"+e].apply(i,arguments):console.warn('[WARNING] : Missing "on'+e+'" handler.')},c.bindEvt(t,o[e],i._domHandlers_[e]),p[e]&&c.bindEvt(t,p[e],i._domHandlers_[e]),i},t.prototype.unbindEvt=function(t,e){var i=this;return i._domHandlers_=i._domHandlers_||{},c.unbindEvt(t,o[e],i._domHandlers_[e]),p[e]&&c.unbindEvt(t,p[e],i._domHandlers_[e]),delete i._domHandlers_[e],this},e.prototype=new t,e.constructor=e,e.id=0,e.prototype.buildEl=function(t){return this.ui={},this.options.dataOnly?this:(this.ui.el=document.createElement("div"),this.ui.back=document.createElement("div"),this.ui.front=document.createElement("div"),this.ui.el.className="nipple collection_"+this.collection.id,this.ui.back.className="back",this.ui.front.className="front",this.ui.el.setAttribute("id","nipple_"+this.collection.id+"_"+this.id),this.ui.el.appendChild(this.ui.back),this.ui.el.appendChild(this.ui.front),this)},e.prototype.stylize=function(){if(this.options.dataOnly)return this;var t=this.options.fadeTime+"ms",e=c.getVendorStyle("borderRadius","50%"),i=c.getTransitionStyle("transition","opacity",t),n={};return n.el={position:"absolute",opacity:this.options.restOpacity,display:"block",zIndex:999},n.back={position:"absolute",display:"block",width:this.options.size+"px",height:this.options.size+"px",marginLeft:-this.options.size/2+"px",marginTop:-this.options.size/2+"px",background:this.options.color,opacity:".5"},n.front={width:this.options.size/2+"px",height:this.options.size/2+"px",position:"absolute",display:"block",marginLeft:-this.options.size/4+"px",marginTop:-this.options.size/4+"px",background:this.options.color,opacity:".5"},c.extend(n.el,i),c.extend(n.back,e),c.extend(n.front,e),this.applyStyles(n),this},e.prototype.applyStyles=function(t){for(var e in this.ui)if(this.ui.hasOwnProperty(e))for(var i in t[e])this.ui[e].style[i]=t[e][i];return this},e.prototype.addToDom=function(){return this.options.dataOnly||document.body.contains(this.ui.el)?this:(this.options.zone.appendChild(this.ui.el),this)},e.prototype.removeFromDom=function(){return this.options.dataOnly||!document.body.contains(this.ui.el)?this:(this.options.zone.removeChild(this.ui.el),this)},e.prototype.destroy=function(){clearTimeout(this.removeTimeout),clearTimeout(this.showTimeout),clearTimeout(this.restTimeout),this.trigger("destroyed",this.instance),this.removeFromDom(),this.off()},e.prototype.show=function(t){var e=this;return e.options.dataOnly?e:(clearTimeout(e.removeTimeout),clearTimeout(e.showTimeout),clearTimeout(e.restTimeout),e.addToDom(),e.restCallback(),setTimeout(function(){e.ui.el.style.opacity=1},0),e.showTimeout=setTimeout(function(){e.trigger("shown",e.instance),"function"==typeof t&&t.call(this)},e.options.fadeTime),e)},e.prototype.hide=function(t){var e=this;return e.options.dataOnly?e:(e.ui.el.style.opacity=e.options.restOpacity,clearTimeout(e.removeTimeout),clearTimeout(e.showTimeout),clearTimeout(e.restTimeout),e.removeTimeout=setTimeout(function(){var i="dynamic"===e.options.mode?"none":"block";e.ui.el.style.display=i,"function"==typeof t&&t.call(e),e.trigger("hidden",e.instance)},e.options.fadeTime),e.restPosition(),e)},e.prototype.restPosition=function(t){var e=this;e.frontPosition={x:0,y:0};var i=e.options.fadeTime+"ms",n={};n.front=c.getTransitionStyle("transition",["top","left"],i);var o={front:{}};o.front={left:e.frontPosition.x+"px",top:e.frontPosition.y+"px"},e.applyStyles(n),e.applyStyles(o),e.restTimeout=setTimeout(function(){"function"==typeof t&&t.call(e),e.restCallback()},e.options.fadeTime)},e.prototype.restCallback=function(){var t=this,e={};e.front=c.getTransitionStyle("transition","none",""),t.applyStyles(e),t.trigger("rested",t.instance)},e.prototype.resetDirection=function(){this.direction={x:!1,y:!1,angle:!1}},e.prototype.computeDirection=function(t){var e,i,n,o=t.angle.radian,r=Math.PI/4,s=Math.PI/2;if(e=o>r&&o<3*r?"up":o>-r&&o<=r?"left":o>3*-r&&o<=-r?"down":"right",i=o>-s&&o<s?"left":"right",n=o>0?"up":"down",t.force>this.options.threshold){var d={};for(var a in this.direction)this.direction.hasOwnProperty(a)&&(d[a]=this.direction[a]);var p={};this.direction={x:i,y:n,angle:e},t.direction=this.direction;for(var a in d)d[a]===this.direction[a]&&(p[a]=!0);if(p.x&&p.y&&p.angle)return t;p.x&&p.y||this.trigger("plain",t),p.x||this.trigger("plain:"+i,t),p.y||this.trigger("plain:"+n,t),p.angle||this.trigger("dir dir:"+e,t)}return t},i.prototype=new t,i.constructor=i,i.id=0,i.prototype.prepareNipples=function(){var t=this,e=t.nipples;e.on=t.on.bind(t),e.off=t.off.bind(t),e.options=t.options,e.destroy=t.destroy.bind(t),e.ids=t.ids,e.id=t.id,e.processOnMove=t.processOnMove.bind(t),e.processOnEnd=t.processOnEnd.bind(t),e.get=function(t){if(void 0===t)return e[0];for(var i=0,n=e.length;i<n;i+=1)if(e[i].identifier===t)return e[i];return!1}},i.prototype.bindings=function(){var t=this;t.bindEvt(t.options.zone,"start"),t.options.zone.style.touchAction="none",t.options.zone.style.msTouchAction="none"},i.prototype.begin=function(){var t=this,e=t.options;if("static"===e.mode){var i=t.createNipple(e.position,t.manager.getIdentifier());i.add(),t.idles.push(i)}},i.prototype.createNipple=function(t,i){var n=this,o=c.getScroll(),r={},s=n.options;if(t.x&&t.y)r={x:t.x-(o.x+n.box.left),y:t.y-(o.y+n.box.top)};else if(t.top||t.right||t.bottom||t.left){var d=document.createElement("DIV");d.style.display="hidden",d.style.top=t.top,d.style.right=t.right,d.style.bottom=t.bottom,d.style.left=t.left,d.style.position="absolute",s.zone.appendChild(d);var a=d.getBoundingClientRect();s.zone.removeChild(d),r=t,t={x:a.left+o.x,y:a.top+o.y}}var p=new e(n,{color:s.color,size:s.size,threshold:s.threshold,fadeTime:s.fadeTime,dataOnly:s.dataOnly,restOpacity:s.restOpacity,mode:s.mode,identifier:i,position:t,zone:s.zone,frontPosition:{x:0,y:0}});return s.dataOnly||(c.applyPosition(p.ui.el,r),c.applyPosition(p.ui.front,p.frontPosition)),n.nipples.push(p),n.trigger("added "+p.identifier+":added",p),n.manager.trigger("added "+p.identifier+":added",p),n.bindNipple(p),p},i.prototype.updateBox=function(){var t=this;t.box=t.options.zone.getBoundingClientRect()},i.prototype.bindNipple=function(t){var e,i=this,n=function(t,n){e=t.type+" "+n.id+":"+t.type,i.trigger(e,n)};t.on("destroyed",i.onDestroyed.bind(i)),t.on("shown hidden rested dir plain",n),t.on("dir:up dir:right dir:down dir:left",n),t.on("plain:up plain:right plain:down plain:left",n)},i.prototype.pressureFn=function(t,e,i){var n=this,o=0;clearInterval(n.pressureIntervals[i]),n.pressureIntervals[i]=setInterval(function(){var i=t.force||t.pressure||t.webkitForce||0;i!==o&&(e.trigger("pressure",i),n.trigger("pressure "+e.identifier+":pressure",i),o=i)}.bind(n),100)},i.prototype.onstart=function(t){var e=this,i=e.options;t=c.prepareEvent(t),e.updateBox();var n=function(t){e.actives.length<i.maxNumberOfNipples&&e.processOnStart(t)};return c.map(t,n),e.manager.bindDocument(),!1},i.prototype.processOnStart=function(t){var e,i=this,n=i.options,o=i.manager.getIdentifier(t),r=t.force||t.pressure||t.webkitForce||0,s={x:t.pageX,y:t.pageY},d=i.getOrCreate(o,s);d.identifier=o;var a=function(e){e.trigger("start",e),i.trigger("start "+e.id+":start",e),e.show(),r>0&&i.pressureFn(t,e,e.identifier),i.processOnMove(t)};if((e=i.idles.indexOf(d))>=0&&i.idles.splice(e,1),i.actives.push(d),i.ids.push(d.identifier),"semi"!==n.mode)a(d);else{var p=c.distance(s,d.position);if(!(p<=n.catchDistance))return d.destroy(),void i.processOnStart(t);a(d)}return d},i.prototype.getOrCreate=function(t,e){var i,n=this,o=n.options;return/(semi|static)/.test(o.mode)?(i=n.idles[0])?(n.idles.splice(0,1),i):"semi"===o.mode?n.createNipple(e,t):(console.warn("Coudln't find the needed nipple."),!1):i=n.createNipple(e,t)},i.prototype.processOnMove=function(t){var e=this,i=e.options,n=e.manager.getIdentifier(t),o=e.nipples.get(n);if(!o)return console.error("Found zombie joystick with ID "+n),void e.manager.removeIdentifier(n);o.identifier=n;var r=o.options.size/2,s={x:t.pageX,y:t.pageY},d=c.distance(s,o.position),a=c.angle(s,o.position),p=c.radians(a),l=d/r;d>r&&(d=r,s=c.findCoord(o.position,d,a)),o.frontPosition={x:s.x-o.position.x,y:s.y-o.position.y},i.dataOnly||c.applyPosition(o.ui.front,o.frontPosition);var u={identifier:o.identifier,position:s,force:l,pressure:t.force||t.pressure||t.webkitForce||0,distance:d,angle:{radian:p,degree:a},instance:o};u=o.computeDirection(u),u.angle={radian:c.radians(180-a),degree:180-a},o.trigger("move",u),e.trigger("move "+o.id+":move",u)},i.prototype.processOnEnd=function(t){var e=this,i=e.options,n=e.manager.getIdentifier(t),o=e.nipples.get(n),r=e.manager.removeIdentifier(o.identifier);o&&(i.dataOnly||o.hide(function(){"dynamic"===i.mode&&(o.trigger("removed",o),e.trigger("removed "+o.id+":removed",o),e.manager.trigger("removed "+o.id+":removed",o),o.destroy())}),clearInterval(e.pressureIntervals[o.identifier]),o.resetDirection(),o.trigger("end",o),e.trigger("end "+o.id+":end",o),e.ids.indexOf(o.identifier)>=0&&e.ids.splice(e.ids.indexOf(o.identifier),1),e.actives.indexOf(o)>=0&&e.actives.splice(e.actives.indexOf(o),1),/(semi|static)/.test(i.mode)?e.idles.push(o):e.nipples.indexOf(o)>=0&&e.nipples.splice(e.nipples.indexOf(o),1),e.manager.unbindDocument(),/(semi|static)/.test(i.mode)&&(e.manager.ids[r.id]=r.identifier))},i.prototype.onDestroyed=function(t,e){var i=this;i.nipples.indexOf(e)>=0&&i.nipples.splice(i.nipples.indexOf(e),1),i.actives.indexOf(e)>=0&&i.actives.splice(i.actives.indexOf(e),1),i.idles.indexOf(e)>=0&&i.idles.splice(i.idles.indexOf(e),1),i.ids.indexOf(e.identifier)>=0&&i.ids.splice(i.ids.indexOf(e.identifier),1),i.manager.removeIdentifier(e.identifier),i.manager.unbindDocument()},i.prototype.destroy=function(){var t=this;t.unbindEvt(t.options.zone,"start"),t.nipples.forEach(function(t){t.destroy()});for(var e in t.pressureIntervals)t.pressureIntervals.hasOwnProperty(e)&&clearInterval(t.pressureIntervals[e]);t.trigger("destroyed",t.nipples),t.manager.unbindDocument(),t.off()},n.prototype=new t,n.constructor=n,n.prototype.prepareCollections=function(){var t=this;t.collections.create=t.create.bind(t),t.collections.on=t.on.bind(t),t.collections.off=t.off.bind(t),t.collections.destroy=t.destroy.bind(t),t.collections.get=function(e){var i;return t.collections.every(function(t){return!(i=t.get(e))}),i}},n.prototype.create=function(t){return this.createCollection(t)},n.prototype.createCollection=function(t){var e=this,n=new i(e,t);return e.bindCollection(n),e.collections.push(n),n},n.prototype.bindCollection=function(t){var e,i=this,n=function(t,n){e=t.type+" "+n.id+":"+t.type,i.trigger(e,n)};t.on("destroyed",i.onDestroyed.bind(i)),t.on("shown hidden rested dir plain",n),t.on("dir:up dir:right dir:down dir:left",n),t.on("plain:up plain:right plain:down plain:left",n)},n.prototype.bindDocument=function(){var t=this;t.binded||(t.bindEvt(document,"move").bindEvt(document,"end"),t.binded=!0)},n.prototype.unbindDocument=function(t){var e=this;Object.keys(e.ids).length&&t!==!0||(e.unbindEvt(document,"move").unbindEvt(document,"end"),e.binded=!1)},n.prototype.getIdentifier=function(t){var e;return t?(e=void 0===t.identifier?t.pointerId:t.identifier,void 0===e&&(e=this.latest||0)):e=this.index,void 0===this.ids[e]&&(this.ids[e]=this.index,this.index+=1),this.latest=e,this.ids[e]},n.prototype.removeIdentifier=function(t){var e={};for(var i in this.ids)if(this.ids[i]===t){e.id=i,e.identifier=this.ids[i],delete this.ids[i];break}return e},n.prototype.onmove=function(t){var e=this;return e.onAny("move",t),!1},n.prototype.onend=function(t){var e=this;return e.onAny("end",t),!1},n.prototype.onAny=function(t,e){var i,n=this,o="processOn"+t.charAt(0).toUpperCase()+t.slice(1);e=c.prepareEvent(e);var r=function(t,e,i){i.ids.indexOf(e)>=0&&(i[o](t),t._found_=!0)},s=function(t){i=n.getIdentifier(t),c.map(n.collections,r.bind(null,t,i)),t._found_||n.removeIdentifier(i)};return c.map(e,s),!1},n.prototype.destroy=function(){var t=this;t.unbindDocument(!0),t.ids={},t.index=0,t.collections.forEach(function(t){t.destroy()}),t.off()},n.prototype.onDestroyed=function(t,e){var i=this;return!(i.collections.indexOf(e)<0)&&void i.collections.splice(i.collections.indexOf(e),1)};var l=new n;return{create:function(t){return l.create(t)},factory:l}});
```

Mettre les deux fichiers dans le même dossier à renommer en "html".

Il nous reste à "connecter" cette interface web à un script Python selon nos besoins car pour l'instant, à part la vidéo, rien de foncionne ...