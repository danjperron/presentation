#!/usr/bin/python3


#ceci est un exemple d'un light chaser 
#comme celui des cylons dans battlestar galatica
#Ce sont des leds individuelles qui son activees
#par des pcf8574 en i2c.
#16 leds en tout, donc deux pcf8574


import time
import smbus


#Pour le PI3 c'est SMBus(1)

bus = smbus.SMBus(0)


#initialisation des variables de depart
#la variable led est une variable mirroir des sorties des deux pcf8574
#Le Low byte est sur le pcf8574 avec l'adresse 0x20
#Le High byte est sur le pcf8574 avec l'adresse 0x21

led = 0x100

Direction = 1


#cette fonction transfere la variable led au sorties par le i2c
def DisplayLed():
    bus.write_byte(0x20, (~led & 0xff))
    bus.write_byte(0x21, ((~led) >> 8) & 0xff)


#program principale
#affiche les leds 
#ensuite shift a gauche ou a droite pour afficher la prochaine led

try:
    while True:
        DisplayLed()
        if Direction == 1:
            led = led >> 1
            if led == 0:
               led = 2
               Direction = -1
        else:
            led = led << 1
            if led == 0x10000:
               led = 0x4000
               Direction = 1
        #ajustement du delais
        time.sleep(0.075)

#si le keyboard recoit on ctrl-C arrete tout et coupe toute led
except KeyboardInterrupt:
    led = 0
    DisplayLed()


   
