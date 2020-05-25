import io
import sys
import fcntl
import time
import copy
import string
from datetime import datetime
from AtlasI2C import AtlasI2C
from RPi import GPIO
from Repositories.DataRepository import DataRepository
import lcd20x4
from subprocess import check_output

time_between_readings = 10
lcd_addr = 0x27

temp_file = "/sys/bus/w1/devices/w1_bus_master1/28-000009083444/w1_slave"
GPIO.setmode(GPIO.BCM)
motorPin = 15
GPIO.setup(motorPin, GPIO.OUT)


def return_ip():
    # get ip
    ips = check_output(['hostname', '--all-ip-addresses'])
    ips = str(ips)
    ip = ips.strip("b'").split(" ")
    return ip[0]

def get_devices():
    device = AtlasI2C()
    device_address_list = device.list_i2c_devices()
    device_list = []

    for i in device_address_list:
        if(i!=lcd_addr):
            device.set_i2c_address(i)
            response = device.query("I")
            moduletype = device.query("name,?").split(",")[1]
            device_list.append(AtlasI2C(address=i,moduletype=moduletype, name=response))

    return device_list

def print_devices(device_list, device):
    for i in device_list:
        if(i==device):
            print("--> " + i.get_device_info())
        else:
            print("--> " + i.get_device_info())

def read_sensor(address):
    device_list = get_devices()
    for i in device_list:
        if(i.address == int(address)):
            device = i
            output = device.query("R")
            output = str(output).split(" ")
            types = str(output[6]).split(",")
            result = []
            result.append(types[1])
            result.append(output[7].replace("\x00", ""))
            return result

def lights_off(address):
    device_list = get_devices()
    for i in device_list:
        if(i.address == int(address)):
            device = i
            device.query("L,0");

def lights_on(address):
    device_list = get_devices()
    for i in device_list:
        if(i.address == int(address)):
            device = i
            device.query("L,1");

def read_temperature():
    sensorfile = open(temp_file, 'r')
    for i, line in enumerate(sensorfile):
        if i == 1:  # 2de lijn
            result = []
            temp = int(line.strip('\n')[line.find('t=')+2:])/1000.0
            result.append("Graden ")
            result.append(temp)
            return result
    sensorfile.close()

def clear_lcd():
    lcd20x4.lcd_string(return_ip(),lcd20x4.LCD_LINE_1)
    lcd20x4.lcd_string(" ", lcd20x4.LCD_LINE_2)
    lcd20x4.lcd_string(" ", lcd20x4.LCD_LINE_3)
    lcd20x4.lcd_string(" ", lcd20x4.LCD_LINE_4)

device_list = get_devices()
device = device_list[0]

try:
    GPIO.output(motorPin,GPIO.LOW)
    lcd20x4.I2C_ADDR = lcd_addr
    lcd20x4.lcd_init()
    
    while True:
        clear_lcd()
        datum = datetime.now().replace(microsecond=0)
        GPIO.output(motorPin,GPIO.HIGH)
        DataRepository.post_new_pump_change(1,datum,1)
        dataPh = read_sensor(98)
        lcd20x4.lcd_string("Ph:   " + str(dataPh[1]), lcd20x4.LCD_LINE_2)
        DataRepository.post_new_reading(dataPh,datum,1)
        dataOrp = read_sensor(99)
        lcd20x4.lcd_string("Orp:  " + str(dataOrp[1]), lcd20x4.LCD_LINE_3)
        DataRepository.post_new_reading(dataOrp,datum,2)
        dataC = read_temperature()
        lcd20x4.lcd_string("C:    " + str(dataC[1]), lcd20x4.LCD_LINE_4)
        DataRepository.post_new_reading(dataC,datum,3)
        DataRepository.post_new_pump_change(1,datum,1)
        GPIO.output(motorPin,GPIO.LOW)
        DataRepository.post_new_pump_change(0,datum,1)
        
        time.sleep(time_between_readings)
except:
    clear_lcd()
    lcd20x4.I2C_ADDR = lcd_addr
    lcd20x4.lcd_toggle_enable(0)
    GPIO.cleanup()