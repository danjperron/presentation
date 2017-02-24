#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
# Ce programme lit l'information envoyé par le dé bluetooth
# et affiche le numéro indiquer par le dé
#
# l'information du  module à l'intérieur du dé est disponible sur
# https://github.com/danjperron/blueGyro.X

import sys
import serial
import time

#création de la classe Dice pour encapsuler le module
class Dice:

    def __init__(self,SerialName):
        self.SerialName= SerialName
        try:
            #ouverture du port série
            self.com= serial.Serial(SerialName, baudrate=9600, timeout=1.0)
            self.validateDice()
        except:
            self.com = None

    def __del__(self):
       if not (self.com is None):
        if self.com.isOpen():
            self.com.close()

    #cette fonction retourne la tension de la batterie
    def readVoltage(self):
        try:
            self.com.write('V')
            line= self.com.readline()
        except:
            return 0
         
        if len(line) == 0:
            return 0
        print('line',line)
        items= line.split('=')
        print('items',items[1])
        V = items[1].split('V')
        print('V',V)

        try:
            Voltage = float(V[0])
        except ValueError:
            return -1.0
        print('Voltage',Voltage) 

        return Voltage
     
    #cette fonction retourne le numéro sur le dessus du dé
    def read(self):

        #demande au module l'information présente des capteurs sur une ligne
        try:
            self.com.flushInput()
            time.sleep(0.1)
            self.com.write('i')
            line= self.com.readline()
        except:
            return 0

        if len(line) == 0:
            return 0
        items= line.split()
        if len(items) < 5:
            return 0
        #extraction de l'accéléromètre
        Gx = items[2].split('=')
        Gy = items[3].split('=')
        Gz = items[4].split('=')
  
        #Validation des étiquettes
        if not (Gx[0]=='x'):
            return 0
        if not (Gy[0]=='y'):
            return 0
        if not (Gz[0]=='z'):
            return 0
        
        #Lire les valeurs
        try:
            ValueX = float(Gx[1])
            ValueY = float(Gy[1])
            #split Z to remove 'G'
            Gz[1]  = Gz[1].split('G')[0]
            ValueZ = float(Gz[1])
        except ValueError:
            return 0

        #Calculer les valeurs absolues
        AbsX = abs(ValueX)
        AbsY = abs(ValueY)
        AbsZ = abs(ValueZ)

        #Cherchons l'axe avec le plus grand G
        #pour déterminer la valeur sur le dessus
        if (AbsX > AbsY) and ( AbsX > AbsZ):
            #Max is X
            if ValueX > 0:
                return 3
            else:
                return 4
        elif AbsY > AbsZ:
            #Max is Y
            if ValueY > 0:
                return 2
            else:
                return 5
        else:
            #Max is Z
            if ValueZ > 0:
                return 6
            else:
                return 1

    #cette fonction vérifie la connection série
    def validateDice(self):
        try:
            #force egg crash device to be in idle mode by sending escape
            self.com.write(chr(27))
            time.sleep(0.1)
            #flush serial in buffer
            self.com.flushInput()
            #do it twice just in case
            self.com.write(chr(27))
            time.sleep(0.1)
        except:
            pass
        #return true if dice return value is valid
        return (self.read() > 0)



    #cette fonction connecte le module
    def connect(self,CloseFirst=True):
        if self.com.isOpen():
            self.com.close()
        try:
            time.sleep(0.1)
            self.com = serial.Serial(self.SerialName, baudrate=9600, timeout=2.0)
        except IOError: 
            self.com = None
            return 0
        return self.validateDice()


#routine principale si cette classe est rouler seule
if __name__  == "__main__" :
    #creation de l'objet myDice
    myDice = Dice('/dev/rfcomm1')
    time.sleep(01)
    if myDice.com is None:
       print('Erreur de communication avec le dé')
       quit()

    #Ouvrir la connection série encore
    #pas nécessaire mais j'en ai besoin pour Alexa
    #et c'est ma façon simple de faire un flush
   
    #myDice.connect()

    try:
        while True:
            #afficher la valeur du dé 
            #en utilisant stdout pour ne pas sauter de ligne
            sys.stdout.write(chr(13))
            sys.stdout.write(str(myDice.read()))
            #forcer l'output parcequ'il n'y a pas de saut de ligne
            sys.stdout.flush()
            time.sleep(0.1)

    #arreter si le clavier envoie un CTRL-C
    except KeyboardInterrupt:
      pass


