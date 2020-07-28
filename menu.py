import curses
from curses import textpad
import time


# GUI Source: https://github.com/nikhilkumarsingh/python-curses-tut
# https://www.youtube.com/watch?v=zwMsmBsC1GM
# FILE Source: https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions
# main menu items
# to use python2 do not use ASCII characters either at comments!

### set_IR_Livedata(IR_ID_number,Distance,CountA,CountB,BattVoltage,BattPercent,Temperature)
# set_BT_Livedata(BT_ID_number ,AccX , AccY ,AccZ , MagnX ,MagnY ,MagnZ , GyroX ,GyroY ,GyroZ ,BattV ,BattPercent , temp)
# set_Force_Livedata(Force_ID_number ,Measured_weight,BattV,BattPercent,temperature)

### Jelenleg a szimulalt eredmenyeket a kovetkezo fuggvenyben generalom:
# get_live_data()

# Variables:
class menuCreatorObject:
    def initial_variables(self):
        global main_menu  # Main menu elements
        global header_menu_text
        global bottom_menu_text
        global device_Serial_number
        global device_name_text

        global Lang  # chosed Language -->python2--> EN
        global h  # Screen resolution height
        global w  # Screen resolution with
        global minimal_h  # Requirement screen resolution heigh
        global minimal_w  # Requirement screen resolution width
        global status_Rollower_Warning  # Is it safe or not safe --> byte  safe 0 - 5 dangerous
        # Bluetooth
        global item_BT  # BT settings name
        global item_short_names_BT  # BT devices short names for LOG
        global item_BT_enable_values  # BT enabled/disabled view and logging
        global item_BT_sensor_ALL_values  # BT measurement values
        global item_BT_sensor_values_header  # BT values topic/header
        global item_BT_selected_columns  # BT selected columns (values) to log
        # IR Distance meter
        global item_IR  # IR settings name
        global item_short_names_IR  # IR devices short names for LOG
        global item_IR_enable_values  # IR enabled/disabled view and logging
        global item_IR_sensor_ALL_values  # IR settings values
        global item_IR_sensor_values_header  # IR values topic/header
        global item_IR_selected_columns  # IR selected columns (values) to log   (True/False)
        # Force meter
        global item_Force  # Force measurement names
        global item_short_names_Force  # Force devices short names for LOG
        global item_Force_enable_values  # Force enabled/disabled view and logging
        global item_Force_type_name_ID  # Force Transducer typelist is connected?
        global ForceType_Name_LIST  # List of Cells which is availabled? [U9C, S9M-S, U10M]
        global item_Force_sensor_ALL_values  # Force measurement datas
        global item_Force_calibrations  # Calibration datas for Force Sensor
        global item_Force_sensor_values_header  # Force values topic/header
        global item_Force_selected_columns  # Selected columns (values) to log

        # LOG - variables
        global Log_current_status  # Log type 0: Off,  1: Started-for unlimited time,  2: Log Enabled devices for unlimited time    3: Log 20 measurement data                  4: Log 1 measurement data
        global Log_current_status_list  # Log type 0: Off,  1: Started-for unlimited time,  2: Log Enabled devices for unlimited time    3: Log 20 measurement data                  4: Log 1 measurement data

        global Log_File_name
        global Log_init  # is it a new file?  --> f.write-header
        global Log_Selected_Folder  # Selected Folder
        global Log_i_measurement  # In a log file - how many time has measurement the Datas
        global Log_change_ALL_flag  # Flag for make a new log.
        global Log_columns_header
        global Log_columns_enabled  # Time, ID,
        global LOG_settings_header  # ID, time,milisec, separators...
        global LOG_settings_values  # True/False
        global LOG_File_Number  # How many Log have we got in this file.
        global separator  # Separator for Columns at LOG

        # main_menu = ['Live data', '','', 'Devices', 'Settings', 'Exit']
        main_menu = ['Live data', 'Devices', 'Settings', 'Exit']

        header_menu_text = "EBK HEE Central Control Unit"
        bottom_menu_text = "GUI v0.7"
        #    header_menu_text     = "RODIN CONNECTING Central Control Unit"
        #    bottom_menu_text     = "GUI v1.0"
        device_Serial_number = "S/N: EHRR-CCU001"
        device_name_text = "--  "
        Lang = "EN"

        # Screen:
        h = 0
        w = 0
        minimal_h = 35  # Requirement resolution -its depend on live
        minimal_w = 85  # Requirement resolution

        # BT ACCELERATION DECLARATION:

        # DEVICES Names:
        item_BT = ['Device_Bt_Node_01',
                   'Device_Bt_Node_02',
                   'Device_Bt_Node_03',
                   'Device_Bt_Node_04',
                   'Device_Bt_Node_05',
                   'Device_Bt_Node_06'
                   ]
        item_short_names_BT = ['BT_1', 'BT_2', 'BT_3', 'BT_4', 'BT_5', 'BT_6']

        item_BT_sensor_values_header = ['AccX', 'AccY', 'AccZ',
                                        'MagnX', 'MagnY', 'MagnZ',
                                        'GyroX', 'GyroY', 'GyroZ',
                                        'BattV', 'Batt%', 'Temp*C']
        item_BT_selected_columns = [True, True, True,
                                    True, True, True,
                                    True, True, True,
                                    True, True, True]

        # Enabled devices (Show in live and LOG)
        item_BT_enable_values = [True,
                                 True,
                                 True,
                                 True,
                                 False,
                                 False]
        #  Measurement              Acc:     x    y   z  Magn:x   y    z   Gyro x   y   z   Batt: V  %  Temp
        item_BT_sensor_ALL_values = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 00, 00],
                                     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 00, 00],
                                     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 00, 00],
                                     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 00, 00],
                                     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 00, 00],
                                     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 00, 00]]

        # IR Names:
        item_IR = ['Device_IR_Node_01',
                   'Device_IR_Node_02',
                   'Device_IR_Node_03',
                   'Device_IR_Node_04',
                   'Device_IR_Node_05',
                   'Device_IR_Node_06'
                   ]

        item_short_names_IR = ['IR_1', 'IR_2', 'IR_3', 'IR_4', 'IR_5', 'IR_6']
        # IR enables
        item_IR_enable_values = [True,
                                 True,
                                 False,
                                 False,
                                 False,
                                 False]
        #    Dist  countA:   B, BattV, %     Temp
        item_IR_sensor_ALL_values = [[00.00, 0, 0, 0.00, 00, 00.00],
                                     [00.00, 0, 0, 0.00, 00, 00.00],
                                     [00.00, 0, 0, 0.00, 00, 00.00],
                                     [00.00, 0, 0, 0.00, 00, 00.00],
                                     [00.00, 0, 0, 0.00, 00, 00.00],
                                     [00.00, 0, 0, 0.00, 00, 00.00]
                                     ]
        item_IR_sensor_values_header = ['Dist', 'countA', '-',
                                        'BattV', 'Batt%', 'Temp*C']
        item_IR_selected_columns = [True, True, False,
                                    True, True, True]

        # Distance between two scale:
        item_Force_calibrations = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        item_Force = ['Device_Force_Node_01',
                      'Device_Force_Node_02',
                      'Device_Force_Node_03',
                      'Device_Force_Node_04',
                      'Device_Force_Node_05',
                      'Device_Force_Node_06'
                      ]

        item_short_names_Force = ['F_1', 'F_2', 'F_3', 'F_4', 'F_5', 'F_6']

        item_Force_type_name = ['Device_Force_Node_01',
                                'Device_Force_Node_02',
                                'Device_Force_Node_03',
                                'Device_Force_Node_04',
                                'Device_Force_Node_05',
                                'Device_Force_Node_06'
                                ]

        item_Force_enable_values = [False,
                                    True,
                                    True,
                                    False,
                                    False,
                                    False]

        item_Force_type_name_ID = [2, 1, 2, 2, 0, 2]
        #                          0      1        2
        ForceType_Name_LIST = ["U9C", "S9M-S", "U10M"]

        #  Force: [Measured, Calibrated, BattV, Batt%, --   Temperature*C
        item_Force_sensor_ALL_values = [[0.0, 0.0, 0.0, 0.0, 00, 0.0],
                                        [0.0, 0.0, 0.0, 0.0, 00, 0.0],
                                        [0.0, 0.0, 0.0, 0.0, 00, 0.0],
                                        [0.0, 0.0, 0.0, 0.0, 00, 0.0],
                                        [0.0, 0.0, 0.0, 0.0, 00, 0.0],
                                        [0.0, 0.0, 0.0, 0.0, 00, 0.0]]

        item_Force_sensor_values_header = ['Meas_F', 'CalF', 'BattV', 'Batt%', '--', 'Temp*C', ]
        item_Force_selected_columns = [True, True, True, True, False, True]

        # OFFSET  25% m   50%m  75%m  100%m
        item_Force_calibrations = [[0.0, 0.0, 0.0, 0.0, 0.0],
                                   [0.0, 0.0, 0.0, 0.0, 0.0],
                                   [0.0, 0.0, 0.0, 0.0, 0.0],
                                   [0.0, 0.0, 0.0, 0.0, 0.0],
                                   [0.0, 0.0, 0.0, 0.0, 0.0],
                                   [0.0, 0.0, 0.0, 0.0, 0.0]
                                   ]
        Log_current_status = 0
        Log_current_status_list = ['         Stopped ', '         Started ', '        Started ', ' 20 data LOG ',
                                   ' 1 data LOG ']

        LOG_File_Number = 0
        Log_init = True
        status_Rollower_Warning = 0

        # Log_change_ALL_flag = False
        # LOG - variables
        # Log type 0: Off,  1: Started-for unlimited time,  2: Log Enabled devices for unlimited time    3: Log 20 measurement data                  4: Log 1 measurement data

        separator = "\t"
        Log_File_name = "Rollover"
        Log_Selected_Folder = "/share/log/"
        Log_i_measurement = 0  # How many row have we Logged
        #                      0               1         2         3         4              5           6           7               8
        LOG_settings_header = ['ID', 'Time HH:MM:SS', 'Time HH', 'TIME MM', 'TIME SS', 'TIME miliSec', 'Separator "TAB"',
                               'Separator ","', 'Separator "-"']

        #                      0   1      2     3     4     5     6     7   8
        LOG_settings_values = [True, False, False, False, False, True, True, False, False]  # True/False


    def load_initial_settings_from_file(self,stdscr, file_name):
        self.initial_variables()
        self.print_center(stdscr, "All default values is loaded.")
        self.screen_refresh(stdscr)


    # File Functions:
    def LOG_file_is_access_able(self,path, mode='r'):
        # Return True  if file exist
        # Return False if not exist
        try:
            f = open(path, mode)
            f.close()
        except IOError:
            return False
            print
            "file not exist"
        return True


    def LOG_file_writeln(self,path, line):
        # 'w' signifies that you are writing to the file (overwrites)
        # 'a' signifies that you are appending to the file
        f = open(path, 'a')
        f.write(str(line) + '\n')
        f.close()


    def Log_Write_header(self,path):
        global header_menu_text  #
        global bottom_menu_text  #
        global device_Serial_number  # Device_Serial_number
        global item_BT_enable_values  #
        global Log_i_measurement  # In a log file - how many time has measurement the Datas
        global separator
        file_exist = self.LOG_file_is_access_able(path, mode='r')  # True/False
        if not (file_exist):
            f = open(path, 'a')
            f.write(header_menu_text + '\n')
            f.write(bottom_menu_text + ',  ')
            f.write(device_Serial_number + '\n')
            f.write('This is a valid measurement file. This file is created by Control Unit Software.' + '\n')
            f.write('The measurement settings are the following:' + '\n')
            f.write('Log name: ' + '\n')
            f.write('')
            f.write('________________________________________________________________________________' + '\n')

            Log_i_measurement = 1
            # f.write('Selected device names: '+ '\n')
            # selected_device_names_line = ''
            # line1 = ''
            # line2 = ''
            line1 = separator
            line2 = 'ID' + separator

            # Selected_device_names_line:
            # Here is the code for list selected devices line to LOG.
            # Check the BT sensors is turned ON/OFF

            for i in range(len(item_BT)):  # i --> All BT Devices
                if item_BT_enable_values[i] == True:  # IF device is ENABLED
                    for j in range(len(item_BT_sensor_values_header)):  # J --> Check all Column
                        if item_BT_selected_columns[j]:  # Is Column Checked
                            line1 = line1 + item_short_names_BT[i] + separator  # Device name
                            line2 = line2 + item_BT_sensor_values_header[j] + separator

                            # Check the Force sensors is turned ON/OFF
            for i in range(len(item_Force)):  # i --> All BT Devices
                if item_Force_enable_values[i] == True:  # IF device is ENABLED
                    for j in range(len(item_Force_sensor_values_header)):  # J --> Check all Column
                        if item_Force_selected_columns[j]:  # Is Column Checked
                            line1 = line1 + item_short_names_Force[i] + separator  # Device name
                            line2 = line2 + item_Force_sensor_values_header[j] + separator

                            # Check the IR sensors is turned ON/OFF
            for i in range(len(item_IR)):  # i --> All BT Devices
                if item_IR_enable_values[i] == True:  # IF device is ENABLED
                    for j in range(len(item_IR_sensor_values_header)):  # J --> Check all Column
                        if item_IR_selected_columns[j]:  # Is Column Checked
                            line1 = line1 + item_short_names_IR[i] + separator  # Device name
                            line2 = line2 + item_IR_sensor_values_header[j] + separator

            f.write(line1 + '\n')
            f.write(line2 + '\n')
            f.write('\n')
            f.close()


    def Log_Write_Selected_DATA(self,path):
        global header_menu_text  #
        global bottom_menu_text  #
        global device_Serial_number  # Device_Serial_number

        # Bluetooth
        global item_BT  # BT settings name
        global item_BT_enable_values  # BT enabled/disabled view and logging
        global item_BT_sensor_ALL_values  # BT settings values
        global item_BT_selected_columns
        global item_BT_sensor_values_header

        # IR Distance meter
        global item_IR  # IR settings name
        global item_IR_enable_values  # IR enabled/disabled view and logging
        global item_IR_sensor_ALL_values  # IR settings values
        global item_IR_selected_columns
        global item_IR_sensor_values_header
        # Force meter
        global item_Force  # Force measurement names
        global item_Force_enable_values  # Force enabled/disabled view and logging
        global item_Force_type_name_ID  # Force Transducer typelist is connected?
        global ForceType_Name_LIST  # List of Cells which is availabled? [U9C, S9M-S, U10M]
        global item_Force_sensor_values_header
        global item_Force_selected_columns

        global item_Force_sensor_ALL_values  # Force measurement datas
        global item_Force_calibratins  # Calibration datas
        global item_Force_calibratins
        global Log_i_measurement

        file_exist = self.LOG_file_is_access_able(path, mode='r')  # True/False
        line3 = str(Log_i_measurement) + separator

        for i in range(len(item_BT)):  # i --> All BT Devices
            if item_BT_enable_values[i] == True:  # IF device is ENABLED
                for j in range(len(item_BT_sensor_values_header)):  # J --> Check all Column
                    if item_BT_selected_columns[j]:  # Is Column Checked
                        line3 = line3 + str(item_BT_sensor_ALL_values[i][j]) + separator  # Device name

        # Check the Force sensors is turned ON/OFF
        for i in range(len(item_Force)):  # i --> All BT Devices
            if item_Force_enable_values[i] == True:  # IF device is ENABLED
                for j in range(len(item_Force_sensor_values_header)):  # J --> Check all Column
                    if item_Force_selected_columns[j]:  # Is Column Checked
                        line3 = line3 + str(item_Force_sensor_ALL_values[i][j]) + separator  # Device name

        # Check the IR sensors is turned ON/OFF
        for i in range(len(item_IR)):  # i --> All BT Devices
            if item_IR_enable_values[i] == True:  # IF device is ENABLED
                for j in range(len(item_IR_sensor_values_header)):  # J --> Check all Column
                    if item_IR_selected_columns[j]:  # Is Column Checked
                        line3 = line3 + str(item_IR_sensor_ALL_values[i][j]) + separator  # Device name

        Log_i_measurement += 1

        if (file_exist):
            f = open(path, 'a')
            f.write(line3 + '\n')

            f.close()


    def random_number(self,minimum, maximum):
        import random
        A = random.randint(minimum, maximum)

        return float(A)


    def get_live_data(self):
        # Sensor values:
        global item_BT_sensor_ALL_values
        global item_IR_sensor_ALL_values

        """   UNCOMMENT FOR OFFLINE USE                   BLUETOOTH:      """
        a = float(self.random_number(0, 1000) / 100)  # ACC  X
        b = float(self.random_number(0, 1000) / 100)  # ACC  Y
        c = float(self.random_number(0, 1000) / 100)  # ACC  Z
        d = float(self.random_number(0, 1000) / 100)  # Magn X
        e = float(self.random_number(0, 1000) / 100)  # Magn Y
        f = float(self.random_number(0, 1000) / 100)  # Magn Z
        g = float(self.random_number(0, 1000) / 100)  # Gyro
        h = float(self.random_number(0, 1000) / 100)  # Gyro
        i = float(self.random_number(0, 1000) / 100)  # Gyro      b V  b%  temp
        t = float(self.random_number(0, 1000)) / 100 + 15
        self.set_BT_Livedata(1, a, b, c, d, e, f, g, h, i, 3.1, 72, t)

        a = float(self.random_number(0, 1000) / 100)  # ACC  X
        b = float(self.random_number(0, 1000) / 100)  # ACC  Y
        c = float(self.random_number(0, 1000) / 100)  # ACC  Z
        d = float(self.random_number(0, 1000) / 100)  # Magn X
        e = float(self.random_number(0, 1000) / 100)  # Magn Y
        f = float(self.random_number(0, 1000) / 100)  # Magn Z
        g = float(self.random_number(0, 1000) / 100)  # Gyro
        h = float(self.random_number(0, 1000) / 100)  # Gyro
        i = float(self.random_number(0, 1000) / 100)  # Gyro
        t = float(self.random_number(0, 1000)) / 100 + 15
        self.set_BT_Livedata(2, a, b, c, d, e, f, g, h, i, 3.1, 72, t)

        a = float(self.random_number(0, 1000) / 100)  # ACC  X
        b = float(self.random_number(0, 1000) / 100)  # ACC  Y
        c = float(self.random_number(0, 1000) / 100)  # ACC  Z
        d = float(self.random_number(0, 1000) / 100)  # Magn X
        e = float(self.random_number(0, 1000) / 100)  # Magn Y
        f = float(self.random_number(0, 1000) / 100)  # Magn Z
        g = float(self.random_number(0, 1000) / 100)  # Gyro
        h = float(self.random_number(0, 1000) / 100)  # Gyro
        i = float(self.random_number(0, 1000) / 100)  # Gyro
        t = float(self.random_number(0, 1000)) / 100 + 15
        self.set_BT_Livedata(3, a, b, c, d, e, f, g, h, i, 3.1, 72, t)

        a = float(self.random_number(0, 1000) / 100)  # ACC  X
        b = float(self.random_number(0, 1000) / 100)  # ACC  Y
        c = float(self.random_number(0, 1000) / 100)  # ACC  Z
        d = float(self.random_number(0, 1000) / 100)  # Magn X
        e = float(self.random_number(0, 1000) / 100)  # Magn Y
        f = float(self.random_number(0, 1000) / 100)  # Magn Z
        g = float(self.random_number(0, 1000) / 100)  # Gyro
        h = float(self.random_number(0, 1000) / 100)  # Gyro
        i = float(self.random_number(0, 1000) / 100)  # Gyro
        t = float(self.random_number(0, 1000)) / 100 + 15
        self.set_BT_Livedata(4, a, b, c, d, e, f, g, h, i, 3.1, 72, t)

        """                                                             IR SENSOR   """
        # Make Random values for IR SENSOR
        a = float(self.random_number(0, 1000) / 100)  # ACC  X
        b = float(self.random_number(0, 10))  # Count A
        c = float(self.random_number(0, 10))  # Count B
        d = float(self.random_number(0, 1000) / 100)  # Magn X
        e = self.random_number(0, 10)  # Magn Y
        f = self.random_number(0, 10)  # Magn Z
        t = float(self.random_number(0, 1000)) / 100 + 15  # Temperature
        self.set_IR_Livedata(1, a, b, c, 3.2, 73, t)

        # Make Random values for IR SENSOR
        a = float(self.random_number(0, 1000) / 100)  # ACC  X
        b = float(self.random_number(0, 10))  # Count A
        c = float(self.random_number(0, 10))  # Count B
        d = float(self.random_number(0, 1000) / 100)  # Magn X
        e = self.random_number(0, 10)  # Magn Y
        f = self.random_number(0, 10)  # Magn Z
        t = float(self.random_number(0, 1000)) / 100 + 15  # Temperature
        self.set_IR_Livedata(2, a, b, c, 3.2, 73, t)
        self.set_IR_Livedata(3, a, b, c, 3.2, 73, t)
        self.set_IR_Livedata(4, a, b, c, 3.2, 73, t)
        self.set_IR_Livedata(5, a, b, c, 3.2, 73, t)
        self.set_IR_Livedata(6, a, b, c, 3.2, 73, t)

        # Make Random values for Force
        Measured_weight = float(self.random_number(0, 1000))  #
        temperature = float(self.random_number(0, 100)) / 10 + 15  #
        #                  0                1   2  3            4
        self.set_Force_Livedata(1, Measured_weight, 3.2, 70, temperature)
        self.set_Force_Livedata(2, Measured_weight, 3.2, 70, temperature)
        self.set_Force_Livedata(3, Measured_weight, 3.2, 70, temperature)
        self.set_Force_Livedata(4, Measured_weight, 3.2, 70, temperature)
        self.set_Force_Livedata(5, Measured_weight, 3.2, 70, temperature)
        self.set_Force_Livedata(6, Measured_weight, 3.2, 70, temperature)

        """   UNCOMMENT FOR OFFLINE USE   """
        # Here is the code to refresh Sensors DATA:

        # Here is the code of LOG Checking:

        calc_Rollower_Warning = 0  # 0 is not warning, 3 is Roll Over!


    # Set a value of sensor data:
    def set_IR_Livedata(self,IR_ID_number, Distance, CountA, CountB, BattVoltage, BattPercent, Temperature):
        global item_IR_sensor_ALL_values
        # example:
        item_IR_sensor_X_values = [Distance, CountA, CountB, BattVoltage, BattPercent, Temperature]
        item_IR_sensor_ALL_values[IR_ID_number - 1] = item_IR_sensor_X_values


    def set_BT_Livedata(self,BT_ID_number, AccX, AccY, AccZ, MagnX, MagnY, MagnZ, GyroX, GyroY, GyroZ, BattV, BattPercent, temp):
        # set_BT_Livedata(3 , 10.4,10.1,3.2, 10.4,10.1,3.2, 10.4,10.1,3.2, 3.12 , 64 , 21.32)
        global item_BT_sensor_ALL_values
        min = 0
        max = 7

        # set_line = [Acc[0],Acc[1],Acc[2],Magn[0],Magn[1],Magn[2],Gyro[0],Gyro[1],Gyro[2],BattV ,BattPercent ,temp ]
        set_line = [AccX, AccY, AccY, MagnX, MagnY, MagnZ, GyroX, GyroY, GyroZ, BattV, BattPercent, temp]
        item_BT_sensor_ALL_values[BT_ID_number - 1] = set_line


    def set_Force_Livedata(self,Force_ID_number, Measured_weight, BattV, BattPercent, temperature):
        # Force meter
        global item_Force  # Force measurement names
        global item_Force_enable_values  # Force enabled/disabled view and logging
        global item_Force_sensor_ALL_values  # Force measurement datas
        global item_Force_calibratins  # Calibration datas
        global item_BT_sensor_ALL_values
        min = 0
        max = 7

        # Input force calibration:
        Measured_weight_calc = Measured_weight

        set_line = [Measured_weight, Measured_weight_calc, BattV, BattPercent, 0, temperature]
        item_Force_sensor_ALL_values[Force_ID_number - 1] = set_line


    def set_Livedata_Log(self):
        global Log_current_status

        if Log_current_status > 0:
            # Write all selected data to file **********************************
            header = True  # If file is exist and


    # LOG functions:
    def set_start_log(self,set_log_status):
        # 0: Log Off ALL
        # 1: Started-for unlimited time,
        # 2: Log Enabled devices for unlimited time
        # 3: Log 20 measurement data
        # 4: Log 1 measurement data

        # LOG - variables
        global Log_current_status
        global LOG_File_Number

        # ON --> OFF
        # if Log_current_status  > 0 and set_log_status == 0:
        #    Log_current_status = 0      # 1: Started-for unlimited time
        #    LOG_File_Number    += 1

        # OFF --> ON
        if Log_current_status == 0 and set_log_status == 1:
            Log_current_status = 1  # 1: Started unlimited time
            LOG_File_Number += 1
            self.Log_Write_header(Log_Selected_Folder + Log_File_name + str(LOG_File_Number) + '.log')

        # OFF --> Only enabled devices
        if Log_current_status == 0 and set_log_status == 2:
            Log_current_status = 2  # 2: Log Enabled devices for unlimited time
            LOG_File_Number += 1
            self.Log_Write_header(Log_Selected_Folder + Log_File_name + str(LOG_File_Number) + '.log')

        # OFF --> Enabled devices 20 Measurement data
        if Log_current_status == 0 and set_log_status == 3:
            Log_current_status = 3  # 3: Log 20 measurement data
            LOG_File_Number += 1
            self.Log_Write_header(Log_Selected_Folder + Log_File_name + str(LOG_File_Number) + '.log')

        # OFF --> Enabled devices 1 Measurement data
        if Log_current_status == 0 and set_log_status == 4:
            Log_current_status = 4  # 4: Log 1 measurement data
            LOG_File_Number += 1
            self.Log_Write_header(Log_Selected_Folder + Log_File_name + str(LOG_File_Number) + '.log')


    def set_stop_log(self,set_log_status):
        # 0: Log Off ALL
        # 1: Started-for unlimited time,
        # 2: Log Enabled devices for unlimited time
        # 3: Log 20 measurement data
        # 4: Log 1 measurement data

        # LOG - variables
        global Log_current_status
        # global LOG_File_Number

        Log_current_status = 0


    # STD SRC FUNCTIONS:
    def get_screen_size(self,stdscr):
        # Not used!!!
        # update the screen variables: h, w
        error_code = "Couldn't get the resolution!"
        try:
            h, w = stdscr.getmaxyx()
        except:
            print(error_code)

        if (h < 20 or w < 20):
            stdscr.addstr(1, 1, ("Resolution is too small!"))
            print("Resolution is too small!")


    def screen_refresh(self,stdscr):
        h, w = stdscr.getmaxyx()
        if (h >= minimal_h and w >= minimal_w):
            error_code = 'Error! to refresh the screen! Maybe too small resolution!'
            try:
                stdscr.refresh()
            except (curses.error, RuntimeError, TypeError, NameError):
                print(error_code)
                pass
        else:
             stdscr.clear()
             x = w // 2 - len('Choose a higher resolution! ' + str(minimal_h) + 'x' + str(minimal_w)) // 2
             y = h // 2
             stdscr.addstr(y, x, 'Choose a higher resolution! ' + str(minimal_h) + 'x' + str(minimal_w))
             stdscr.refresh()

        # PRINT TO SCREEN FUNCTIONS


    def print_debug(self,stdscr):
        h, w = stdscr.getmaxyx()
        # stdscr.addstr(0, 0, ("h x w: " + str(h) + " x " + str(w)))

        global LOG_File_Number
        global Log_current_status
        stdscr.addstr(0, 0, (
                    "h x w: " + str(h) + " x " + str(w) + " LogMode: " + str(Log_current_status) + " Log_file: " + str(
                LOG_File_Number)))


    def print_main_menu(self,stdscr, selected_row_idx):
        global main_menu
        # print the main_menu
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        # get_screen_size(stdscr) # h,w

        # List the menu items:
        for idx, row in enumerate(main_menu):
            x = w // 2 - len(row) // 2
            y = h // 2 - len(main_menu) // 2 + idx
            if idx == selected_row_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x - 2, ("  " + row + "  "))
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)
        # Box or border to Main Menu parameters:
        b_startx = w // 2 - 20
        b_starty = h // 2 - len(main_menu) // 2 - 3
        b_end_x = w // 2 + 20
        b_end_y = h // 2 + len(main_menu) // 2 + 3
        # make a border to the menu:
        self.print_box(stdscr, b_starty, b_startx, b_end_y, b_end_x)
        #   Uncomment to full screen border!
        # print_box(stdscr,0,0,h-1,w-2)

        #   Header menu text parameters
        y = h // 2 - len(main_menu) // 2 - 4
        x = w // 2 - len(header_menu_text) // 2
        stdscr.addstr(y, x, header_menu_text)
        #   Bottom text parameters
        y = h // 2 + len(main_menu) // 2 + 4
        x = w // 2 - len(bottom_menu_text) // 2
        stdscr.addstr(y, x, bottom_menu_text)
        self.print_debug(stdscr)
        self.screen_refresh(stdscr)  # Check Screen resolution and refresh


    def print_menu(self,stdscr, selected_row_idx, menu_items):
        h, w = stdscr.getmaxyx()
        for id_menu_x, row in enumerate(menu_items):
            x = w // 2 - len(row) // 2
            y = h // 2 - len(menu_items) // 2 + id_menu_x
            if id_menu_x == selected_row_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, (row))
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)
        # stdscr.refresh()
        self.screen_refresh(stdscr)


    def print_menu_position(self,stdscr, selected_row_idx, menu_items, start_x):
        h, w = stdscr.getmaxyx()
        x = start_x
        for id_menu_x, row in enumerate(menu_items):
            # x = w//2 - len(row)//2
            y = h // 2 - len(menu_items) // 2 + id_menu_x
            if id_menu_x == selected_row_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, (row))
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)
        self.screen_refresh(stdscr)


    def print_center(self,stdscr, text):
        # print to center of the screen
        stdscr.clear()
        # get_screen_size(stdscr) # h,w
        h, w = stdscr.getmaxyx()
        x = w // 2 - len(text) // 2
        y = h // 2
        stdscr.addstr(y, x, text)
        # stdscr.refresh()
        self.screen_refresh(stdscr)


    def print_sensor_bluetooth_values_with_border(self,stdscr, begin_y, begin_x, sensor_name, Accel, Magn, Gyro, Temp):
        #
        # Accel [x,y,z]
        # Magn [x,y,z]
        # Gyro [x,y,z]
        # Temp 12.3
        #
        h, w = stdscr.getmaxyx()

        # Box size definition:
        box_size_x = 34
        box_size_y = 7

        # Box BORDER:
        self.print_box(stdscr, begin_y, begin_x, begin_y + box_size_y, begin_x + box_size_x)

        sensor_data_type_1 = "Accel X:       Y:       Z:      "
        sensor_data_type_2 = "Magn  X:       Y:       Z:      "
        sensor_data_type_3 = "Gyro  X:       Y:       Z:      "
        sensor_data_type_4 = "  -.  *C"

        # Sensor name:
        stdscr.addstr(begin_y + 1, begin_x + 1, (sensor_name))
        # Sensor label1:
        stdscr.addstr(begin_y + 3, begin_x + 1, (sensor_data_type_1))
        stdscr.addstr(begin_y + 4, begin_x + 1, (sensor_data_type_2))
        stdscr.addstr(begin_y + 5, begin_x + 1, (sensor_data_type_3))
        stdscr.addstr(begin_y + 6, begin_x + 1, (sensor_data_type_4))

        # Temp data:
        stdscr.addstr(begin_y + 6, begin_x + 2, str('%5.2f' % Temp))
        # Device collections:
        if len(Accel) == 3 and len(Magn) == 3 and len(Gyro) == 3:
            stdscr.addstr(begin_y + 3, begin_x + 10, str('%5.2f' % Accel[0]))
            stdscr.addstr(begin_y + 4, begin_x + 10, str('%5.2f' % Magn[0]))
            stdscr.addstr(begin_y + 5, begin_x + 10, str('%5.2f' % Gyro[0]))

            stdscr.addstr(begin_y + 3, begin_x + 19, str('%5.2f' % Accel[1]))
            stdscr.addstr(begin_y + 4, begin_x + 19, str('%5.2f' % Magn[1]))
            stdscr.addstr(begin_y + 5, begin_x + 19, str('%5.2f' % Gyro[1]))

            stdscr.addstr(begin_y + 3, begin_x + 28, str('%5.2f' % Accel[2]))
            stdscr.addstr(begin_y + 4, begin_x + 28, str('%5.2f' % Magn[2]))
            stdscr.addstr(begin_y + 5, begin_x + 28, str('%5.2f' % Gyro[2]))


    def print_sensor_IR_values_with_border(self,stdscr, begin_y, begin_x, sensor_name, values):
        h, w = stdscr.getmaxyx()

        # Box size definition:
        box_size_x = 28
        box_size_y = 7

        # Box BORDER:
        self.print_box(stdscr, begin_y, begin_x, begin_y + box_size_y, begin_x + box_size_x)

        sensor_data_type_1 = "Distance :"
        sensor_data_type_2 = "Count   A:"
        sensor_data_type_3 = "Count   B:"
        # sensor_data_type_4 = "                  "

        # Sensor name:
        stdscr.addstr(begin_y + 1, begin_x + 1, (sensor_name))
        # Sensor label1:
        stdscr.addstr(begin_y + 3, begin_x + 1, (sensor_data_type_1))
        stdscr.addstr(begin_y + 4, begin_x + 1, (sensor_data_type_2))
        stdscr.addstr(begin_y + 5, begin_x + 1, (sensor_data_type_3))

        if len(values) == 3:
            stdscr.addstr(begin_y + 3, begin_x + 12, '%6.2f' % values[0])
            stdscr.addstr(begin_y + 4, begin_x + 12, '%6.0f' % values[1])
            stdscr.addstr(begin_y + 5, begin_x + 12, str('%6.0f' % values[2]))


    def print_sensor_Force_values_with_border(self,stdscr, begin_y, begin_x, sensor_name, InData, Calibrated_data, Sensor_Type_i,
                                              Temperature):
        global ForceType_Name_LIST

        h, w = stdscr.getmaxyx()

        # Box size definition:
        box_size_x = 34
        box_size_y = 7

        # Box BORDER:
        self.print_box(stdscr, begin_y, begin_x, begin_y + box_size_y, begin_x + box_size_x)

        sensor_data_type_1 = "Get Data       :        dN      "
        sensor_data_type_2 = "Calibrated Data:        dN      "
        sensor_data_type_3 = "TYPE           :                "
        sensor_data_type_4 = "  -.  *C"

        # Sensor name:
        stdscr.addstr(begin_y + 1, begin_x + 1, (sensor_name))
        # Sensor label1:
        stdscr.addstr(begin_y + 3, begin_x + 1, (sensor_data_type_1))
        stdscr.addstr(begin_y + 4, begin_x + 1, (sensor_data_type_2))
        stdscr.addstr(begin_y + 5, begin_x + 1, (sensor_data_type_3))
        stdscr.addstr(begin_y + 6, begin_x + 1, (sensor_data_type_4))

        stdscr.addstr(begin_y + 3, begin_x + 19, str('%5.0f' % InData))
        stdscr.addstr(begin_y + 4, begin_x + 19, str('%5.0f' % Calibrated_data))
        stdscr.addstr(begin_y + 5, begin_x + 23, str(ForceType_Name_LIST[Sensor_Type_i]))

        # Temp data:
        stdscr.addstr(begin_y + 6, begin_x + 2, str('%5.2f' % Temperature))


    def print_list_name(self,stdscr, start_y, start_x, items):
        for i, val in enumerate(items):
            stdscr.addstr(start_y + i, start_x, val)


    def print_list_checkbox(self,stdscr, start_y, start_x, values, selected_row_idx):
        for i, row in enumerate(values):
            # If the value is True/False
            if values[i] == True:
                str_value = 'x'
            else:
                str_value = ' '

            stdscr.addstr(start_y + i, start_x, '[ ]')

            # Is it selected/ or not selected  -- Highlight or no
            if i == selected_row_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(start_y + i, start_x + 1, str_value)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(start_y + i, start_x + 1, str_value)


    def print_box(self,stdscr, ul_y, ul_x, dr_y, dr_x):
        # create a game box
        sh, sw = stdscr.getmaxyx()
        box = [[ul_y, ul_x], [dr_y, dr_x]]  # [[ul_y, ul_x], [dr_y, dr_x]]
        textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])


    def print_Logmode(self,stdscr, s_h, s_w):
        sh, sw = stdscr.getmaxyx()
        global Log_current_status_list
        global Log_current_status  # Log type 0: Off,  1: Started-for unlimited time,  2: Log Enabled devices for unlimited time    3: Log 20 measurement data  4: Log 1 measurement data
        global Log_i_measurement

        status_line = Log_current_status_list[Log_current_status]

        if Log_current_status == 0:
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(s_h, s_w, status_line)
            stdscr.addstr(s_h + 1, s_w, str('        ' + '%8.0f' % Log_i_measurement) + ' ')
            stdscr.attroff(curses.color_pair(3))
        else:
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(s_h, s_w, status_line)
            stdscr.addstr(s_h + 1, s_w, str('        ' + '%8.0f' % Log_i_measurement) + ' ')

            stdscr.attroff(curses.color_pair(2))


    def print_Liveview_menu(self,stdscr, text_header, text_list, c_current_row):
        self.print_debug(stdscr)
        h, w = stdscr.getmaxyx()
        for id_menu_x, row in enumerate(text_list):
            x = w - 18
            y = 1 + id_menu_x
            if id_menu_x == c_current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, (row))
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)
        # stdscr.refresh()
        self.screen_refresh(stdscr)


    # SELECTING OBJECTS FUNCTIONS:
    def select_box(self,stdscr, Topic_name, items, values):
        # Python keys: https://gist.github.com/Enteleform/a2e4daf9c302518bf31fcc2b35da4661

        prev_values = values  # ESC is not save the settings
        s_values = values
        prev_yes = False
        Topic_name = " " + Topic_name + " "

        # screen positions:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        s_current_row = 0
        b_start_x = w // 2 - 20
        b_Topic_x = w // 2 - len(Topic_name) // 2
        b_start_y = h // 2 - len(items) // 2 - 3
        b_end_x = w // 2 + 20
        b_end_y = h // 2 + len(items) // 2 + 3

        # Prints:
        self.print_box(stdscr, b_start_y, b_start_x, b_end_y, b_end_x)
        self.print_list_name(stdscr, b_start_y + 2, b_start_x + 3, items)
        self.print_list_checkbox(stdscr, b_start_y + 2, b_end_x - 5, s_values, s_current_row)
        stdscr.addstr(b_start_y, b_Topic_x, Topic_name)  # Topic name
        self.screen_refresh(stdscr)
        while 1:
            key = stdscr.getch()
            # UP and DOWN and ENTER KEY definition:
            if key == curses.KEY_UP and s_current_row > 0:
                s_current_row -= 1
            elif key == curses.KEY_DOWN and s_current_row < len(items) - 1:
                s_current_row += 1
            # PAGE DOWN
            elif key == curses.KEY_NPAGE:
                s_current_row = (len(items) - 1)
            # PAGE UP
            elif key == curses.KEY_PPAGE:
                s_current_row = 0

                # Change selected item              32- Space Tab:9
            elif key in [32, 9]:
                s_values[s_current_row] = not s_values[s_current_row]

            # Escape    27-ESC  113-q
            elif key in [27, 113]:
                prev_yes = True
                break

            # Enter
            elif key == curses.KEY_ENTER or key in [10, 13]:
                prev_yes = False

                break

            stdscr.clear()
            h, w = stdscr.getmaxyx()
            b_start_x = w // 2 - 20
            b_Topic_x = w // 2 - len(Topic_name) // 2
            b_start_y = h // 2 - len(items) // 2 - 3
            b_end_x = w // 2 + 20
            b_end_y = h // 2 + len(items) // 2 + 3

            # Prints:
            self.print_box(stdscr, b_start_y, b_start_x, b_end_y, b_end_x)
            self.print_list_name(stdscr, b_start_y + 2, b_start_x + 3, items)
            self.print_list_checkbox(stdscr, b_start_y + 2, b_end_x - 5, s_values, s_current_row)
            stdscr.addstr(b_start_y, b_Topic_x, Topic_name)  # Topic name

        if prev_yes:
            out = prev_values
        else:
            out = prev_values

        return (prev_values)


    def Confirmation_BOX_LEFT(self,stdscr, text_question, text_anwser, c_current_row):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        # Box or border to  Menu parameters:
        b_start_x = w // 2 - 20
        b_question_x = w // 2 - len(text_question) // 2
        b_start_y = h // 2 - len(text_anwser) // 2 - 3
        b_end_x = w // 2 + 20
        b_end_y = h // 2 + len(text_anwser) // 2 + 3
        # make a border to the menu:
        self.print_box(stdscr, b_start_y, b_start_x, b_end_y, b_end_x)
        # Text header
        stdscr.addstr(b_start_y + 1, b_question_x, text_question)
        self.print_menu_position(stdscr, c_current_row, text_anwser, b_start_x + 2)
        while 1:
            key = stdscr.getch()
            # UP and DOWN and ENTER KEY definition:
            if key == curses.KEY_UP and c_current_row > 0:
                c_current_row -= 1
            elif key == curses.KEY_DOWN and c_current_row < len(text_anwser) - 1:
                c_current_row += 1
            # PAGE DOWN
            elif key == curses.KEY_NPAGE:
                c_current_row = (len(text_anwser) - 1)
            # PAGE UP
            elif key == curses.KEY_PPAGE:
                c_current_row = 0
            elif key == curses.KEY_ENTER or key in [10, 13]:

                break
            # Update Screen:
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            # Box or border to  Menu parameters:
            b_start_x = w // 2 - 20
            b_question_x = w // 2 - len(text_question) // 2
            b_start_y = h // 2 - len(text_anwser) // 2 - 3
            b_end_x = w // 2 + 20
            b_end_y = h // 2 + len(text_anwser) // 2 + 3
            self.print_box(stdscr, b_start_y, b_start_x, b_end_y, b_end_x)
            stdscr.addstr(b_start_y + 1, b_question_x, text_question)
            self.print_menu_position(stdscr, c_current_row, text_anwser, b_start_x + 2)
        return (c_current_row)


    def Confirmation_BOX(self,stdscr, text_question, text_anwser, c_current_row):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        # Box or border to Main Menu parameters:
        b_start_x = w // 2 - 20
        b_question_x = w // 2 - len(text_question) // 2
        b_start_y = h // 2 - len(text_anwser) // 2 - 3
        b_end_x = w // 2 + 20
        b_end_y = h // 2 + len(text_anwser) // 2 + 3
        # make a border to the menu:
        self.print_box(stdscr, b_start_y, b_start_x, b_end_y, b_end_x)
        # Text header
        stdscr.addstr(b_start_y + 1, b_question_x, text_question)
        self.print_menu(stdscr, c_current_row, text_anwser)
        while 1:
            key = stdscr.getch()
            # UP and DOWN and ENTER KEY definition:
            if key == curses.KEY_UP and c_current_row > 0:
                c_current_row -= 1
            elif key == curses.KEY_DOWN and c_current_row < len(text_anwser) - 1:
                c_current_row += 1
            # PAGE DOWN
            elif key == curses.KEY_NPAGE:
                c_current_row = (len(text_anwser) - 1)
            # PAGE UP
            elif key == curses.KEY_PPAGE:
                c_current_row = 0
            elif key == curses.KEY_ENTER or key in [10, 13]:
                # print_center(stdscr, "You selected '{}'".format(text_anwser[c_current_row]))
                break
            # Update Screen:
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            # Box or border to Main Menu parameters:
            b_start_x = w // 2 - 20
            b_question_x = w // 2 - len(text_question) // 2
            b_start_y = h // 2 - len(text_anwser) // 2 - 3
            b_end_x = w // 2 + 20
            b_end_y = h // 2 + len(text_anwser) // 2 + 3
            self.print_box(stdscr, b_start_y, b_start_x, b_end_y, b_end_x)
            stdscr.addstr(b_start_y + 1, b_question_x, text_question)
            self.print_menu(stdscr, c_current_row, text_anwser)
        return (c_current_row)


    def exit_Confirmation(self,stdscr):
        #    anwser = ['Nem', 'Igen','123','2345','1234565']
        anwser = [' YES ', ' No  ']
        a_ok = self.Confirmation_BOX(stdscr, 'Do you want to EXIT?', anwser, 0)
        # a_ok is a choosed anwser:
        # 0 - Exit
        # 1 - Stay running
        if a_ok == 0:
            return True
        else:
            return False
        # LIVE VIEW:


    def Live_Full_Screen_loop(self,stdscr, text_header, text_anwser, c_current_row):
        global item_BT_enable_values  # BT settings values
        global item_BT
        global item_BT_sensor_ALL_values
        global item_Force  # IR settings name
        global item_Force_enable_values  # IR settings values
        global item_IR  # IR settings name
        global item_IR_enable_values  # IR settings values
        global item_IR_sensor_01_values
        global item_IR_sensor_ALL_values
        global item_Force  # Force measurement names
        global item_Force_enable_values  # Force enabled/disabled view and logging
        global item_Force_sensor_ALL_values  # Force measurement datas
        global item_Force_calibratins  # Calibration datas
        global item_Force_type_name_ID  # Type IDs of Force Node
        global Log_current_status

        # Screen refreshing time / or waiting time for pressing key:
        stdscr.nodelay(1)
        stdscr.timeout(1000)
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Box or border to Main Menu parameters:
        b_start_x = w - 20
        b_header_x = w // 2 - len(text_header) // 2
        b_start_y = 0
        b_end_x = w - 2
        b_end_y = 1 + len(text_anwser)

        # Sensor_BOX start positions
        Sensor_BOX_XY = [[2, 2], [10, 2], [18, 2], [26, 2],
                         [2, 37], [10, 37], [18, 37], [26, 37],
                         [2, 72], [10, 72], [18, 72], [26, 72],
                         [2, 107], [10, 107], [18, 107], [26, 107],
                         [2, 142], [10, 142], [18, 142], [26, 142]]

        # FIRST Printing:  ------------------------
        # make a border to the menu:
        self.print_box(stdscr, b_start_y, b_start_x, b_end_y, b_end_x)
        # Full Screen box
        self.print_box(stdscr, 0, 1, h - 1, w - 2)
        # Sensor Header:
        stdscr.addstr(1, 3, "Gyro data:")
        # Print Sensor Box                                 y x
        show_item_number = 0

        self.print_Logmode(stdscr, (b_end_y + 1), (w - 19))  # Is Log is running

        # Check the BT sensors is turned ON/OFF
        for i in range(len(item_BT)):
            # stdscr.addstr( i+20, 46, str(i))
            if item_BT_enable_values[i] == True:
                Acc = [item_BT_sensor_ALL_values[i][0], item_BT_sensor_ALL_values[i][1], item_BT_sensor_ALL_values[i][2]]
                Magn = [item_BT_sensor_ALL_values[i][3], item_BT_sensor_ALL_values[i][4], item_BT_sensor_ALL_values[i][5]]
                Gyro = [item_BT_sensor_ALL_values[i][6], item_BT_sensor_ALL_values[i][7], item_BT_sensor_ALL_values[i][8]]

                Temp = item_BT_sensor_ALL_values[i][11]  # Start  Y positions           Start X position
                self.print_sensor_bluetooth_values_with_border(stdscr, Sensor_BOX_XY[show_item_number][0],
                                                          Sensor_BOX_XY[show_item_number][1], item_BT[i], Acc, Magn, Gyro,
                                                          Temp)
                show_item_number = show_item_number + 1

        # Check the Force sensors is turned ON/OFF
        for i in range(len(item_Force)):
            # stdscr.addstr( i+20, 46, str(i))
            if item_Force_enable_values[i] == True:
                # a= [10.12,5,4]
                InData = item_Force_sensor_ALL_values[i][0]
                Calibrated_data = item_Force_sensor_ALL_values[i][1]
                Sensor_Type = item_Force_type_name_ID[i]
                # Sensor_Type = item_Force_type_name[i]
                Temperature = item_Force_sensor_ALL_values[i][5]

                self.print_sensor_Force_values_with_border(stdscr, Sensor_BOX_XY[show_item_number][0],
                                                      Sensor_BOX_XY[show_item_number][1], item_Force[i], InData,
                                                      Calibrated_data, Sensor_Type, Temperature)
                # print_sensor_Force_values_with_border(stdscr, begin_y,begin_x, sensor_name ,InData ,Calibrated_data ,Sensor_Type, Temperature)
                # print_sensor_Force_values_with_border(stdscr, begin_y,begin_x, sensor_name ,InData ,Calibrated_data ,Sensor_Type, Temperature)
                show_item_number = show_item_number + 1

        # Check the IR sensors is turned ON/OFF
        for i in range(len(item_IR)):
            # stdscr.addstr( i+20, 46, str(i))
            if item_IR_enable_values[i] == True:
                a = [item_IR_sensor_ALL_values[i][0], item_IR_sensor_ALL_values[i][1], item_IR_sensor_ALL_values[i][2]]

                # a= [10.12,5,4]
                self.print_sensor_IR_values_with_border(stdscr, Sensor_BOX_XY[show_item_number][0],
                                                   Sensor_BOX_XY[show_item_number][1], item_IR[i], a)
                show_item_number = show_item_number + 1

        # set_IR_Livedata( 1,   4.2,   20,   20, 3.12, 70, 24.3)
        stdscr.addstr(1, b_header_x, text_header)  #
        self.print_Liveview_menu(stdscr, text_header, text_anwser, c_current_row)  # Right Menu

        scr_change = False  # Check when should refresh the screen

        while 1:
            key = stdscr.getch()
            # c_prev_current_row = c_current_row
            # IS curren row change   -->  Screen refresh
            # UP and DOWN and ENTER KEY definition:
            if key == curses.KEY_UP and c_current_row > 0:
                c_current_row -= 1

            elif key == curses.KEY_DOWN and c_current_row < len(text_anwser) - 1:
                c_current_row += 1

            # PAGE DOWN
            elif key == curses.KEY_NPAGE:
                c_current_row = (len(text_anwser) - 1)

            # PAGE UP
            elif key == curses.KEY_PPAGE:
                c_current_row = 0

            # On press enter
            elif key == curses.KEY_ENTER or key in [10, 13]:
                # scr_change = True

                if c_current_row == len(text_anwser) - 1:
                    # EXIT TO MAIN MENU

                    break

                if c_current_row == 0:
                    # Start the LOG:
                    self.set_start_log(1)
                    # break

                if c_current_row == 1:
                    # END the LOG:
                    self.set_stop_log(0)
                    # set_start_log(1)
                    # break

                if c_current_row == 2:
                    # Make 20 Data log:
                    self.set_start_log(2)
                    # break

            self.get_live_data()
            scr_change = True

            if scr_change:
                # LOG:
                if Log_current_status > 0:
                    self.Log_Write_Selected_DATA(Log_Selected_Folder + Log_File_name + str(LOG_File_Number) + '.log')  # Filename

                # scr_change=False
                # Update Screen:
                stdscr.clear()
                h, w = stdscr.getmaxyx()

                # Box or border to Main Menu parameters:
                b_start_x = w - 20
                b_header_x = w // 2 - len(text_header) // 2
                b_start_y = 0
                b_end_x = w - 2
                b_end_y = 1 + len(text_anwser)

                # FIRST Printing:  ------------------------
                # make a border to the menu:
                self.print_box(stdscr, b_start_y, b_start_x, b_end_y, b_end_x)
                # Full Screen box
                self.print_box(stdscr, 0, 1, h - 1, w - 2)

                show_item_number = 0
                self.print_Logmode(stdscr, (b_end_y + 1), (w - 19))  # Is Log is running

                # Check the BT sensors is turned ON/OFF
                for i in range(len(item_BT)):
                    # stdscr.addstr( i+20, 46, str(i))
                    if item_BT_enable_values[i] == True:
                        Acc = [item_BT_sensor_ALL_values[i][0], item_BT_sensor_ALL_values[i][1],
                               item_BT_sensor_ALL_values[i][2]]
                        Magn = [item_BT_sensor_ALL_values[i][3], item_BT_sensor_ALL_values[i][4],
                                item_BT_sensor_ALL_values[i][5]]
                        Gyro = [item_BT_sensor_ALL_values[i][6], item_BT_sensor_ALL_values[i][7],
                                item_BT_sensor_ALL_values[i][8]]

                        Temp = item_BT_sensor_ALL_values[i][
                            11]  # Start  Y positions           Start X position
                        self.print_sensor_bluetooth_values_with_border(stdscr, Sensor_BOX_XY[show_item_number][0],
                                                                  Sensor_BOX_XY[show_item_number][1], item_BT[i], Acc, Magn,
                                                                  Gyro, Temp)
                        show_item_number = show_item_number + 1

                # Check the Force sensors is turned ON/OFF
                for i in range(len(item_Force)):
                    # stdscr.addstr( i+20, 46, str(i))
                    if item_Force_enable_values[i] == True:
                        # a= [10.12,5,4]
                        InData = item_Force_sensor_ALL_values[i][0]
                        Calibrated_data = item_Force_sensor_ALL_values[i][1]
                        Sensor_Type = item_Force_type_name_ID[i]
                        Temperature = item_Force_sensor_ALL_values[i][5]

                        self.print_sensor_Force_values_with_border(stdscr, Sensor_BOX_XY[show_item_number][0],
                                                              Sensor_BOX_XY[show_item_number][1], item_Force[i], InData,
                                                              Calibrated_data, Sensor_Type, Temperature)
                        show_item_number = show_item_number + 1

                # Check the IR sensors is turned ON/OFF
                for i in range(len(item_IR)):
                    if item_IR_enable_values[i] == True:
                        a = [item_IR_sensor_ALL_values[i][0], item_IR_sensor_ALL_values[i][1],
                             item_IR_sensor_ALL_values[i][2]]
                        self.print_sensor_IR_values_with_border(stdscr, Sensor_BOX_XY[show_item_number][0],
                                                           Sensor_BOX_XY[show_item_number][1], item_IR[i], a)
                        show_item_number = show_item_number + 1

                # Text header
                stdscr.addstr(1, b_header_x, text_header)
                self.print_Liveview_menu(stdscr, text_header, text_anwser, c_current_row)

        return (c_current_row)


    # MENU FUNCTIONS:
    def sub_main_bluetooth_settings(self,stdscr):
        global item_BT  # BT settings name
        global item_BT_enable_values  # BT settings values

        # Bluetooth devices Settings make a checkbox
        caption_name = 'Bluetooth settings'

        item_BT_enable_values = self.select_box(stdscr, caption_name, item_BT, item_BT_enable_values)


    def sub_main_bluetooth_LOG_columns(self,stdscr):
        global item_BT_sensor_values_header  # BT values topic/header
        global item_BT_selected_columns  # BT selected columns (values) to log
        # Bluetooth columns LOG setting up a checkbox
        caption_name = 'Bluetooth columns for LOG'
        item_BT_selected_columns = self.select_box(stdscr, caption_name, item_BT_sensor_values_header, item_BT_selected_columns)


    def sub_main_IR_settings(self,stdscr):
        global item_IR  # BT settings name
        global item_IR_enable_values  # BT settings values

        # Bluetooth devices Settings make a checkbox
        caption_name = 'IR settings'

        item_IR_enable_values = self.select_box(stdscr, caption_name, item_IR, item_IR_enable_values)


    def sub_main_IR_LOG_columns(self,stdscr):
        global item_IR_sensor_values_header  # BT values topic/header
        global item_IR_selected_columns  # BT selected columns (values) to log
        # Bluetooth columns LOG setting up a checkbox
        caption_name = 'IR columns for LOG'
        item_IR_selected_columns = self.select_box(stdscr, caption_name, item_IR_sensor_values_header, item_IR_selected_columns)


    def sub_main_Force_settings(self,stdscr):
        global item_Force  # Force settings name
        global item_Force_enable_values  # Force settings values

        # Bluetooth devices Settings make a checkbox
        caption_name = 'Force node settings'

        item_Force_enable_values = self.select_box(stdscr, caption_name, item_Force, item_Force_enable_values)


    def sub_main_Force_LOG_columns(self,stdscr):
        global item_Force_sensor_values_header  # BT values topic/header
        global item_Force_selected_columns  # BT selected columns (values) to log
        # Bluetooth columns LOG setting up a checkbox
        caption_name = 'Force columns for LOG'
        item_Force_selected_columns = self.select_box(stdscr, caption_name, item_Force_sensor_values_header,
                                                 item_Force_selected_columns)


    def sub_main_LOG_format_columns(self,stdscr):
        global LOG_settings_header  # ID, time,milisec, separators...
        global LOG_settings_values  # True/False

        # global item_Force_sensor_values_header # BT values topic/header
        # global item_Force_selected_columns     # BT selected columns (values) to log
        # Bluetooth columns LOG setting up a checkbox
        caption_name = 'LOG Format settings'
        LOG_settings_values = self.select_box(stdscr, caption_name, LOG_settings_header, LOG_settings_values)


    def main_menu_live(self,stdscr, type):
        #    anwser = ['Nem', 'Igen','123','2345','1234565']
        live_list = ['Start LOG       ',
                     'Stop LOG        ',
                     'Make 10 Data Log',
                     'Refresh Data    ',
                     '                ',
                     'Main Menu       ']
        if type == 0:
            str_type = 'Live data'
        elif type == 1:
            str_type = 'Live data with LOG'
        elif type == 2:
            str_type = 'Live data with custom LOG'

            # Live_Full_Screen_BOX(stdscr,str_type,live_list, 0 )

        anws_choosed = self.Live_Full_Screen_loop(stdscr, str_type, live_list, 0)

        return anws_choosed


    def main_selected_devices(self,stdscr):
        # 0 - Bluetooth
        # 1 - Force meter
        # 2 - IR node
        # 3 - LOG format
        # 4 - LOG folder
        # 5 - Load default settings
        # 6 - ABOUT
        # 7 - Back to main menu
        Settings_Loop = True

        anws_choosed = 0
        while Settings_Loop:
            settings_type = [
                ' Bluetooth   - Enabled Devices ',  # 0
                ' Bluetooth   - Columns to LOG  ',  # 1
                ' Force meter - Enabled Devices ',  # 2
                ' Force meter - Columns to LOG  ',  # 3
                ' IR          - Enabled Devices ',  # 4
                ' IR          - Columns to LOG  ',  # 5
                ' Back to main menu             ']  # 6

            anws_choosed = self.Confirmation_BOX_LEFT(stdscr, 'Settings', settings_type, anws_choosed)
            self.screen_refresh

            # If there was a selected menu, do the task
            if anws_choosed == 0:
                #  - Bluetooth   - Enabled Devices
                self.sub_main_bluetooth_settings(stdscr)

            elif anws_choosed == 1:
                #  - Bluetooth   - Columns to LOG
                self.sub_main_bluetooth_LOG_columns(stdscr)

            elif anws_choosed == 2:
                #  - Force meter - Enabled Devices
                self.sub_main_Force_settings(stdscr)

            elif anws_choosed == 3:
                #  - Force meter - Columns to LOG
                self.sub_main_Force_LOG_columns(stdscr)

            elif anws_choosed == 4:
                #  - IR          - Enabled Devices
                self.sub_main_IR_settings(stdscr)

            elif anws_choosed == 5:
                #  - IR          - Columns to LOG
                self.sub_main_IR_LOG_columns(stdscr)


            elif anws_choosed == 6:
                #  - Back to main menu
                # print_center(stdscr,"Back to Main Menu")
                Settings_Loop = False


    def main_selected_settings(self,stdscr):
        global Log_File_name
        # global Log_init                     # is it a new file?  --> f.write-header
        global Log_Selected_Folder  # Selected Folder
        # global Log_i_measurement            # In a log file - how many time has measurement the Datas

        Settings_Loop = True
        anws_choosed = 0
        while Settings_Loop:
            settings_type = [
                ' LOG filename                  ',  # 0
                ' LOG format                    ',  # 1
                ' LOG folder                    ',  # 2
                ' Load ALL settings to default  ',  # 3
                ' ABOUT                         ',  # 4
                ' Back to main menu             ']  # 5

            anws_choosed = self.Confirmation_BOX_LEFT(stdscr, 'Settings', settings_type, anws_choosed)
            self.screen_refresh

            # If there was a selected menu, do the task
            if anws_choosed == 0:
                #  - LOG filename
                # time.sleep(1)
                self.print_center(stdscr, "File name is: " + Log_File_name)
                time.sleep(2)

            elif anws_choosed == 1:
                #  - LOG format
                self.sub_main_LOG_format_columns(stdscr)
                # print_center(stdscr,"LOG FORMAT Service is unavailable")
                # time.sleep(1)


            elif anws_choosed == 2:
                #  - LOG folder
                self.print_center(stdscr, "LOG folder is: " + Log_Selected_Folder)
                # print_center(stdscr,"Service is unavailable")
                time.sleep(2)


            elif anws_choosed == 3:
                #  - Load ALL settings to default
                self.load_initial_settings_from_file(stdscr, "settings.json")
                time.sleep(1)
                # print_center(stdscr,"Service is unavailable")
                # time.sleep(1)

            elif anws_choosed == 4:
                #  - ABOUT
                self.print_center(stdscr, "Selected ABOUT")
                time.sleep(1)

            elif anws_choosed == 5:
                #  - Back to main menu
                # load_initial_settings_from_file(stdscr, "settings.json")
                Settings_Loop = False

                # print_center(stdscr,"Selected Load default settings")
                # time.sleep(1)


    def main_refresh_devices(self,stdscr):
        #    anwser = ['Nem', 'Igen','123','2345','1234565']
        anwser = [' All devices ', ' Bluetooth Devices ', ' SPI port ', ' SPI devices ', ' Force devices ',
                  ' Back to main menu ']
        anws_choosed = self.Confirmation_BOX(stdscr, 'Refresh devices', anwser, 0)
        # 0 - Bluetooth
        # 1 - Gyroscope
        # 2 - Force meter
        # 3 - IR node
        # 4 - LOG format
        # 5 - LOG folder
        # 6 - ABOUT
        return anws_choosed


    def main_GUI_START(self,stdscr):
        global main_menu
        self.initial_variables()

        # turn off cursor blinking
        curses.curs_set(0)

        # color scheme for selected row
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)

        # specify the current selected row
        current_row = 0

        # print the menu
        self.print_main_menu(stdscr, current_row)

        while 1:
            # print_main_menu(stdscr, current_row)
            key = stdscr.getch()

            # Arrow keys:   UP and DOWN:
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(main_menu) - 1:
                current_row += 1

            # PAGE DOWN
            elif key == curses.KEY_NPAGE:
                current_row = (len(main_menu) - 1)
            # PAGE UP
            elif key == curses.KEY_PPAGE:
                current_row = 0

            elif key == curses.KEY_ENTER or key in [10, 13]:
                # print_center(stdscr, "You selected '{}'".format(main_menu[current_row]))
                # IF Kilepes is selected:
                if current_row == len(main_menu) - 1:
                    if (self.exit_Confirmation(stdscr) == True):
                        # Here is the shutdown code:

                        # END of the shutdown code:
                        break
                    else:
                        # if not exit --> refresh screen
                        self.print_main_menu(stdscr, current_row)
                if current_row == 0:
                    self.main_menu_live(stdscr, 0)  # Live data
                if current_row == 1:
                    self.main_selected_devices(stdscr)  # Devices
                # if current_row == 2:
                #    main_menu_live(stdscr,2)  # Live data & Custom LOG
                # if current_row == 3:
                #    main_refresh_devices(stdscr)
                if current_row == len(main_menu) - 2:  # SETTINGS:
                    # choice = input_box_center(stdscr, 'Log name:')
                    self.main_selected_settings(stdscr)
                # stdscr.getch()
            # IF PRESS ESC --> select Exit

            self.print_main_menu(stdscr, current_row)


    def input_box(self,stdscr, h, w, question_str):
        curses.echo()
        stdscr.addstr(h, w, question_str)
        stdscr.refresh()
        input = stdscr.getstr(h + 1, w, 20)
        return input  # ^^^^  reading input at next line


    def input_box_center(self,stdscr, question_str):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        x = w // 2 - len(question_str) // 2
        y = h // 2 - 1
        # x = 10
        # y = 10

        # curses.echo()
        stdscr.addstr(x, y, question_str)
        screen_refresh(stdscr)
        # stdscr.refresh()

        input = stdscr.getstr(x + 1, y - 3, 20)
        return input  # ^^^^  reading input at next line


### TEST ### def main(stdscr):
### TEST ###     main_GUI_START(stdscr)
    # choice = input_box_center(stdscr, 'Log name:')


### TEST ### curses.wrapper(main)