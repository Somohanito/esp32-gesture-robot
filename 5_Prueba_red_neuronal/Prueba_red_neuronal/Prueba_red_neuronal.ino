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

///////////////////////////////// Variables Red Neuronal /////////////////////////////////
double a0[3];
double W1[2][3] = {{-6.16,-6.646,-2.776},{4.442,-7.092,-1.373}};
double a1[2];
double W2[5][2] = {{-8.495,-26.6},{2.687,2.597},{-28.226,5.705},{8.409,-31.872},{-0.859,-2.993}};
double a2[5]; 
double b1[2]= {2.48,3.12};
double b2[5]= {31.694,-26.682,-2.053,-1.107,15.058};
double aux = 0.0;
//////////////////////////////////////////////////////////////////



///////////////////////////////// Preprocesamiento Red Neuronal /////////////////////////////////
double mean[3]={-0.2,3.734,5.639};
double dstd[3]={4.699,4.172,3.494};
///////////////////////////////////////////////////////////////////////////////////////////////////////

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
  
  delay(100);
}

void loop() {
  
  sensors_event_t a, g, t;
  mpu.getEvent(&a, &g, &t);

  a0[0]=dataNormalized(a.acceleration.x,mean[0],dstd[0]);
  a0[1]=dataNormalized(a.acceleration.y,mean[1],dstd[1]);
  a0[2]=dataNormalized(a.acceleration.z,mean[2],dstd[2]);
  
  ///////////////////////////////// Estructura Red Neuronal /////////////////////////////////
  for(int i = 0 ; i<2; i++ ) {aux=0.0;for(int j = 0 ; j <3 ; j++ ) { aux=aux+W1[i][j]*a0[j];} a1[i]=relu(aux+b1[i]);}
  double aux1 = 0;
  for(int i = 0 ; i<5; i++ ) {aux=0.0;for(int j = 0 ; j <2 ; j++ ){ aux=aux+W2[i][j]*a1[j];} a2[i]=(aux+b2[i]);aux1=aux1+exp(a2[i]);}
  double minimo = 0.0;
  int classes = 0;
  for(int i = 0;  i<5; i++){a2[i] = exp(a2[i])/aux1;if(a2[i]>minimo){minimo=a2[i];classes=i;}}
  //////////////////////////////////////////////////////////////////////////////////////////
  
  SerialBT.println(classes+1);   
  
  delay(200);
}

double dataNormalized(double inputData, double mean, double desvStandar)
{
  return (inputData-mean)/desvStandar; 
}

double relu(double n)
{
  if(n>=0) return n; else if (n<0) return 0;
}
