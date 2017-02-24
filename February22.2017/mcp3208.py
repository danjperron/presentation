#!/usr/bin/python3
import spidev

def readadc(adcnum):
    if adcnum > 7 or adcnum < 0:     #just to check if adcnum is out of the A/D converters channel range
        return -1
    r = spi.xfer2([4 + (adcnum >> 2), (adcnum & 3) << 6, 0])  
    #send the three bytes to the A/D in the format the A/D's datasheet explains(take time to 
    #doublecheck these
    adcout = ((r[1] & 15) << 8) + r[2] 
    #use AND operation with the second byte to get the last  4 bits, and then make way 
    #for the third data byte with the "move 8 bits to left" << 8 operation
    return adcout

if __name__ == "__main__" :
    spi = spidev.SpiDev()
    spi.open(0,0)


    #Le facteur est en realite deux
    # Un diviseur de tension par deux resistance
    # R1 = 10K R2 = 100K donc la reduction est de (10/10+100)= 1/11 =>  donc l'enverse est 11
    # La Tension de reference  qui est de 3.3V . 12 Bits donne une valeur maximale de 4095  pow(2,12)
    # Donc l'etallonage est sur 3.3V/4095
    CFactor = (110.0/10.0) * 3.3 / 4095

    #le canal 1 est en realite le 0 
    print("Channel 1 is {:.2} Volt(s)".format(readadc(0) * CFactor))


