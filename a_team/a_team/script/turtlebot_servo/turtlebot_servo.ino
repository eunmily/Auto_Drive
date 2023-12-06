#include <Servo.h>
#include <stdlib.h>


Servo tilt;

int pos_tilt = 0;

void setup() {
  Serial.begin(9600);
  tilt.attach(9);
  tilt.write(103);
}

void loop() { 
     // turn the LED off by making the voltage LOW
  //Serial.println(Serial.available());
  if(Serial.available())
  { 
    char ch = Serial.read();
    if(ch == '1')
    {
      tilt.write(100);
    }
    else if(ch == '2')
    {
      tilt.write(50);
    }
    else;


    
  } 
}
