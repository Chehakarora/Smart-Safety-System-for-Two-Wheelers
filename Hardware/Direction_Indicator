#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define LEFT_LED 13
#define RIGHT_LED 33
#define BUTTON 15

LiquidCrystal_I2C lcd(0x27, 16, 2);

String incoming = "";
String currentDirection = "";   //remembers last direction
bool overrideActive = false;

void setup() {
  Serial.begin(115200);

  lcd.init();
  lcd.backlight();

  pinMode(LEFT_LED, OUTPUT);
  pinMode(RIGHT_LED, OUTPUT);
  pinMode(BUTTON, INPUT_PULLUP);
lcd.setCursor(0,0);
  lcd.print("Ready");
}
void loop() {
  //  Button → turn OFF LEDs and keep them OFF
  if (digitalRead(BUTTON) == LOW) {
   overrideActive = true;
    digitalWrite(LEFT_LED, LOW);
    digitalWrite(RIGHT_LED, LOW);
delay(200); // debounce
  }

  // Receive serial only; don't touch LEDs here
  while (Serial.available()) {
    char c = Serial.read();

    if (c == '\n') {
      processCommand(incoming);
      incoming = "";
    } else {
      incoming += c;
    }
  }
}

void processCommand(String cmd) {
  int comma = cmd.indexOf(',');
  if (comma == -1) return;

  String direction = cmd.substring(0, comma);
  String distance = cmd.substring(comma + 1);
// new step → reset override and update direction
  overrideActive = false;
  currentDirection = direction;
 // LCD 
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(direction);
  lcd.setCursor(0,1);
  lcd.print(distance );
//Update LEDs ONLY HERE (on new command)
  if (!overrideActive) {
    if (currentDirection == "LEFT") {
      digitalWrite(LEFT_LED, HIGH);
      digitalWrite(RIGHT_LED, LOW);
    }
    else if (currentDirection == "RIGHT") {
      digitalWrite(LEFT_LED, LOW);
      digitalWrite(RIGHT_LED, HIGH);
    }
    else {
      digitalWrite(LEFT_LED, LOW);
      digitalWrite(RIGHT_LED, LOW);
    }
  }
}
