# Import section
# Main thread
from threading import Thread
import time
import RPi.GPIO as IO
from gpiozero import LED
from pprint import pprint
from menu import menuCreatorObject
import serial
import socket
import select
import binascii
import can
import os
import curses

import signal
import sys

# Bluetooth thread
import bluetooth

# SPI thread
import time
import spidev

# Logging for tests
import logging

# Logging into JSON
import json

import subprocess as sp

# Adafruit Flora
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART

# Prepare global variables
global transportData1
global transportData2
global transportData3
global transportData4
global transportDataGroup
global nodeDataBase
global testPackage
global newDataFlag
global uartBTOK
global uartGPSOK
global actRFIDSettings
global sock
global client_sock
global haveSocketOpened
global logFileName
global isLogging
global dateTimeYear
global dateTimeMonth
global dateTimeDay
global dateTimeHour
global dateTimeMin
global dateTimeSec
global lat
global lon
global latTarget
global lonTarget
global altitude
global speed
global fixedGPS
global gsmQuality
global gsmOperator
global messageNumber
global bluetoothConnected
global idCollector
global idPacket
global alarmState
global alarmContent
global haltThreadFlag

global gyroY
global gyroP
global gyroR

global accelX
global accelY
global accelZ

global menuCreator

global ble

idCollector = 11
idPacket = 1
transportData1 = 0
transportData2 = 0
transportData3 = 0
transportData4 = 0
transportDataGroup = []
nodeDataBase = []
testPackage = []
allDataPackage = []
newDataFlag = False
uartBTOK = False
uartGPSOK = False
haveSocketOpened = False
logFileName = "hrrLogFile_0"
isLogging = False
messageNumber = 0

dateTimeYear = "0"
dateTimeMonth = "0"
dateTimeDay = "0"
dateTimeHour = "0"
dateTimeMin = "0"
dateTimeSec = "0"
lat = "0.0"
lon = "0.0"
latTarget = "47.68472"
lonTarget = "16.58306"
altitude = "0.0"
speed = "0.0"
fixedGPS = False
gsmQuality = 255
gsmOperator = "SteinCom"
alarmState = 0
alarmContent = ""
haltThreadFlag = False

accelX = 0
accelY = 0
accelZ = 0

gyroY = 0
gyroP = 0
gyroR = 0

bluetoothConnected = False

# Prepare SPI variables
# We only have SPI bus 0 available to us on the Pi
bus = 0

# Device is the chip select pin. Set to 0 or 1, depending on the connections
geckoDevice = 0
canDevice = 1

# Enable SPI
spi = spidev.SpiDev()

# Open a connection to a specific bus and device (chip select pin)
spi.open(bus, geckoDevice)

# Set SPI speed and mode
spi.max_speed_hz = 5000000
spi.mode = 0

