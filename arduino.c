/*********************************************************************
 This is an example for our nRF51822 based Bluefruit LE modules

 Pick one up today in the adafruit shop!

 Adafruit invests time and resources providing this open source code,
 please support Adafruit and open-source hardware by purchasing
 products from Adafruit!

 MIT license, check LICENSE for more information
 All text above, and the splash screen below must be included in
 any redistribution
*********************************************************************/

#include <Arduino.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM9DS0.h>

#include "Adafruit_BLE.h"
#include "BluefruitConfig.h"
#include "Adafruit_BluefruitLE_SPI.h"
#include "Adafruit_BluefruitLE_UART.h"
#if SOFTWARE_SERIAL_AVAILABLE
  #include <SoftwareSerial.h>
#endif

#include "BluefruitConfig.h"

Adafruit_BluefruitLE_UART ble(Serial1, BLUEFRUIT_UART_MODE_PIN);

Adafruit_LSM9DS0 lsm = Adafruit_LSM9DS0(1000);  // Use I2C, ID #1000

/**************************************************************************/
/*!
    @brief  A small helper function for error messages
*/
/**************************************************************************/
void error(const __FlashStringHelper*err)
{
  Serial.println(err);
  while (1);
}

/**************************************************************************/
/*
    Displays some basic information on this sensor from the unified
    sensor API sensor_t type (see Adafruit_Sensor for more information)
*/
/**************************************************************************/
void displaySensorDetails(void)
{
  sensor_t accel, mag, gyro, temp;

  lsm.getSensor(&accel, &mag, &gyro, &temp);

  Serial.println(F("------------------------------------"));
  Serial.print  (F("Sensor:       ")); Serial.println(accel.name);
  Serial.print  (F("Driver Ver:   ")); Serial.println(accel.version);
  Serial.print  (F("Unique ID:    ")); Serial.println(accel.sensor_id);
  Serial.print  (F("Max Value:    ")); Serial.print(accel.max_value); Serial.println(F(" m/s^2"));
  Serial.print  (F("Min Value:    ")); Serial.print(accel.min_value); Serial.println(F(" m/s^2"));
  Serial.print  (F("Resolution:   ")); Serial.print(accel.resolution); Serial.println(F(" m/s^2"));
  Serial.println(F("------------------------------------"));
  Serial.println(F(""));

  Serial.println(F("------------------------------------"));
  Serial.print  (F("Sensor:       ")); Serial.println(mag.name);
  Serial.print  (F("Driver Ver:   ")); Serial.println(mag.version);
  Serial.print  (F("Unique ID:    ")); Serial.println(mag.sensor_id);
  Serial.print  (F("Max Value:    ")); Serial.print(mag.max_value); Serial.println(F(" uT"));
  Serial.print  (F("Min Value:    ")); Serial.print(mag.min_value); Serial.println(F(" uT"));
  Serial.print  (F("Resolution:   ")); Serial.print(mag.resolution); Serial.println(F(" uT"));
  Serial.println(F("------------------------------------"));
  Serial.println(F(""));

  Serial.println(F("------------------------------------"));
  Serial.print  (F("Sensor:       ")); Serial.println(gyro.name);
  Serial.print  (F("Driver Ver:   ")); Serial.println(gyro.version);
  Serial.print  (F("Unique ID:    ")); Serial.println(gyro.sensor_id);
  Serial.print  (F("Max Value:    ")); Serial.print(gyro.max_value); Serial.println(F(" rad/s"));
  Serial.print  (F("Min Value:    ")); Serial.print(gyro.min_value); Serial.println(F(" rad/s"));
  Serial.print  (F("Resolution:   ")); Serial.print(gyro.resolution); Serial.println(F(" rad/s"));
  Serial.println(F("------------------------------------"));
  Serial.println(F(""));

  Serial.println(F("------------------------------------"));
  Serial.print  (F("Sensor:       ")); Serial.println(temp.name);
  Serial.print  (F("Driver Ver:   ")); Serial.println(temp.version);
  Serial.print  (F("Unique ID:    ")); Serial.println(temp.sensor_id);
  Serial.print  (F("Max Value:    ")); Serial.print(temp.max_value); Serial.println(F(" C"));
  Serial.print  (F("Min Value:    ")); Serial.print(temp.min_value); Serial.println(F(" C"));
  Serial.print  (F("Resolution:   ")); Serial.print(temp.resolution); Serial.println(F(" C"));
  Serial.println(F("------------------------------------"));
  Serial.println(F(""));

  delay(500);
}

