#include <stdint.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include <fcntl.h>
#include <malloc.h>
#include <string.h>
#include <sys/ioctl.h>
#include <linux/types.h>
#include <linux/spi/spidev.h>


#define MAX7219_DIGIT0 1
#define MAX7219_DIGIT1 2
#define MAX7219_DIGIT2 3
#define MAX7219_DIGIT3 4


#define MAX7219_MODE_DECODE 9
#define MAX7219_MODE_INTENSITY 0xa
#define MAX7219_MODE_SCAN_LIMIT 0x0B
#define MAX7219_MODE_POWER 0x0C
#define MAX7219_MODE_TEST 0x0F
#define MAX7219_MODE_NOOP 0x00




/* application  pour afficher sur un display utilisant un max7219
la valeur de temperature d'un capteur DS18B20 


Le SPI  sur le chip select 1 est utilisé


Le DS18B20 est branché sur le GPIO4 avec le 1W enable sur le raspberry Pi
*/


// ne pas oublier de changer l'ID du capteur
#define DS18B20_ID "28-000006f058c9"



int fd;

static void pabort(const char *s)
{
   perror(s);
   abort();
}


static uint8_t mode;
static uint8_t bits = 8;
static uint32_t speed = 500000;
static uint16_t delay;
static unsigned char Bits[8]={128,64,32,16,8,4,2,1};


void MaxWrite(unsigned char Reg, unsigned char Value)
{
   int ret;
   unsigned char ArrayTx[2];
   unsigned char ArrayRx[3];
   ArrayRx[0]=0;
   ArrayTx[0]=Reg;
   ArrayTx[1]=Value;
   delay = 1;
   struct spi_ioc_transfer tr = {
   .tx_buf = (unsigned long) ArrayTx,
   .rx_buf = (unsigned long) ArrayRx,
   .len = 2,
   .delay_usecs = delay,
   .speed_hz= speed,
   .bits_per_word = bits,
  };
  ret = ioctl(fd, SPI_IOC_MESSAGE(1), &tr);
  if(ret < 1)
    pabort("Can't send spi message");
}


double readTemp(char * ds_sensor)
{
       char fname[256];

       sprintf(fname,"/sys/bus/w1/devices/%s/w1_slave",ds_sensor);

	FILE *device = fopen(fname, "r");
	double temperature = -1;
	char crcVar[5];
	if (device == NULL)
	{
		pabort("Unresponsive DS18B20\n");
	}
	if (device != NULL)
	{
		if (!ferror(device))
		{
			fscanf(device, "%*x %*x %*x %*x %*x %*x %*x %*x %*x : crc=%*x %s", crcVar);
			if (strncmp(crcVar, "YES", 3) == 0)
			{
				fscanf(device, "%*x %*x %*x %*x %*x %*x %*x %*x %*x t=%lf", &temperature);
				//printf("%.3lf\n",temperature);
				temperature /= 1000.0;
			}
		}
	}
	fclose(device);
	return temperature;
}

void SetDigit(int idx,unsigned char value)
{
  unsigned char temp;
  switch(value)
  {
   case ' ': temp=15;break;
   case '-': temp=10;break;
   default : temp=value-'0';break; 
  }
  if(idx==2) temp|=128;
  MaxWrite(idx,temp);
}



void DisplayTemperature(float  t)
{
  int loop;
  int  idx=0;
  char buffer[16];
  sprintf(buffer,"%5.1f",t);
  SetDigit(4,buffer[0]);
  SetDigit(3,buffer[1]);
  SetDigit(2,buffer[2]);
  SetDigit(1,buffer[4]);
}



int main(int argc, char *argv[])
{
   int ret = 0;
   int loop;
   unsigned char Array[2];


   fd = open("/dev/spidev0.1",O_RDWR);
   if(fd <0)
     pabort("Can't open device\n");

   mode = 0;

   ret = ioctl(fd, SPI_IOC_WR_MODE, &mode);
   if (ret == -1)
      pabort("can't set spi mode");

   ret = ioctl(fd, SPI_IOC_RD_MODE, &mode);
   if (ret == -1)
      pabort("can't get spi mode");

   /*
    * bits per word
    */
   ret = ioctl(fd, SPI_IOC_WR_BITS_PER_WORD, &bits);
   if (ret == -1)
      pabort("can't set bits per word");

   ret = ioctl(fd, SPI_IOC_RD_BITS_PER_WORD, &bits);
   if (ret == -1)
      pabort("can't get bits per word");

    /*
    * max speed hz
    */
   ret = ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed);
   if (ret == -1)
      pabort("can't set max speed hz");

   ret = ioctl(fd, SPI_IOC_RD_MAX_SPEED_HZ, &speed);
   if (ret == -1)
      pabort("can't get max speed hz");

   printf("speed = %d\n",speed);
   printf("bits  = %d\n",bits);
   printf("mode  = %d\n",mode);

   // Init Display

   MaxWrite(MAX7219_MODE_DECODE, 0xff);
   MaxWrite(MAX7219_MODE_DECODE, 0xff);
   MaxWrite(MAX7219_MODE_SCAN_LIMIT, 3);
   MaxWrite(MAX7219_MODE_INTENSITY, 4);
   MaxWrite(MAX7219_MODE_POWER, 1);

   MaxWrite(MAX7219_DIGIT0, 15);
   MaxWrite(MAX7219_DIGIT1, 15);
   MaxWrite(MAX7219_DIGIT2, 15);
   MaxWrite(MAX7219_DIGIT3, 15);




while(1)
   {
      double t=readTemp(DS18B20_ID);
      DisplayTemperature(t);
      usleep(250000);
      printf("%3.1f\n",t);
   }
close(fd);
return 0;
}
