import io
import sys
import fcntl
import time
import copy
import string
from datetime import datetime
from AtlasI2C import AtlasI2C
from Repositories.DataRepository import DataRepository

temp_file = "/sys/bus/w1/devices/w1_bus_master1/28-000009083444/w1_slave"

def get_devices():
    device = AtlasI2C()
    device_address_list = device.list_i2c_devices()
    device_list = []

    for i in device_address_list:
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

device_list = get_devices()
device = device_list[0]

while True:
    datum = datetime.now().replace(microsecond=0)
    DataRepository.post_new_reading(read_sensor(98),datum,1)
    DataRepository.post_new_reading(read_sensor(99),datum,2)
    DataRepository.post_new_reading(read_temperature(),datum,3)
    DataRepository.post_new_pump_change(1,datum,1)
    time.sleep(4)