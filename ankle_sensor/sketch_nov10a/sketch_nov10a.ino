#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

Adafruit_MPU6050 mpu;

void setup() {
  Serial.begin(9600);
  
  // Initialize the MPU6050
  if (!mpu.begin()) {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    while (1);
  }

  Serial.println("MPU6050 Found!");
}

void loop() {
  // Get sensor data
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Send data in JSON format
  Serial.print("{\"accX\": ");
  Serial.print(a.acceleration.x);
  Serial.print(", \"accY\": ");
  Serial.print(a.acceleration.y);
  Serial.print(", \"accZ\": ");
  Serial.print(a.acceleration.z);
  Serial.print(", \"gyroX\": ");
  Serial.print(g.gyro.x);
  Serial.print(", \"gyroY\": ");
  Serial.print(g.gyro.y);
  Serial.print(", \"gyroZ\": ");
  Serial.print(g.gyro.z);
  Serial.println("}");

  delay(1000);  // Wait 1 second before sending new data
}
