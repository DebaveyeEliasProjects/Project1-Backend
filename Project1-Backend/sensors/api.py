from Repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
import datetime
import time
import threading
from subprocess import check_output
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
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hier mag je om het even wat schrijven, zolang het maar geheim blijft en een string is'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

endpoint = "/aquastats/api/v1/"

@socketio.on('connect')
def connection():
    print("A new client connected")

@app.route(endpoint + "devices", methods = ['GET'])
def read_sensors():
    if(request.method == "GET"):
        output = DataRepository.read_all_sensors()
        return jsonify(sensors=output), 200

@app.route(endpoint + "readings/<date>/<id>", methods=['GET'])
def read_all_readings_for_day(date, id):
    if request.method == 'GET':
        print(date)
        output1 = DataRepository.readings_by_sensor_and_date(date,id)
        new_out = []
        for x in output1:
            d = {
                "MetingID": x['MeetingID'],
                "Datum": x['Datum'].strftime("%Y-%m-%d %H:%M:%S"),
                "Waarde": x['Waarde'],
                "DeviceID": x["DeviceID"],
                "Eenheid": x["Eenheid"]
            }
            new_out.append(d)
        return jsonify(readings=new_out), 200


@app.route(endpoint + "readings/<date>/<DeviceID>", methods = ['GET'])
def read_all_values_by_date(date,DeviceID):
    if(request.method == "GET"):
        output = DataRepository.read_all_readings_by_date(date)
        new_out = []
        for i in output:
            if(i['DeviceID']==int(DeviceID)):
                new_out.append(i)
        return jsonify(readings=new_out), 200

@app.route(endpoint + "five-readings/<date>/<DeviceID>", methods = ['GET'])
def read_all_values_by_date_limit5(date,DeviceID):
    if(request.method == "GET"):
        output = DataRepository.read_all_readings_by_date_limit5(date)
        new_out = []
        for i in output:
            if(i['DeviceID']==int(DeviceID)):
                new_out.append(i)
        return jsonify(readings=new_out), 200



@app.route(endpoint + "last-five-readings/<DeviceID>", methods = ['GET'])
def read_last_5_readings(DeviceID):
    if(request.method == "GET"):
        output = DataRepository.get_last_five_readings(DeviceID)
        new_out = []
        for x in output:
            d = {
                "MetingID": x['MeetingID'],
                "Datum": x['Datum'].strftime("%Y-%m-%d %H:%M:%S"),
                "Waarde": x['Waarde'],
                "DeviceID": x["DeviceID"],
                "Eenheid": x["Eenheid"]
            }
            new_out.append(d)
        return jsonify(readings=new_out), 200

@app.route(endpoint + "pump", methods = ['GET'])
def read_pump():
    if request.method == "GET":
        output = DataRepository.get_pump_status()
        
        return jsonify(pump=output),200

@app.route(endpoint + "dates", methods = ['GET'])
def read_dates():
    if(request.method == "GET"):
        output = DataRepository.get_dates()
        dates = []
        for i in output:
            t = i['Datum'].strftime("%Y-%m-%d")
            dates.append(t)
        return jsonify(dates =dates)

@app.route(endpoint + "5dates", methods = ['GET'])
def read_5dates():
    if(request.method == "GET"):
        output = DataRepository.get_last_five_dates()
        dates = []
        for i in output:
            t = i['Datum'].strftime("%Y-%m-%d %H:%M:%S")
            dates.append(t)
        return jsonify(dates =dates)

##SENSI PROGRAM

temp_file = "/sys/bus/w1/devices/w1_bus_master1/28-000009083444/w1_slave"
GPIO.setmode(GPIO.BCM)
motorPin = 18
GPIO.setup(motorPin, GPIO.OUT)
time_between_readings = 60*20
lcd_addr = 0x27


def return_ip():
    # get ip
    ips = check_output(['hostname', '--all-ip-addresses'])
    ips = str(ips)
    ip = ips.strip("b'").split(" ")
    return ip[1]

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

def send_pump_data(pumpstatus):
    socketio.emit("B2F_pump_change",{"pump":pumpstatus})

def selc_control():
    GPIO.output(motorPin,GPIO.LOW)
    lcd20x4.I2C_ADDR = lcd_addr
    lcd20x4.lcd_init()
    clear_lcd()

    send_pump_data(1)
    
    datum = datetime.now().replace(microsecond=0)
    GPIO.output(motorPin,GPIO.HIGH)
    DataRepository.post_new_pump_change(1,7)
    dataPh = read_sensor(99)
    lcd20x4.lcd_string("pH:   " + str(dataPh[1]), lcd20x4.LCD_LINE_2)
    DataRepository.post_new_reading(dataPh,4)
    dataOrp = read_sensor(98)
    lcd20x4.lcd_string("ORP:  " + str(dataOrp[1]), lcd20x4.LCD_LINE_3)
    DataRepository.post_new_reading(dataOrp,5)
    dataC = read_temperature()
    lcd20x4.lcd_string("C:    " + str(dataC[1]), lcd20x4.LCD_LINE_4)
    DataRepository.post_new_reading(dataC,6)
    GPIO.output(motorPin,GPIO.LOW)
    
    send_pump_data(0)

    DataRepository.post_new_pump_change(0,7)
    socketio.emit('B2F_self_control', {"ph":dataPh[1],"orp":dataOrp[1],"degrees":dataC[1]})   
    socketio.emit('B2F_verandering_data', {"ph":dataPh[1],"orp":dataOrp[1],"degrees":dataC[1]}) 


def program_code():
    GPIO.output(motorPin,GPIO.LOW)
    lcd20x4.I2C_ADDR = lcd_addr
    lcd20x4.lcd_init()
    clear_lcd()
    datum = datetime.now().replace(microsecond=0)
    GPIO.output(motorPin,GPIO.HIGH)
    DataRepository.post_new_pump_change(1,7)
    dataPh = read_sensor(99)
    lcd20x4.lcd_string("pH:   " + str(dataPh[1]), lcd20x4.LCD_LINE_2)
    DataRepository.post_new_reading(dataPh,4)
    dataOrp = read_sensor(98)
    lcd20x4.lcd_string("ORP:  " + str(dataOrp[1]), lcd20x4.LCD_LINE_3)
    DataRepository.post_new_reading(dataOrp,5)
    dataC = read_temperature()
    lcd20x4.lcd_string("C:    " + str(dataC[1]), lcd20x4.LCD_LINE_4)
    DataRepository.post_new_reading(dataC,6)
    GPIO.output(motorPin,GPIO.LOW)
    DataRepository.post_new_pump_change(0,7)

    socketio.emit('B2F_verandering_data', {"ph":dataPh[1],"orp":dataOrp[1],"degrees":dataC[1]})   
    time.sleep(time_between_readings)


@socketio.on("F2B_ButtonPressed")
def button_pressed():
    selc_control()

def programma():
    
    try:
        while True:
            # pass
            program_code()
    except:
        clear_lcd()
        lcd20x4.I2C_ADDR = lcd_addr
        lcd20x4.lcd_toggle_enable(0)
        GPIO.cleanup()

threading.Timer(15, programma).start()

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0',port=5000)

    programma()
    

