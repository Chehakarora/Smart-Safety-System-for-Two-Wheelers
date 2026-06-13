#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <MPU6050.h>
#include <TinyGPS++.h>
#include <math.h>

// ------------ PINS ------------
#define FSR_PIN 34
#define RELAY 27
#define LDR_PIN 32

#define HEADLIGHT1 14
#define HEADLIGHT2 12

#define TRIG_PIN 5
#define ECHO_PIN 18

#define GREEN_LED 25
#define YELLOW_LED 26
#define RED_LED 23
#define BUZZER 19

#define CANCEL_BUTTON 4

LiquidCrystal_I2C lcd(0x27, 16, 2);
MPU6050 mpu;

// ------------ GPS ------------
TinyGPSPlus gps;
HardwareSerial GPSserial(2);

// ------------ VARIABLES ------------
bool accidentMode = false;
unsigned long accidentStartTime = 0;
unsigned long lastBeepTime = 0;

void setup() {
  Serial.begin(115200);

  pinMode(FSR_PIN, INPUT);
  pinMode(RELAY, OUTPUT);
  pinMode(LDR_PIN, INPUT);

  pinMode(HEADLIGHT1, OUTPUT);
  pinMode(HEADLIGHT2, OUTPUT);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  pinMode(GREEN_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  pinMode(CANCEL_BUTTON, INPUT_PULLUP);

  digitalWrite(RELAY, HIGH);

  Wire.begin(21,22);
  lcd.init();
  lcd.backlight();

  mpu.initialize();

  // GPS INIT
  GPSserial.begin(9600, SERIAL_8N1, 16, 17);

  lcd.setCursor(0,0);
  lcd.print("SMART BIKE");
  delay(2000);
  lcd.clear();
}

void loop() {

  // -------- GPS READ --------
  while (GPSserial.available()) {
    gps.encode(GPSserial.read());
  }

  // ================= HELMET =================
  int fsrValue = analogRead(FSR_PIN);
  bool helmetWorn = (fsrValue > 500);

  if (!helmetWorn) {
    digitalWrite(RELAY, HIGH);
    lcd.setCursor(0,0);
    lcd.print("Wear Helmet   ");
    lcd.setCursor(0,1);
    lcd.print("Engine Locked ");
    delay(200);
    return;
  }

  digitalWrite(RELAY, LOW);

  // ================= LDR =================
  int ldrState = digitalRead(LDR_PIN);
  if (ldrState == 1) {
    digitalWrite(HEADLIGHT1, HIGH);
    digitalWrite(HEADLIGHT2, HIGH);
  } else {
    digitalWrite(HEADLIGHT1, LOW);
    digitalWrite(HEADLIGHT2, LOW);
  }

  // ================= ULTRASONIC =================
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(5);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 25000);
  float distance;

  if (duration == 0) distance = 999;
  else distance = (duration * 0.0343) / 2;

  if (distance < 2 || distance > 400) distance = 999;

  if (distance > 85) {
    digitalWrite(GREEN_LED, HIGH);
    digitalWrite(YELLOW_LED, LOW);
    digitalWrite(RED_LED, LOW);
    digitalWrite(BUZZER, LOW);
  }
  else if (distance > 40) {
    digitalWrite(GREEN_LED, LOW);
    digitalWrite(YELLOW_LED, HIGH);
    digitalWrite(RED_LED, LOW);

    digitalWrite(BUZZER, HIGH);
    delay(250);
    digitalWrite(BUZZER, LOW);
    delay(250);
  }
  else {
    digitalWrite(GREEN_LED, LOW);
    digitalWrite(YELLOW_LED, LOW);
    digitalWrite(RED_LED, HIGH);

    digitalWrite(BUZZER, HIGH);
    delay(120);
    digitalWrite(BUZZER, LOW);
    delay(120);
  }

  // ================= MPU =================
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);

  float ax_g = ax / 16384.0;
  float ay_g = ay / 16384.0;
  float az_g = az / 16384.0;

  float angle = atan2(
      sqrt(ax_g * ax_g + ay_g * ay_g),
      az_g
  ) * 180.0 / PI;

  // ================= ACCIDENT TRIGGER =================
  if (angle > 75 && !accidentMode) {
    accidentMode = true;
    accidentStartTime = millis();
  }

  // ================= ACCIDENT MODE =================
  if (accidentMode) {

    unsigned long elapsed = millis() - accidentStartTime;
    unsigned long remaining = 60000 - elapsed;

    int seconds = remaining / 1000;
    int mins = seconds / 60;
    int secs = seconds % 60;

    lcd.setCursor(0,0);
    lcd.print("Accident Alert!     ");
    lcd.setCursor(0,1);

    if (secs < 10)
      lcd.print(String(mins) + ":0" + String(secs) + " Cancel?");
    else
      lcd.print(String(mins) + ":" + String(secs) + " Cancel?");

    digitalWrite(RELAY, HIGH);
    digitalWrite(RED_LED, HIGH);

    // BUZZER
    if (millis() - lastBeepTime > 500) {
      digitalWrite(BUZZER, HIGH);
      delay(100);
      digitalWrite(BUZZER, LOW);
      lastBeepTime = millis();
    }

    // Cancel button
    if (digitalRead(CANCEL_BUTTON) == LOW) {
      accidentMode = false;
      digitalWrite(BUZZER, LOW);
      digitalWrite(RED_LED, LOW);
    }

    // FINAL ALERT
    if (remaining <= 0) {

      lcd.setCursor(0,0);
      lcd.print("EMERGENCY !!! ");

      digitalWrite(BUZZER, HIGH);
      delay(3000);
      digitalWrite(BUZZER, LOW);

      String location;

      if (gps.location.isValid()) {
        location = String(gps.location.lat(), 6) + "," +
                   String(gps.location.lng(), 6);
      } else {
        location = "0,0";
      }

      Serial.print("ACCIDENT:");
      Serial.println(location);

      accidentMode = false;
    }

    return;
  }

  // ================= NORMAL =================
  lcd.setCursor(0,0);
  lcd.print("Dist:");
  lcd.print(distance);
  lcd.print("cm   ");

  lcd.setCursor(0,1);
  lcd.print("Angle:");
  lcd.print(angle);
  lcd.print("   ");

  delay(150);
}
