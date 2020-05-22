from Repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS

import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hier mag je om het even wat schrijven, zolang het maar geheim blijft en een string is'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

endpoint = "/aquastats/api/v1/"

@app.route(endpoint + "sensors", methods = ['GET'])
def read_sensors():
    if(request.method == "GET"):
        output = DataRepository.read_all_sensors()
        return jsonify(sensors=output), 200

@app.route(endpoint + "readings/<date>/<sensorID>", methods = ['GET'])
def read_all_values_by_date(date,sensorID):
    if(request.method == "GET"):
        output = DataRepository.read_all_readings_by_date(date)
        new_out = []
        for i in output:
            if(i['SensorID']==int(sensorID)):
                new_out.append(i)
        return jsonify(readings=new_out), 200

@app.route(endpoint + "five-readings/<date>/<sensorID>", methods = ['GET'])
def read_all_values_by_date_limit5(date,sensorID):
    if(request.method == "GET"):
        output = DataRepository.read_all_readings_by_date_limit5(date)
        new_out = []
        for i in output:
            if(i['SensorID']==int(sensorID)):
                new_out.append(i)
        return jsonify(readings=new_out), 200

@app.route(endpoint + "pump", methods = ['GET'])
def read_pump():
    if request.method == "GET":
        output = DataRepository.get_pump_status()
        return jsonify(pump=output),200

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')

