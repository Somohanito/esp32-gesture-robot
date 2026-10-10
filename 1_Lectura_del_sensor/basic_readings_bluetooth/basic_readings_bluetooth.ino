#include <BluetoothSerial.h>

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>


#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

#if !defined(CONFIG_BT_SPP_ENABLED)
#error Serial Bluetooth not available or not enabled. It is only available for the ESP32 chip.
#endif

BluetoothSerial SerialBT;


Adafruit_MPU6050 mpu;

void setup(void) {
  
  SerialBT.begin("SensorMPU6050");

  if (!mpu.begin()) {
    SerialBT.println("Error al encontrar el chip MPU6050");
    while (1) {
      delay(10);
    }
  }


  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  
  SerialBT.println("");
  delay(100);
  
}

void loop() {
  
  /* Obtener nuevas lecturas del sensor*/
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  /* Imprime los valores */
  SerialBT.print("AccelX:");
  SerialBT.print(a.acceleration.x);
  SerialBT.print(",");
  SerialBT.print("AccelY:");
  SerialBT.print(a.acceleration.y);
  SerialBT.print(",");
  SerialBT.print("AccelZ:");
  SerialBT.print(a.acceleration.z);
  SerialBT.print(", ");
  SerialBT.print("GyroX:");
  SerialBT.print(g.gyro.x);
  SerialBT.print(",");
  SerialBT.print("GyroY:");
  SerialBT.print(g.gyro.y);
  SerialBT.print(",");
  SerialBT.print("GyroZ:");
  SerialBT.print(g.gyro.z);
  SerialBT.println("");
  
  delay(200);
}
