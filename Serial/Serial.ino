#include <Servo.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <gfxfont.h>

#define OLED_RESET 4
Adafruit_SSD1306 display(OLED_RESET);

#define NUMFLAKES 10
#define XPOS 0
#define YPOS 1
#define DELTAY 2

#define LOGO16_GLCD_HEIGHT 16 
#define LOGO16_GLCD_WIDTH  16 
static const unsigned char PROGMEM logo16_glcd_bmp[] =
{ B00000000, B11000000,
  B00000001, B11000000,
  B00000001, B11000000,
  B00000011, B11100000,
  B11110011, B11100000,
  B11111110, B11111000,
  B01111110, B11111111,
  B00110011, B10011111,
  B00011111, B11111100,
  B00001101, B01110000,
  B00011011, B10100000,
  B00111111, B11100000,
  B00111111, B11110000,
  B01111100, B11110000,
  B01110000, B01110000,
  B00000000, B00110000 };

#if (SSD1306_LCDHEIGHT != 32)
#error("Height incorrect, please fix Adafruit_SSD1306.h!");
#endif

Servo myservo;

int i =0;
int led = 13;
int lastVolume = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(led, OUTPUT);
  digitalWrite(led,LOW);

  //servo stuff:
  myservo.attach(9);
  int servoPos = 0;

  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  // initialize with the I2C addr 0x3C (for the 128x32)

  display.display();
  delay(2000);
  display.clearDisplay();
  display.display();
}

void loop() {
  // put your main code here, to run repeatedly:
 //Serial.println(i);
  //i++;

  if(Serial.available()>0){
     char msg = Serial.read();
     if(msg == '1'){
      digitalWrite(led,HIGH);
     }
     else if(msg == 'V'){
      delay(10);
      
      char volume = Serial.read();
      
      
      if(abs(volume-lastVolume) > 10) return;
      
      drawProgress(int(volume));
      display.display();
      
      lastVolume = volume;
     }
     else{
      digitalWrite(led, LOW);
     }
  }
}

void writeNumber(int num){
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.setCursor(0,0);

  display.write(num);

  display.display();
}
void drawProgress(int progress){
  double width = (100/progress)*display.width();
  display.clearDisplay();
 //display.fillRect(0,0,int(width),display.height(), WHITE);
 
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.setCursor(50,15);

  display.print(progress);
}

