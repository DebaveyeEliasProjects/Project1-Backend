import io
import sys
import fcntl
import time
import copy
import string
from AtlasI2C import AtlasI2C
from Repositories.DataRepository import DataRepository


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
            result.append(output[7])
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

device_list = get_devices()
device = device_list[0]


lights_on(98)
lights_on(99)