/**************************************************************************/
/*!
    @brief  Initializes the one wire temperature sensor
*/
/**************************************************************************/
void initSensor(void)
{
  //#ifndef ESP8266
  //while (!Serial);     // will pause Zero, Leonardo, etc until serial console opens
  //#endif
  Serial.begin(9600);
  Serial.println(F("LSM9DS0 9DOF Sensor Test")); Serial.println("");

  /* Initialise the sensor */
  if(!lsm.begin())
  {
    /* There was a problem detecting the LSM9DS0 ... check your connections */
    Serial.print(F("Ooops, no LSM9DS0 detected ... Check your wiring or I2C ADDR!"));
    while(1);
  }
  Serial.println(F("Found LSM9DS0 9DOF"));

  delay(1000);

  // Display some basic information on this sensor
  displaySensorDetails();
}

/**************************************************************************/
/*
    Configures the gain and integration time for the TSL2561
*/
/**************************************************************************/
void configureSensor(void)
{
  // 1.) Set the accelerometer range
  lsm.setupAccel(lsm.LSM9DS0_ACCELRANGE_2G);
  //lsm.setupAccel(lsm.LSM9DS0_ACCELRANGE_4G);
  //lsm.setupAccel(lsm.LSM9DS0_ACCELRANGE_6G);
  //lsm.setupAccel(lsm.LSM9DS0_ACCELRANGE_8G);
  //lsm.setupAccel(lsm.LSM9DS0_ACCELRANGE_16G);

  // 2.) Set the magnetometer sensitivity
  lsm.setupMag(lsm.LSM9DS0_MAGGAIN_2GAUSS);
  //lsm.setupMag(lsm.LSM9DS0_MAGGAIN_4GAUSS);
  //lsm.setupMag(lsm.LSM9DS0_MAGGAIN_8GAUSS);
  //lsm.setupMag(lsm.LSM9DS0_MAGGAIN_12GAUSS);

  // 3.) Setup the gyroscope
  lsm.setupGyro(lsm.LSM9DS0_GYROSCALE_245DPS);
  //lsm.setupGyro(lsm.LSM9DS0_GYROSCALE_500DPS);
  //lsm.setupGyro(lsm.LSM9DS0_GYROSCALE_2000DPS);
}

/**************************************************************************/
/*!
    @brief  Sets up the HW an the BLE module (this function is called
            automatically on startup)
*/
/**************************************************************************/
void setup(void)
{
  //while (!Serial);  // required for Flora & Micro
  //delay(500);

  Serial.begin(9600);
  Serial.println(F("Adafruit Bluefruit Command Mode Example"));
  Serial.println(F("---------------------------------------"));

  // Init sensor
  initSensor();

  /* Setup the sensor gain and integration time */
  configureSensor();

  // Initialise the module
  Serial.print(F("Initialising the Bluefruit LE module: "));

  if ( !ble.begin(VERBOSE_MODE) )
  {
    error(F("Couldn't find Bluefruit, make sure it's in CoMmanD mode & check wiring?"));
  }
  Serial.println( F("OK!") );

  // Perform a factory reset to make sure everything is in a known state
  Serial.println(F("Performing a factory reset: "));
  if (! ble.factoryReset() ){
       error(F("Couldn't factory reset"));
  }

  // Disable command echo from Bluefruit
  ble.echo(false);

  Serial.println("Requesting Bluefruit info:");
  // Print Bluefruit information
  ble.info();

  ble.verbose(false);  // debug info is a little annoying after this point!

  // Setup the BNO055 sensor
  initSensor();

  Serial.println("Waiting for a BLE connection to continue ...");

  // Wait for connection to finish
  while (! ble.isConnected()) {
      delay(5000);
  }

  Serial.println(F("CONNECTED!"));
  Serial.println(F("**********"));
}