# Init intou and output ports
IO.setwarnings(False)  # Ignore warning for now
IO.setmode(IO.BCM)
IO.setup(5, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(6, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(12, IO.IN, pull_up_down=IO.PUD_UP)
SIMEnFlag = LED(18)

zummer = LED(13)
led_red = LED(16)
led_green = LED(20)
led_blue = LED(21)
zummer.off()
led_red.off()
led_green.on()
led_blue.on()


# logging.info("Informational message")
# logging.debug("Helpful debugging info")
# logging.error("Something bad happened")

import os

##TEST## os.system('sudo systemctl start bluetooth')
##TEST## os.system('sudo hciconfig hci0 piscan')
# SET the time in OS SHELL script: os.system('date -s '2014-12-25 12:34:56'')


class BluetoothServer:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global transportData1
        global transportData2
        global transportData3
        global transportData4
        global transportDataGroup
        global actSettings
        global recSettings
        global newDataFlag
        global bluetoothConnected

        global haltThreadFlag

        while not haltThreadFlag:
            print('OPENING socket')
            try:
                server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                port = 1
                server_sock.bind(("", port))
                server_sock.listen(1)
                client_sock, address = server_sock.accept()

                print('Accepted connection from ', address)
                bluetoothConnected = True
                #led_red.on()
                #led_green.off()
                while self._running:
                    try:
                        # data = client_sock.recv(1024)
                        # print ("received [%s]" % data)

                        if (newDataFlag == True):
                            try:
                                newDataFlag = False
                                print('There are new Data -> Send to Bluetooth')
                                client_sock.sendall(''.join(format(x, '02x') for x in transportDataGroup))
                                client_sock.sendall("\r\n")
                            except Exception as e:
                                newDataFlag = False
                                print(e)
                                print('Enable to send')
                                # Exception saving to the log file
                                writeLogFileError("Exception while send data to bluetooth!")
                                break

                    except:
                        print('Enable to receive')
                        writeLogFileError("Exception disable the bluetooth communication")
                        break

                print("Closing socket")
                client_sock.close()
                server_sock.close()
                bluetoothConnected = False

            except:
                writeLogFileError("Exception while connection to the bluetooth")
                print("Closing socket")
                client_sock.close()
                server_sock.close()
                bluetoothConnected = False

class AdafruitBLEServer:
    def __init__(self):
        global ble
        ble = Adafruit_BluefruitLE.get_provider()

        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global ble
        global haltThreadFlag

        # Initialize the BLE system.  MUST be called before other BLE calls!
        ble.initialize()

        # Clear any cached data because both bluez and CoreBluetooth have issues with
        # caching data and it going stale.
        ble.clear_cached_data()

        # Get the first available BLE network adapter and make sure it's powered on.
        adapter = ble.get_default_adapter()
        adapter.power_on()
        print('Using adapter: {0}'.format(adapter.name))

        # Disconnect any currently connected UART devices.  Good for cleaning up and
        # starting from a fresh state.
        print('Disconnecting any connected UART devices...')
        UART.disconnect_devices()

        # Scan for UART devices.
        print('Searching for UART device...')
        try:
            adapter.start_scan()
            # Search for the first UART device found (will time out after 60 seconds
            # but you can specify an optional timeout_sec parameter to change it).
            device = UART.find_device()
            if device is None:
                raise RuntimeError('Failed to find UART device!')
        finally:
            # Make sure scanning is stopped before exiting.
            adapter.stop_scan()

        print('Connecting to device...')
        device.connect()  # Will time out after 60 seconds, specify timeout_sec parameter
        # to change the timeout.

        # Once connected do everything else in a try/finally to make sure the device
        # is disconnected when done.
        try:
            # Wait for service discovery to complete for the UART service.  Will
            # time out after 60 seconds (specify timeout_sec parameter to override).
            print('Discovering services...')
            UART.discover(device)

            # Once service discovery is complete create an instance of the service
            # and start interacting with it.
            uart = UART(device)

            while not haltThreadFlag:
                # Now wait up to one minute to receive data from the device.
                # print('Waiting up to 60 seconds to receive data from the device...')
                received = uart.read()

                received = "[3,-1.90,-0.28,-9.63]"

                nodeIdNumber = 0
                accX = 0.0
                accY = 0.0
                accZ = 0.0

                if received is not None:
                    # Received data, print it ou
                    print(received)
                    # Parse the data -- [3,-1.90,-0.28,-9.63]
                    paramsList = str(received)
                    params = paramsList.split(',')
                    nodeIdNumber = int(params[0][1:])
                    accX = float(params[1])
                    accY = float(params[2])
                    if params[3][len(params[3])-1] == ']':
                        accZ = float(params[3][:len(params[3])-1])
                    else:
                        accZ = float(params[3])
                    print("num: " + str(nodeIdNumber) + " accX: " + str(accX) + " accY: " + str(accY) + " accZ: " + str(accZ))
                    #Set live Bluetooth Data
                    menuCreator.set_BT_Livedata(nodeIdNumber,
                                    accX,
                                    accY,
                                    accZ,
                                    0,
                                    0,
                                    0,
                                    0,
                                    0,
                                    0,
                                    0,
                                    100,
                                    25)
                else:
                    # Timeout waiting for data, None is returned.
                    print('Received no data!')
        finally:
            # Make sure device is disconnected on exit.
            device.disconnect()

class GPSUARTConnection:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global serGPS
        global uartGPSOK
        global sock
        global haltThreadFlag

        if uartGPSOK == True:
            try:
                time.sleep(1)
                serialmessage = str.encode('AT\r\n')
                serGPS.write(serialmessage)
                time.sleep(2)
                #print("Read from GPS:" + serialmessage)
                x = serGPS.readline()
                #print("Feedback from GPS : " + x)
                writeINFOLogFile("GPS - AT:" + x)
                SocketServerClass.sendSocketMessage(x)
                time.sleep(2)
                x = serGPS.readline()
                #print(x)
                writeINFOLogFile("GPS - AT2:" + x)
                SocketServerClass.sendSocketMessage(x)

                time.sleep(1)
                serialmessage = str.encode('AT+CGNSPWR=1\r\n')
                serGPS.write(serialmessage)
                time.sleep(2)
                x = serGPS.readline()
                #print(x)
                writeINFOLogFile("GPS - AT+CGNSPWR=1:" + x)
                SocketServerClass.sendSocketMessage(x)
                time.sleep(2)
                x = serGPS.readline()
                #print(x)
                writeINFOLogFile("GPS - AT+CGNSPWR2:" + x)
                SocketServerClass.sendSocketMessage(x)



                while not haltThreadFlag:
                    time.sleep(1)
                    serialmessage = str.encode('AT+CGNSINF\r\n')
                    serGPS.write(serialmessage)
                    time.sleep(2)
                    x = serGPS.readline()
                    #print(x)
                    #writeINFOLogFile("GPS - AT+CGNSINF1:" + x)
                    SocketServerClass.sendSocketMessage(x)
                    time.sleep(2)
                    x = serGPS.readline()
                    #print(x)
                    #writeINFOLogFile("GPS - AT+CGNSINF2:" + x)
                    getCoord(x)
                    SocketServerClass.sendSocketMessage(x)
            except Exception as e:
                print("Error using GPS serial port - " + str(e))
                writeLogFileError("ERROR;GPS error while using serial port for GPS:" + str(e))
                serGPS.close()
                uartGPSOK = False
        else:
            time.sleep(5)
            self.initGPS()
            self.run()

    def initGPS(self):
        global uartGPSOK
        global serGPS
        # SIMEnFlag.on()
        time.sleep(1)
        print('OPENING serial port for GPS GSN')
        try:
            serGPS = serial.Serial(
                port='/dev/ttyS0',
                baudrate=115200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )
            uartGPSOK = True
        except:
            # SIMEnFlag.off()
            writeLogFileError("GPS - Could not open Serial port for GPS")
            print("Error opening serial port 0")
        print('GPS GSN connected succesfully')


class SerialPort:
    def __init__(self):
        global ser
        global uartBTOK
        global actRFIDSettings
        global nodeDataBase
        global actSettings
        actRFIDSettings = RfIDSettings()
        self._running = True
        self.initUART()

    def terminate(self):
        self._running = False

    def run(self):
        global ser
        global uartBTOK
        global haltThreadFlag

        while not haltThreadFlag:
            if uartBTOK == True:
                try:
                    # print("Write serial port")
                    time.sleep(1)
                    self.readAllByteUART()
                    time.sleep(1)
                    x = ser.readline()
                    self.recParamsAndNodesFromUART(x)
                    # print(x)
                except Exception as e:
                    print("Error using serial port - " + str(e))
                    writeLogFileError("RFID - Error while using serial port for RFiD reader" + str(e))
                    ser.close()
                    uartBTOK = False
            else:
                time.sleep(5)
                self.initUART()

    def readAllByteUART(self):
        global ser
        global uartBTOK
        # print('Read UART')
        CRC = ord('H') ^ ord('R') ^ ord('R') ^ 0x02 ^ 0x00 ^ 0x01 ^ 0x08 ^ ord('M') ^ ord('C') ^ 0
        msg = [ord('H'), ord('R'), ord('R'), 0x02, 0x00, 0x01, 0x08, ord('M'), ord('C'), 0x00, 0x87]
        ser.write(bytes(msg))
        time.sleep(0.00001)
        # print(bytes(msg).hex()+ "\n")
        # print("CRC - " + "0x{:02x}".format(CRC) + " \n")

    def initUART(self):
        global uartBTOK
        global ser
        # print('OPENING serial port 0')
        try:
            ser = serial.Serial(
                port='/dev/ttyUSB0',
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )
            uartBTOK = True
        except:
            writeLogFileError("RFID - error while connecting!")
            try:
                ser = serial.Serial(
                    port='/dev/ttyUSB1',
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1
                )
                uartBTOK = True
            except:
                writeLogFileError("Error in serial port module: Error opening serial port 0/1 - RFiD")

    def recParamsAndNodesFromUART(self, message):
        global actRFIDSettings
        global nodeDataBase
        global actSettings
        # print('Rec RfID params from message')
        # RfID reader ID
        actRFIDSettings.readerID = message[8:12]
        # print('Reader ID : ' + bytes(actRFIDSettings.readerID).hex() + " \n")
        # Battery of RfID reader voltage
        actRFIDSettings.batteryVoltage = message[12:14]  # 2 bytes
        # print('Battery voltage : ' + bytes(actRFIDSettings.batteryVoltage).hex() + " \n")
        # Temperature of the RfID reader
        actRFIDSettings.temperature = message[14]  # 1 byte
        # print('Device temp: ' + str(actRFIDSettings.temperature) + " \n")
        # Stored positions
        actRFIDSettings.storedPositions = message[15:31]  # 16 Bytes
        testNum = 0
        clientNum = 0
        while testNum < 7:
            if message[15 + testNum] == 0x01:
                clientNum += 1
            testNum += 1
        actSettings.numOfDevices = clientNum
        # print('Stored positions : ' + bytes(actRFIDSettings.storedPositions).hex() + " \n")
        nodeNum = 0
        while nodeNum < 7:
            actRFIDSettings.storedAddresses[nodeNum].ownAddress = message[31 + (nodeNum * 12):43 + (nodeNum * 12)]
            if actRFIDSettings.storedPositions[nodeNum] == 0x01:
                byteNum = 0
                while byteNum < 12:
                    nodeDataBase[nodeNum].txAddress[byteNum] = message[31 + (nodeNum * 12) + byteNum]
                    # print('Address ' + str(nodeDataBase[nodeNum].txAddress[byteNum]) + " \n")
                    byteNum += 1
            nodeNum += 1

class LEDStateChanges:
    def __init__(self):
        global haltThreadFlag

    def run(self):
        global bluetoothConnected
        global isLogging

        global haltThreadFlag

        while not haltThreadFlag:
            if not bluetoothConnected and not isLogging :
                led_red.on()
                led_blue.off()
                led_green.off()
            if not bluetoothConnected and isLogging :
                led_red.on()
                led_blue.off()
                led_green.on()
            if bluetoothConnected and not isLogging :
                led_red.off()
                led_blue.on()
                led_green.off()
            if bluetoothConnected and isLogging :
                led_red.off()
                led_blue.off()
                led_green.on()

            time.sleep(0.5)



class SPIReceiver:
    def __init__(self):
        global haltThreadFlag
        haltThreadFlag = False

    def terminate(self):
        global haltThreadFlag
        haltThreadFlag = True

    def run(self):
        global transportData1
        global transportData2
        global transportData3
        global transportData4
        global transportDataGroup
        global actSettings
        global testPackage
        global allDataPackage
        global recSettings
        global newDataFlag
        global haltThreadFlag

        while not haltThreadFlag:
            time.sleep(0.5)

    def sendTestPackage(self):
        print('Read 1 Byte')
        transportData1 = spi.xfer2(testPackage)
        # print("Regcontent [ Node - " + str(nodeAddress) + " Reg - " + "{0:b}".format(regAddress) + " Dummy - " + str(dummyCommand) + "] fist byte for adressing - " + "{0:b}".format(s1Byte)
        print(bytes(transportData1) + "\n")

    def serializeDataBaseToMessage(self):
        global actSettings
        global nodeDataBase
        del allDataPackage[:]
        allDataPackage.append(0x00)  # Read mode
        allDataPackage.append(actSettings.radioMode)  # Command Radio mode
        allDataPackage.append(actSettings.deviceReset)  # Device Reset
        allDataPackage.append(actSettings.trControl)  # Transfer Control
        allDataPackage.append(actSettings.numOfDevices)  # Number of Devices
        j = 0
        while j < 12:
            k = 0
            while k < 6:
                allDataPackage.append(0xff)
                k += 1
            j += 1
        while j < 15:
            k = 0
            while k < 7:
                allDataPackage.append(0xff)
                k += 1
            j += 1
        CRCforAllDataPackage = 0
        for x in allDataPackage:
            CRCforAllDataPackage = CRCforAllDataPackage ^ x
        allDataPackage.append(CRCforAllDataPackage)
        # print('to send message size'+str(len(allDataPackage)))

    def sendReadAllPackage(self):
        global transportDataGroup
        global recSettings
        # cls()
        # print('Read All Bytes')
        # prepare package
        SPIReceiver.serializeDataBaseToMessage(self)
        transportDataGroup = spi.xfer2(allDataPackage)
        SPIReceiver.readAndSaveContentOfResult(self)

    def readAndSaveContentOfResult(self):
        global transportDataGroup
        global recSettings
        global newDataFlag
        global nodeDataBase
        global menuCreator

        ### set_IR_Livedata(IR_ID_number,Distance,CountA,CountB,BattVoltage,BattPercent,Temperature)
        # set_BT_Livedata(BT_ID_number ,AccX , AccY ,AccZ , MagnX ,MagnY ,MagnZ , GyroX ,GyroY ,GyroZ ,BattV ,BattPercent , temp)
        # set_Force_Livedata(Force_ID_number ,Measured_weight,BattV,BattPercent,temperature)
        
        # print('Size of received message' + str(len(bytes(transportDataGroup))))
        # uncomment for spi package#
        ##Test##print(bytes(transportDataGroup) + "\n")
        writeINFOLogFile("Read and Save Content from SPI")
        writeINFOLogFile(''.join(format(x, '02x') for x in transportDataGroup))
        # if transportDataGroup[0] == 0xAA:
        #    print("Data message arrives from Gecko")
        recSettings.radioMode = transportDataGroup[1]
        recSettings.deviceReset = transportDataGroup[2]
        recSettings.trControl = transportDataGroup[3]
        recSettings.numOfDevices = transportDataGroup[4]
        print('Num of devices :' + str(recSettings.numOfDevices) + "\n")
        nodeNum = 0
            # Get the Line detector value 6 pieces
        while nodeNum < 6:
            nodeDataBase[nodeNum].nodeNumber = nodeNum
            nodeDataBase[nodeNum].mLDValue = transportDataGroup[(nodeNum * 6) + 5:(nodeNum * 6) + 7]
            nodeDataBase[nodeNum].vBattery = transportDataGroup[(nodeNum * 6) + 7:(nodeNum * 6) + 9]
            nodeDataBase[nodeNum].rssiValue = transportDataGroup[(nodeNum * 6) + 9]
            nodeDataBase[nodeNum].tempDevice = transportDataGroup[(nodeNum * 6) + 10]

            nodeDataBase[nodeNum].vDecBattery = nodeDataBase[nodeNum].vBattery[1] * 256 + \
                                                    nodeDataBase[nodeNum].vBattery[0]
            nodeDataBase[nodeNum].mDecLDValue = nodeDataBase[nodeNum].mLDValue[1] * 256 + \
                                                               nodeDataBase[nodeNum].mLDValue[0]

            #pprint(vars(nodeDataBase[nodeNum]))  # Comment this if the reading is too slow

            menuCreator.set_IR_Livedata(nodeDataBase[nodeNum].nodeNumber,
                                        0,
                                        nodeDataBase[nodeNum].mDecLDValue,
                                        0,
                                        nodeDataBase[nodeNum].vBattery,
                                        0,
                                        nodeDataBase[nodeNum].tempDevice)

            nodeNum += 1

            # Get the weight walue for the load
        if nodeNum == 6:
            nodeDataBase[nodeNum].nodeNumber = nodeNum
            nodeDataBase[nodeNum].mWeigthMeasure = transportDataGroup[(nodeNum * 6) + 5:(nodeNum * 6) + 7]
            nodeDataBase[nodeNum].vBattery = transportDataGroup[(nodeNum * 6) + 7:(nodeNum * 6) + 9]
            nodeDataBase[nodeNum].rssiValue = transportDataGroup[(nodeNum * 6) + 9]
            nodeDataBase[nodeNum].tempDevice = transportDataGroup[(nodeNum * 6) + 10]

            nodeDataBase[nodeNum].vDecBattery = nodeDataBase[nodeNum].vBattery[1] * 256 + \
                                                    nodeDataBase[nodeNum].vBattery[0]
            nodeDataBase[nodeNum].mDecWeigthMeasure = nodeDataBase[nodeNum].mWeigthMeasure[1] * 256 + \
                                                               nodeDataBase[nodeNum].mWeigthMeasure[0]

            #pprint(vars(nodeDataBase[nodeNum]))  # Comment this if the reading is too slow

            menuCreator.set_Force_Livedata(0,
                                           nodeDataBase[nodeNum].mDecWeigthMeasure,
                                           nodeDataBase[nodeNum].vDecBattery,
                                           0,
                                           nodeDataBase[nodeNum].tempDevice)
            
            nodeNum += 1

        if nodeNum == 7:
            nodeDataBase[nodeNum].nodeNumber = nodeNum
            nodeDataBase[nodeNum].mWeigthMeasureStand1 = transportDataGroup[(nodeNum * 6) + 5:(nodeNum * 6) + 7]
            nodeDataBase[nodeNum].vBattery = transportDataGroup[(nodeNum * 6) + 7:(nodeNum * 6) + 9]
            nodeDataBase[nodeNum].rssiValue = transportDataGroup[(nodeNum * 6) + 9]
            nodeDataBase[nodeNum].tempDevice = transportDataGroup[(nodeNum * 6) + 10]

            nodeDataBase[nodeNum].vDecBattery = nodeDataBase[nodeNum].vBattery[1] * 256 + \
                                                    nodeDataBase[nodeNum].vBattery[0]
            nodeDataBase[nodeNum].mDecWeigthMeasureStand1 = nodeDataBase[nodeNum].mWeigthMeasureStand1[1] * 256 + \
                                                               nodeDataBase[nodeNum].mWeigthMeasureStand1[0]

            #pprint(vars(nodeDataBase[nodeNum]))  # Comment this if the reading is too slow

            menuCreator.set_Force_Livedata(1,
                                           nodeDataBase[nodeNum].mDecWeigthMeasureStand1,
                                           nodeDataBase[nodeNum].vDecBattery,
                                           0,
                                           nodeDataBase[nodeNum].tempDevice)

            nodeNum += 1

        if nodeNum == 8:
            nodeDataBase[nodeNum].nodeNumber = nodeNum
            nodeDataBase[nodeNum].mWeigthMeasureStand2 = transportDataGroup[(nodeNum * 6) + 5:(nodeNum * 6) + 7]
            nodeDataBase[nodeNum].vBattery = transportDataGroup[(nodeNum * 6) + 7:(nodeNum * 6) + 9]
            nodeDataBase[nodeNum].rssiValue = transportDataGroup[(nodeNum * 6) + 9]
            nodeDataBase[nodeNum].tempDevice = transportDataGroup[(nodeNum * 6) + 10]

            nodeDataBase[nodeNum].vDecBattery = nodeDataBase[nodeNum].vBattery[1] * 256 + \
                                                    nodeDataBase[nodeNum].vBattery[0]
            nodeDataBase[nodeNum].mDecWeigthMeasureStand2 = nodeDataBase[nodeNum].mWeigthMeasureStand2[1] * 256 + \
                                                               nodeDataBase[nodeNum].mWeigthMeasureStand2[0]

            #pprint(vars(nodeDataBase[nodeNum]))  # Comment this if the reading is too slow

            menuCreator.set_Force_Livedata(2,
                                           nodeDataBase[nodeNum].mDecWeigthMeasureStand2,
                                           nodeDataBase[nodeNum].vDecBattery,
                                           0,
                                           nodeDataBase[nodeNum].tempDevice)

            nodeNum += 1

        while nodeNum < 12:
            nodeDataBase[nodeNum].nodeNumber = nodeNum
            nodeDataBase[nodeNum].mWeigthMeasure = transportDataGroup[(nodeNum * 6) + 5:(nodeNum * 6) + 7]
            nodeDataBase[nodeNum].vBattery = transportDataGroup[(nodeNum * 6) + 7:(nodeNum * 6) + 9]
            nodeDataBase[nodeNum].rssiValue = transportDataGroup[(nodeNum * 6) + 9]
            nodeDataBase[nodeNum].tempDevice = transportDataGroup[(nodeNum * 6) + 10]

            nodeDataBase[nodeNum].vDecBattery = nodeDataBase[nodeNum].vBattery[1] * 256 + \
                                                nodeDataBase[nodeNum].vBattery[0]
            nodeDataBase[nodeNum].mDecWeigthMeasure = nodeDataBase[nodeNum].mWeigthMeasure[1] * 256 + \
                                                            nodeDataBase[nodeNum].mWeigthMeasure[0]

            #pprint(vars(nodeDataBase[nodeNum]))  # Comment this if the reading is too slow

            menuCreator.set_Force_Livedata(nodeNum-6,
                                           nodeDataBase[nodeNum].mDecWeigthMeasure,
                                           nodeDataBase[nodeNum].vDecBattery,
                                           0,
                                           nodeDataBase[nodeNum].tempDevice)

            nodeNum += 1

        while nodeNum < 15:
            nodeDataBase[nodeNum].nodeNumber = nodeNum
            nodeDataBase[nodeNum].mAccelX = transportDataGroup[(nodeNum * 6) + 5]
            nodeDataBase[nodeNum].mAccelY = transportDataGroup[(nodeNum * 6) + 6]
            nodeDataBase[nodeNum].mAccelZ = transportDataGroup[(nodeNum * 6) + 7]
            nodeDataBase[nodeNum].vBattery = transportDataGroup[(nodeNum * 6) + 8:(nodeNum * 6) + 10]
            nodeDataBase[nodeNum].rssiValue = transportDataGroup[(nodeNum * 6) + 10]
            nodeDataBase[nodeNum].tempDevice = transportDataGroup[(nodeNum * 6) + 11]

            nodeDataBase[nodeNum].vDecBattery = nodeDataBase[nodeNum].vBattery[1] * 256 + \
                                                    nodeDataBase[nodeNum].vBattery[0]

            #pprint(vars(nodeDataBase[nodeNum]))  # Comment this if the reading is too slow

            #menuCreator.set_BT_Livedata(nodeNum-12,
            #                nodeDataBase[nodeNum].mAccelX,
            #                nodeDataBase[nodeNum].mAccelY,
            #                nodeDataBase[nodeNum].mAccelZ,
            #                0,
            #                0,
            #                0,
            #                0,
            #                0,
            #                0,
            #                nodeDataBase[nodeNum].vDecBattery,
            #                0,
            #                nodeDataBase[nodeNum].tempDevice)

            nodeNum += 1


        writeDATELogInfos() # write processed data to the log
        newDataFlag = True


class SocketServer:
    global sock
    """ Simple socket server that listens to one single client. """

    def __init__(self, host='0.0.0.0', port=2010):
        global sock
        """ Initialize the server with a host and port to listen to. """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port
        sock.bind((host, port))
        sock.listen(1)
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        global haveSocketOpened
        global haltThreadFlag
        while self._running and not haltThreadFlag:
            self.run_server()
            haveSocketOpened = False
            time.sleep(5)
            self.close()
            time.sleep(5)
            self.__init__()
        print('Exiting Socket Server')

    def close(self):
        global sock
        """ Close the server socket. """
        print('Closing server socket (host {}, port {})'.format(self.host, self.port))
        if sock:
            sock.close()
            sock = None

    def sendSocketMessage(self, message):
        global sock
        global haveSocketOpened
        global client_sock
        # print('Send Socket message : ')
        try:
            if haveSocketOpened:
                client_sock.send(message)
        except:
            writeLogFileError("Socket server - error while sending messages")
            print("Error sending Socket message")

    def run_server(self):
        global sock
        global client_sock
        global haveSocketOpened
        global haltThreadFlag
        """ Accept and handle an incoming connection. """
        print('Starting socket server (host {}, port {})'.format(self.host, self.port))
        client_sock, client_addr = sock.accept()
        print('Client {} connected'.format(client_addr))
        haveSocketOpened = True
        stop = False
        while not stop and not haltThreadFlag:
            if client_sock:
                # Check if the client is still connected and if data is available:
                try:
                    rdy_read, rdy_write, sock_err = select.select([client_sock, ], [], [])
                except select.error:
                    print('Select() failed on socket with {}'.format(client_addr))
                    writeLogFileError("Socket server - Select() failed on socket with {}")
                    return 1
                if len(rdy_read) > 0:
                    try:
                        read_data = client_sock.recv(255)
                        # Check if socket has been closed
                        if len(read_data) == 0:
                            print('{} closed the socket.'.format(client_addr))
                            stop = True
                            haveSocketOpened = False
                        else:
                            print('>>> Received: {}'.format(read_data.rstrip()))
                            if read_data.rstrip() == 'quit':
                                stop = True
                                haveSocketOpened = False
                            else:
                                client_sock.send(read_data)

                    except:
                        print('Client has disconnected while reading from the socket, go back to listening')
                        stop = True
                        haveSocketOpened = False
            else:
                print("No client is connected, SocketServer can't receive data")
                stop = True
                haveSocketOpened = False
        # Close socket
        print('Closing connection with {}'.format(client_addr))
        client_sock.close()
        haveSocketOpened = True
        return 0

class MesurementNode:
    def __init__(self, nodeNumberNode):
        # Number of the actual node
        self.nodeNumber = nodeNumberNode

        # Battery voltage of the actual node
        self.vBattery = []
        i = 0
        while i < 2:
            self.vBattery.append(nodeNumberNode)
            i += 1

        # Battery voltage of the actual node
        self.vDecBattery = self.vBattery[1] * 256 + self.vBattery[0]

        # Rssi value currently
        self.rssiValue = nodeNumberNode
        # Temperature value of the actual node
        self.tempDevice = nodeNumberNode

        # Measured LineDetectorValue of the actual node
        self.mLDValue = []
        i = 0
        while i < 2:
            self.mLDValue.append(nodeNumberNode)
            i += 1

        self.mDecLDValue = self.mLDValue[1] * 256 + self.mLDValue[0]

        # Measured Mesured Weight of the actual node
        self.mWeigthMeasure = []
        i = 0
        while i < 2:
            self.mWeigthMeasure.append(nodeNumberNode)
            i += 1

        self.mDecWeigthMeasure = self.mWeigthMeasure[1] * 256 + self.mWeigthMeasure[0]

        # Measured Mesured Weight on Stand part 2 of the actual node
        self.mWeigthMeasureStand1 = []
        i = 0
        while i < 2:
            self.mWeigthMeasureStand1.append(nodeNumberNode)
            i += 1

        self.mDecWeigthMeasureStand1 = self.mWeigthMeasureStand1[1] * 256 + self.mWeigthMeasureStand1[0]

        # Measured Mesured Weight on Stand part 2 of the actual node
        self.mWeigthMeasureStand2 = []
        i = 0
        while i < 2:
            self.mWeigthMeasureStand2.append(nodeNumberNode)
            i += 1

        self.mDecWeigthMeasureStand2 = self.mWeigthMeasureStand2[1] * 256 + self.mWeigthMeasureStand2[0]


        # Measured Acceleration X Axel of the actual node
        self.mAccelX = nodeNumberNode

        # Measured Acceleration Y Axel of the actual node
        self.mAccelY = nodeNumberNode

        # Measured Acceleration Z Axel of the actual node
        self.mAccelZ = nodeNumberNode

        # txAddress  # 12 bytes [0h-0Bh]
        # vBattry e  # 2 bytes  [0Ch-0Dh]
        # stBattery  # 1 byte   [0Eh]
        # tempDevice # 1 byte   [0Fh]
        # mLDValue     # 2 bytes  Line detector value
        # mWeigthMeasure     # 2 bytes  Weight value
        # mWeigthMeasureStand1     # 2 bytes  Weight value on Stand 1 part
        # mWeigthMeasureStand2     # 2 bytes  Weight value on Stand 2 part
        # mAccelX     # 1 byte
        # mAccelY     # 1 byte
        # mAccelZ     # 1 byte





class RfIDSettings:
    def __init__(self):
        # RfID reader ID
        self.readerID = []  # 4 bytes
        byteNum = 0
        while byteNum < 4:
            self.readerID.append(0x01)
            byteNum += 1
        # Battery of RfID reader voltage
        self.batteryVoltage = []  # 2 bytes
        byteNum = 0
        while byteNum < 2:
            self.batteryVoltage.append(0x00)
            byteNum += 1
        # Temperature of the RfID reader
        self.temperature = -127  # 1 byte
        # Stored positions
        self.storedPositions = []  # 7 Bytes
        nodeNum = 0
        while nodeNum < 7:
            self.storedPositions.append(0xff)
            nodeNum += 1

        # Stored addresseses
        self.storedAddresses = []  # 7 ZigBee Addresses
        nodeNum = 0
        while nodeNum < 7:
            self.storedAddresses.append(ZigBeeAddress())
            nodeNum += 1

class CreateJSONMessageToServer:
    global idCollector
    global idPacket
    global dateTimeYear
    global dateTimeMonth
    global dateTimeDay
    global dateTimeHour
    global dateTimeMin
    global dateTimeSec
    global lat
    global lon
    global altitude
    global speed
    global fixedGPS
    global gsmQuality
    global gsmOperator
    global alarmState
    global alarmContent
    global gyroY
    global gyroP
    global gyroR
    global accelX
    global accelY
    global accelZ
    global latTarget
    global lonTarget
    global nodeDataBase

    def createNextMessage(self):
        global idCollector
        global idPacket
        global dateTimeYear
        global dateTimeMonth
        global dateTimeDay
        global dateTimeHour
        global dateTimeMin
        global dateTimeSec
        global lat
        global lon
        global latTarget
        global lonTarget
        global altitude
        global speed
        global fixedGPS
        global gsmQuality
        global gsmOperator
        global alarmState
        global alarmContent
        global gyroY
        global gyroP
        global gyroR
        global accelX
        global accelY
        global accelZ
        global nodeDataBase
        global isLogging

        currentTime = int(time.time())
        #content:
        dataContent = {
               "dataCollectorID": idCollector,
               "timestamp": currentTime,
               "packageID": idPacket,
               "GPSLatitude": lat,
               "GPSLongitude": lon,
               "targetPositionLatitude": latTarget,
               "targetPositionLongitude": lonTarget,
               "GPSAltitude": altitude,
               "GPSSpeed": speed,
               "GPSFix": fixedGPS,
               "GSMSignalQuality": gsmQuality,
               "GSMOperatorInfo": gsmOperator,
               "alarmState": alarmState,
               "alarmContent": [alarmContent],
               "gyroscopeY": gyroY,
               "gyroscopeP": gyroP,
               "gyroscopeR": gyroR,
               "accelX": accelX,
               "accelY": accelY,
               "accelZ": accelZ,
               "loadingBelts": [
                    {
                        "batteryVoltage":nodeDataBase[0].vDecBattery,
                        "RSSIValue":nodeDataBase[0].rssiValue,
                        "deviceTemperature":nodeDataBase[0].tempDevice,
                        "measuredUSdist":nodeDataBase[0].mDecUltraSoundDistance
                    },
                    {
                        "batteryVoltage": nodeDataBase[1].vDecBattery,
                        "RSSIValue": nodeDataBase[1].rssiValue,
                        "deviceTemperature": nodeDataBase[1].tempDevice,
                        "measuredUSdist": nodeDataBase[1].mDecUltraSoundDistance
                    },
                    {
                        "batteryVoltage":nodeDataBase[2].vDecBattery,
                        "RSSIValue":nodeDataBase[2].rssiValue,
                        "deviceTemperature":nodeDataBase[2].tempDevice,
                        "measuredUSdist":nodeDataBase[2].mDecUltraSoundDistance
                    },
                    {
                        "batteryVoltage": nodeDataBase[3].vDecBattery,
                        "RSSIValue": nodeDataBase[3].rssiValue,
                        "deviceTemperature": nodeDataBase[3].tempDevice,
                        "measuredUSdist": nodeDataBase[3].mDecUltraSoundDistance
                    },
                    {
                        "batteryVoltage":nodeDataBase[4].vDecBattery,
                        "RSSIValue":nodeDataBase[4].rssiValue,
                        "deviceTemperature":nodeDataBase[4].tempDevice,
                        "measuredUSdist":nodeDataBase[4].mDecUltraSoundDistance
                    },
                    {
                        "batteryVoltage": nodeDataBase[5].vDecBattery,
                        "RSSIValue": nodeDataBase[5].rssiValue,
                        "deviceTemperature": nodeDataBase[5].tempDevice,
                        "measuredUSdist": nodeDataBase[5].mDecUltraSoundDistance
                    },
                    {
                        "batteryVoltage":nodeDataBase[6].vDecBattery,
                        "RSSIValue":nodeDataBase[6].rssiValue,
                        "deviceTemperature":nodeDataBase[6].tempDevice,
                        "measuredUSdist":nodeDataBase[6].mDecUltraSoundDistance
                    },
                    {
                        "batteryVoltage": nodeDataBase[7].vDecBattery,
                        "RSSIValue": nodeDataBase[7].rssiValue,
                        "deviceTemperature": nodeDataBase[7].tempDevice,
                        "measuredUSdist": nodeDataBase[7].mDecUltraSoundDistance
                    },
                    {
                        "batteryVoltage":nodeDataBase[8].vDecBattery,
                        "RSSIValue":nodeDataBase[8].stBattery,
                        "deviceTemperature":nodeDataBase[8].tempDevice,
                        "measuredUSdist":nodeDataBase[8].mDecUltraSoundDistance
                    },
                    {
                        "batteryVoltage": nodeDataBase[9].vDecBattery,
                        "RSSIValue": nodeDataBase[9].rssiValue,
                        "deviceTemperature": nodeDataBase[9].tempDevice,
                        "measuredUSdist": nodeDataBase[9].mDecUltraSoundDistance
                    },
                    {
                        "batteryVoltage":nodeDataBase[10].vDecBattery,
                        "RSSIValue":nodeDataBase[10].rssiValue,
                        "deviceTemperature":nodeDataBase[10].tempDevice,
                        "measuredForce":nodeDataBase[10].mDecUltraSoundDistance
                    },
                    {
                        "batteryVoltage": nodeDataBase[11].vDecBattery,
                        "RSSIValue": nodeDataBase[11].rssiValue,
                        "deviceTemperature": nodeDataBase[11].tempDevice,
                        "measuredUSdist": nodeDataBase[11].mDecUltraSoundDistance
                    },
                    {
                        "batteryVoltage":nodeDataBase[12].vDecBattery,
                        "RSSIValue":nodeDataBase[12].rssiValue,
                        "deviceTemperature":nodeDataBase[12].tempDevice,
                        "measuredForce":nodeDataBase[12].mDecUltraSoundDistance
                    },
                    {
                        "batteryVoltage": nodeDataBase[13].vDecBattery,
                        "RSSIValue": nodeDataBase[13].rssiValue,
                        "deviceTemperature": nodeDataBase[13].tempDevice,
                        "measuredUSdist": nodeDataBase[13].mDecUltraSoundDistance
                    },
                    {
                        "batteryVoltage":nodeDataBase[14].vDecBattery,
                        "RSSIValue":nodeDataBase[14].rssiValue,
                        "deviceTemperature":nodeDataBase[14].tempDevice,
                        "measuredUSdist":nodeDataBase[14].mDecUltraSoundDistance
                    },
                    {
                        "batteryVoltage": nodeDataBase[15].vDecBattery,
                        "RSSIValue": nodeDataBase[15].rssiValue,
                        "deviceTemperature": nodeDataBase[15].tempDevice,
                        "measuredUSdist": nodeDataBase[15].mDecUltraSoundDistance
                    }
               ]
        }
        # If the berry is logging we should save the messages
        if isLogging:
            with open("message_"+currentTime+"_"+idPacket+".json", "w") as write_json:
                json.dump(dataContent, write_json)

        idPacket = idPacket + 1;

        # We should send the message here

    def __init__(self):
        global idCollector
        global idPacket

        idCollector = 11
        idPacket = 1


class ZigBeeAddress:
    def __init__(self):
        # Stored addresses
        self.ownAddress = []  # 12 Bytes
        byteNum = 0
        while byteNum < 12:
            self.ownAddress.append(0xff)
            byteNum += 1


class CommandSettings:
    def __init__(self):
        # Radio Mode
        self.radioMode = 2  # 0 - Radio Not Active, 1 - Listen Only, 2 - Radio Active
        # Device Reset
        self.deviceReset = 0xAA  # 0xAA ??
        # Transport / Measure control
        self.trControl = 0  # 0 - Measure Stop, 1 - Measure Start, 2 - Measure Pause
        # Number of devices
        self.numOfDevices = 0


def initNewLogFile():
    global logFileName
    # init logging
    LOG_LEVEL = logging.INFO
    # LOG_LEVEL = logging.DEBUG
    setNextLogFileNumber()
    # LOG_FILE = "/dev/stdout"
    LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
    logging.basicConfig(filename=logFileName, format=LOG_FORMAT, level=LOG_LEVEL)

def closeLogFile():
    logging.shutdown()

def setNextLogFileNumber():
    global logFileName
    onlyfiles = [f for f in listdir("/home/pi") if isfile(join("/home/pi", f))]

    #print("Find files in the directiory:")
    #print("Original file list: " + str(onlyfiles))
    if len(onlyfiles) != 0:
        numbersList = [0]
        for fileItem in onlyfiles:
            if fileItem.find("hrrLogFile") >= 0:
                numbersList.append(fileItem[11:len(fileItem)])
                #print(fileItem[11:len(fileItem)])
        #print("Maximum: " + str(max(numbersList)))
        stringNumber = str(int(max(numbersList))+1)
        logFileName = "%s%s" % ("hrrLogFile_", stringNumber)
    else:
        logFileName = "hrrLogFile_0"

def writeLogFileITEM(msg):
    global isLogging
    if isLogging:
        logging.info(msg)


def writeINFOLogFile(msg):
    global isLogging
    if isLogging:
        writeLogFileITEM("INFO;" + str(int(time.time())) + ";" + str(messageNumber) + ";" + msg)

def writeGPSLogInfos():
    global dateTimeYear
    global dateTimeMonth
    global dateTimeDay
    global dateTimeHour
    global dateTimeMin
    global dateTimeSec
    global lat
    global lon
    global latTarget
    global lonTarget
    global altitude
    global speed
    global isLogging

    global messageNumber

    if isLogging:
        writeLogFileITEM("GPS;"+ str(int(time.time())) + ";" + str(messageNumber) + ";" + dateTimeYear + "." + dateTimeMonth + "." + dateTimeDay + ";" + dateTimeHour + ":" + dateTimeMin + ":" + dateTimeSec )
        messageNumber += 1

def writeDATELogInfos():

    global messageNumber
    global recSettings
    global nodeDataBase
    global isLogging

    if isLogging == True:
        nodenum = 0
        resultstring = "DATE;"+ str(int(time.time())) + ";" + str(messageNumber)
        resultstring += ";" + str(recSettings.radioMode)
        resultstring += ";" + str(recSettings.deviceReset)
        resultstring += ";" + str(recSettings.trControl)
        resultstring += ";" + str(recSettings.numOfDevices)
        while nodenum < 3:
            #print(str(nodenum))
            resultstring += ";" + str(nodeDataBase[nodenum].txAddress)
            resultstring += ";" + str(nodeDataBase[nodenum].vBattery)
            resultstring += ";" + str(nodeDataBase[nodenum].mDecLDValue)
            resultstring += ";" + str(nodeDataBase[nodenum].tempDevice)
            # pprint(vars(nodeDataBase[nodeNum]))
            nodenum += 1
        while nodenum < 6:
            #print(str(nodenum))
            resultstring += ";" + str(nodeDataBase[nodenum].txAddress)
            resultstring += ";" + str(nodeDataBase[nodenum].vBattery)
            resultstring += ";" + str(nodeDataBase[nodenum].mDecWeigthMeasure)
            resultstring += ";" + str(nodeDataBase[nodenum].tempDevice)
            # pprint(vars(nodeDataBase[nodeNum]))
            nodenum += 1
        while nodenum < 9:
            #print(str(nodenum))
            resultstring += ";" + str(nodeDataBase[nodenum].txAddress)
            resultstring += ";" + str(nodeDataBase[nodenum].vBattery)
            resultstring += ";" + str(nodeDataBase[nodenum].mAccelX)
            resultstring += ";" + str(nodeDataBase[nodenum].mAccelY)
            resultstring += ";" + str(nodeDataBase[nodenum].mAccelZ)
            resultstring += ";" + str(nodeDataBase[nodenum].tempDevice)
            # pprint(vars(nodeDataBase[nodeNum]))
            nodenum += 1
        writeLogFileITEM(resultstring)
        messageNumber += 1

def writeLogFileError(msg):
    global isLogging
    if isLogging:
        writeLogFileITEM("ERROR;"+ str(int(time.time())) + ";" + str(messageNumber) + ";" + msg)


def initDataBase():
    nodeDataBase.append(MesurementNode(0))
    nodeDataBase.append(MesurementNode(1))
    nodeDataBase.append(MesurementNode(2))
    nodeDataBase.append(MesurementNode(3))
    nodeDataBase.append(MesurementNode(4))
    nodeDataBase.append(MesurementNode(5))
    nodeDataBase.append(MesurementNode(6))
    nodeDataBase.append(MesurementNode(7))
    nodeDataBase.append(MesurementNode(8))
    nodeDataBase.append(MesurementNode(9))
    nodeDataBase.append(MesurementNode(9))
    nodeDataBase.append(MesurementNode(10))
    nodeDataBase.append(MesurementNode(11))
    nodeDataBase.append(MesurementNode(12))
    nodeDataBase.append(MesurementNode(13))
    nodeDataBase.append(MesurementNode(14))
    nodeDataBase.append(MesurementNode(15))


def initTestPackage():
    testPackage.append(0xaa)
    testPackage.append(1)
    testPackage.append(2)
    testPackage.append(4)
    testPackage.append(8)
    testPackage.append(16)
    testPackage.append(32)
    testPackage.append(64)
    testPackage.append(128)
    testPackage.append(1)
    testPackage.append(2)
    testPackage.append(4)
    testPackage.append(8)
    testPackage.append(16)
    testPackage.append(32)
    testPackage.append(64)
    testPackage.append(128)
    testPackage.append(1)
    testPackage.append(2)
    CRCforTestPackage = 0
    for x in testPackage:
        CRCforTestPackage = CRCforTestPackage ^ x
    testPackage.append(CRCforTestPackage)

def getCoord(expression):
    global dateTimeYear
    global dateTimeMonth
    global dateTimeDay
    global dateTimeHour
    global dateTimeMin
    global dateTimeSec
    global lat
    global lon
    global altitude
    global speed

    global messageNumber
    # Start the serial connection
    if "+CGNSINF: 1," in expression:
        # Split the reading by commas and return the parts referencing lat and long
        array = expression.split(",")
        dateTimeYear = array[2][0:4]
        dateTimeMonth = array[2][4:6]
        dateTimeDay = array[2][6:8]
        dateTimeHour = array[2][8:10]
        dateTimeMin = array[2][10:12]
        dateTimeSec = array[2][12:14]

        lat = array[3]
        print(lat)
        lon = array[4]
        print(lon)

        altitude = array[5]
        speed = array[6]

        writeGPSLogInfos()

        #print("Date " + dateTimeYear + "." + dateTimeMonth + "." + dateTimeDay + " --- " + dateTimeHour + ":" + dateTimeMin + ":" + dateTimeSec + " Alt : " + altitude + " Speed : " + speed)


def cls():
    u = 0
    while u < 7:
        print('\n')
        u += 1

# def uploadDataBase(self):
# read out all data from HW for all nodes in the system

# Init database
initDataBase()

# Init Test package
initTestPackage()

actSettings = CommandSettings()
recSettings = CommandSettings()

# Create Class
##TEST##BTserver = BluetoothServer()
# Create Thread
##TEST##BTserverThread = Thread(target=BTserver.run)
# Start Thread
##TEST##BTserverThread.start()


# Create Class
BTserver = AdafruitBLEServer()
# Create Thread
BTserverThread = Thread(target=BTserver.run)
# Start Thread
BTserverThread.start()

# Create Class
##TEST##GPSConnection = GPSUARTConnection()
# Create Thread
##TEST##GPSConnectionThread = Thread(target=GPSConnection.run)
# Start Thread
##TEST##GPSConnectionThread.start()

# Create Class
SocketServerClass = SocketServer()
# Create Thread
SocketServerThread = Thread(target=SocketServerClass.run)
# Start Thread
SocketServerThread.start()

# Create Class
SPIRec = SPIReceiver()
# Create Thread
SPIRecThread = Thread(target=SPIRec.run)
# Start Thread
SPIRecThread.start()

# Create Class
SerialUART = SerialPort()
# Create Thread
serialThread = Thread(target=SerialUART.run)
# Start Thread
serialThread.start()

# Create LED class for LED state monitoring
LEDMonitor = LEDStateChanges()
# Create the monitoring thread
LEDMonitorThread = Thread(target=LEDMonitor.run)
# Start Thread
LEDMonitorThread.start()

# Create menu Object for using its methods
menuCreator = menuCreatorObject()

##TES##send1Message = True
##TES##send2Message = False

Exit = False  # Exit flag
print('Waiting for data')
def signal_handler(sig, frame):
    global haltThreadFlag
    print('You pressed Ctrl+C! Wait 3 sec for exiting')
    haltThreadFlag = True
    time.sleep(3)
    print('Exiting...')
    # sys.exit(0)
    os._exit(1)
signal.signal(signal.SIGINT, signal_handler)
print('--- Start reading data ---' + str(Exit) + "," + str(haltThreadFlag))
### TEST ### while Exit == False and not haltThreadFlag:
### TEST ###
### TEST ###     print('--- Read ZigBee packets ---')
### TEST ###     SPIRec.sendReadAllPackage()

### TEST ###     time.sleep(3)
### NEW GUI IMPLEMENTATION

def main(stdscr):
    menuCreator.main_GUI_START(stdscr,SPIRec)

    # choice = input_box_center(stdscr, 'Log name:')


curses.wrapper(main)

print('End of resident application')

haltThreadFlag = True

os._exit(1)
