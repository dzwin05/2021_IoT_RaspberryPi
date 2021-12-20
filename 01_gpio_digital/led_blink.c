#include <wiringPi.h>
#define LED_PIN 7

int main (void)
{
  wiringPiSetup () ;
  pinMode (LED_PIN, OUTPUT) ;
  for (int i=0;i<5;i++)
  {   
    digitalWrite (LED_PIN, HIGH) ; delay (100) ;
    digitalWrite (LED_PIN,  LOW) ; delay (100) ;
  }
  printf("hihi");
  return 0 ;
}