/**************************************************************************/
/*!
    @brief  Constantly poll for new command or response data
*/
/**************************************************************************/
void loop(void)
{
  // Check for user input
  char inputs[BUFSIZE+1];

  // Send sensor data out
  if (ble.isConnected())
  {
    /* Get a new sensor event */
  sensors_event_t accel, mag, gyro, temp;

  lsm.getEvent(&accel, &mag, &gyro, &temp);

  // Display the full data in Serial Monitor

  // print out accelleration data
  //Serial.print("Accel X: "); Serial.print(accel.acceleration.x); Serial.print(" ");
  //Serial.print("  \tY: "); Serial.print(accel.acceleration.y);       Serial.print(" ");
  //Serial.print("  \tZ: "); Serial.print(accel.acceleration.z);     Serial.println("  \tm/s^2");

  // print out magnetometer data
  //Serial.print("Magn. X: "); Serial.print(mag.magnetic.x); Serial.print(" ");
  //Serial.print("  \tY: "); Serial.print(mag.magnetic.y);       Serial.print(" ");
  //Serial.print("  \tZ: "); Serial.print(mag.magnetic.z);     Serial.println("  \tgauss");

  // print out gyroscopic data
  //Serial.print("Gyro  X: "); Serial.print(gyro.gyro.x); Serial.print(" ");
  //Serial.print("  \tY: "); Serial.print(gyro.gyro.y);       Serial.print(" ");
  //Serial.print("  \tZ: "); Serial.print(gyro.gyro.z);     Serial.println("  \tdps");

  // print out temperature data
  //Serial.print("Temp: "); Serial.print(temp.temperature); Serial.println(" *C");

  //Serial.println("**********************\n");



    // Send abbreviated integer data out over BLE UART
    /*ble.print("AT+BLEUARTTX=[");
    ble.print(gyro.gyro.x, 2);
    ble.print(",");
    ble.print(gyro.gyro.y, 2);
    ble.print(",");
    ble.print(gyro.gyro.z, 2);
    ble.print(",");
    ble.print(accel.acceleration.x, 2);
    ble.print(",");
    ble.print(accel.acceleration.y, 2);
    ble.print(",");
    ble.print(accel.acceleration.z, 2);
    ble.print(",");
    ble.println(temp.temperature, 2);
    ble.print("]");*/

    /*ble.println("AT+BLEUARTTX=[" +
        String(gyro.gyro.x) + "," +
        String(gyro.gyro.y) + "," +
        String(gyro.gyro.z) + "," +
        String(accel.acceleration.x) + "," +
        String(accel.acceleration.y) + "," +
        String(accel.acceleration.z) + "," +
        String(mag.magnetic.x) + "," +
        String(mag.magnetic.y) + "," +
        String(mag.magnetic.z) + "," +
        String(temp.temperature) + "]");*/

     ble.println("AT+BLEUARTTXF=[" +
        String(accel.acceleration.x) + "," +
        String(accel.acceleration.y) + "," +
        String(accel.acceleration.z) + "]");

    Serial.println("AT+BLEUARTTXF=[" +
        String(accel.acceleration.x) + "," +
        String(accel.acceleration.y) + "," +
        String(accel.acceleration.z) + "]");

    if (! ble.waitForOK() )
    {
      Serial.println(F("Failed to send1?"));
    }

    if (! ble.waitForOK() )
    {
      Serial.println(F("Failed to send2?"));
    }


    // Display the buffer size (firmware 0.6.7 and higher only!)
    /*ble.println("AT+BLEUARTFIFO=TX");
    ble.readline();
    Serial.print("TX FIFO: ");
    Serial.println(ble.buffer);*/


    // Wait a bit ...
    delay(50);
  }

  // Check for incoming characters from Bluefruit
  if (ble.isConnected())
  {
    ble.println("AT+BLEUARTRX");
    ble.readline();
    if (strcmp(ble.buffer, "OK") == 0) {
      // no data
      return;
    }
    // Some data was found, its in the buffer
    Serial.print(F("[Recv] ")); Serial.println(ble.buffer);
    ble.waitForOK();
  }
}