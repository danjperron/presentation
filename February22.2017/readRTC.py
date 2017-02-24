#!/usr/bin/python3
import smbus
import time


#ceci est un program pour lire  le RTC DS1307 Heure minutes secondes pendant 5 secondes

#Le RTC est a 0x68
RTC = 0x68

#fonction pour convertir un octet BCD 
# le  nibble superieur a un poids de 10 et non de 16
def BCD(value):
    return( (value >> 4) * 10 + (value &0xf))

oldsec=99

try:


#   Pour le Pi3 c'est SMBus(1)  et pour les autres SMBus(0) 
#    bus = smbus.SMBus(1)

    bus = smbus.SMBus(0)
   
    depart=time.time()

    while (time.time() - depart) <=  5 :
        #lire heure minute second
        heure = bus.read_byte_data(RTC,2)
        min = bus.read_byte_data(RTC,1)
        sec = bus.read_byte_data(RTC,0)
   
        if oldsec == sec:
            time.sleep(0.1)
            continue
        
        oldsec =sec
        min = BCD(min)
        sec = BCD(sec)

        #heure bit 6-(12/24h) 5-(10hr/ PM/AM)  4-10hour 3..0 hour
        H12_24 = heure & 64

        if (heure & 0x40):
            #ok 12 heures mode
            heure = BCD(heure & 0x1f)
            if heure & 0x20:
                AMPM= "PM"
            else:
                AMPM= "AM"    
        else:
            #24 heures mode
            heure = BCD(heure & 0x3f)
            AMPM=""

        print("{:2}:{:02}:{:02} {}".format(heure,min,sec,AMPM))


except IOError:
    print("Ne peut ouvrir i2c ou lire le RTC")


