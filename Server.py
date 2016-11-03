from flask import Flask, render_template, request
from json import dumps



app = Flask(__name__)

DEBUG = True

def return_response(result):
    return dumps({'error' : False , 'result' : result})
def return_error(error_description):
    return dumps({'error' : True, 'error_description' : str(error_description)})
done_response = return_response({"Done" : True})

devices = devices.devices()
devices.__enter__()
measurements = []
threads = []

def find_device(name):
    for device in devices:
        if name == device.name:
            return device
    raise Exception("Device Wasn't found")

@app.route("/devices/")
def list_devices():
    return dumps([i.to_dict() for i in devices])

@app.route('/console/')
def console():
    return render_template("terminal.html")

@app.route('/update_property/', methods=['POST'])
def update_property():
    try :
        request.get_data()
        device = find_device(request.json["name"])
        for property in request.json['properties']:
            name, value = property['name'], property['value']
            device.object.set_property(name, value)
    except Exception as e:
        return return_error(e)
    return done_response

@app.route('/update_output/', methods=['POST'])
def update_output():
    try :
        request.get_data()
        device = find_device(request.json["name"])
        device.object.write_output(request.json['output'], request.json['value'])
        return done_response
    except Exception as e:
        return return_error(e)

@app.route('/begin_measurement/', methods = ['POST'])
def measure():
    try :
        request.get_data()
        print(request.json)
        meas = Measurement(request.json, find_device)
        measurements.append(meas)
        thread = threading.Thread(target=meas.run, args=())
        threads.append(thread)
        thread.start()
        return return_response({"measurement_id" : id(meas)})
    except Exception as e:
        return return_error(e)

@app.route("/measurement/<int:measurement_id>/")
def get_measurement(measurement_id):
    try:
        if measurement_id not in map(id, measurements):
            raise exception("Cannot find measurement")
        for measurement in measurements:
            if id(measurement) == int(measurement_id):
                return return_response(measurement.to_dict())
    except Exception as e:
        return return_error(e)

@app.route("/stop_measurement/<int:measurement_id>/")
def stop_measurement(measurement_id):
    try:
        if measurement_id not in map(id, measurements):
            raise Exception("Cannot find measurement")
        for measurement in measurements:
            if id(measurement) == int(measurement_id):
                measurement.running = False
                return return_response({"Stopped" : True})
    except Exception as e:
        return return_error(e)

if __name__ == "__main__":
    try : 
        app.run(use_reloader = False)
        devices.__exit__()
    except : 
        devices.__exit__()

