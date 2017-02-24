#!/usr/bin/python3
# -*- coding: utf-8 -*-


#Cette application demontre comment
#utiliser un display 7 segments qui uilisent deux 74hc595
#Le premier est branché sur les segments
#Le deuxième est branché sur chaque digit.
#Le SPI sera utilisé 
 


import spidev
import threading
import time


#definitaopm de la classe LEDS
class LEDs:

    def __init__(self, bus):
        # digit segment
        A = 1
        B = 2
        C = 4
        D = 8
        E = 16
        F = 32
        G = 64
        DP = 128

        # création d'un dictionaire pour convertir le chiffre en segment
        #    segment
        #
        #
        #    -A-
        #   |   |
        #   F   B
        #   |   |
        #    -G-
        #   |   |
        #   E   C
        #   |   |
        #    -D-   DP
        #
        #
        #   création de la correspondance digit versus segment
        #

        D0 = (A | B | C | D | E | F)
        D1 = (B | C)
        D2 = (A | B | G | E | D)
        D3 = (A | B | G | C | D)
        D4 = (F | B | G | C)
        D5 = (A | F | G | C |D)
        D6 = (A | F | G | C |D |E)
        D7 = (A | B | C)
        D8 = (A | B | C | D | E | F | G)
        D9 = (A | B | C | D | F | G)
        DMOINS = G
        DBLANK = 0
        DQUESTION = ( A | B | G | E)

        # dictionaire des valeurs
        self.Chiffre = {0: D0, 1: D1, 2: D2, 3: D3, 4: D4,
                        5: D5, 6: D6, 7: D7, 8: D8, 9: D9,
                        '-': DMOINS, ' ': DBLANK, '?': DQUESTION,
                        'SEGA': A, 'SEGB': B, 'SEGC': C,
                        'SEGD': D, 'SEGE': E, 'SEGF': F,
                        'SEGG': G, 'SEGDP': DP}

        #un display de 4 digits 
        self.ndigits = 4    
        self.digits = self.ndigits * [0]
        self.digitsIdx = 0

        #initialisation du SPI
        self.spi = spidev.SpiDev()
        self.speed=2000000
        self.spi.open(0,bus)
        self.spi.max_speed_hz=self.speed

        #Flag de fin de thread 
        self.Exit = False

        #création d'un thread pour afficher un digit à la fois
        self.timer = threading.Thread(target=self.nextDigits)
        self.timer.start()


    def __del__(self):
        self.Exit = True

    #Thread pour l'affichage en  multiplexage. Un digit à la fois
    def nextDigits(self):
        #je boucle tant que Exit est faux
        while not self.Exit:
            #prochain digit
            self.digitsIdx = self.digitsIdx + 1
             #est-ce le dernier digit
            if self.digitsIdx >= self.ndigits:
                #si oui cèest donc le premier
                self.digitsIdx =0
            #ok va chercher le data du digit et inverse le
            # puisque les leds sur les segments sont sur les cathodes.
            currentDigit= (~self.digits[self.digitsIdx]) & 0xff;
            #ok 2 bytes transfer  le bit indiquant quel digit   et la valeur pour les segments
            self.spi.xfer2([1 << (self.ndigits -1 - self.digitsIdx) , currentDigit])
            #délai de rafraîchissement  200Hz / 4 digits = 50Hz
            time.sleep(0.005)
        #sortie de thread  donc les leds à OFF
        self.spi.xfer2([0,0])



    def GetByte(self, Dval=' ', DP=False):
        if DP:
            BData = DP
        else:
            BData = 0
        if Dval in self.Chiffre:
            BData = BData | self.Chiffre[Dval]
        else:
            BData = BData | self.Chiffre['?']
        return BData


    #enregistre dans la table digits la correspondance de valeur
    def numero(self,valeur):
        ivaleur = int(valeur)
        d = self.ndigits * [ 0 ]
        for i in range(self.ndigits):
            d[i] = self.Chiffre[ivaleur % 10]
            ivaleur = ivaleur // 10
            if ivaleur == 0:
                break;
        self.digits=d
        
        


    def stop(self):
        for i in range(self.ndigits):
            dp.digits[i] = ' ' 
        self.Exit= True      


#programme de test qui affiche un chiffre qui augmente de 1 
#à chaque dixième de seconde

if __name__ == "__main__":

    dp = LEDs(0)

    try:

        i = 0
        while True:
            dp.numero(i)
            i = i + 1
#            print(i)
            time.sleep(0.1)

    except KeyboardInterrupt:
        dp.stop()
                           
    
