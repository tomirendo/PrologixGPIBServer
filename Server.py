import sys
from flask import Flask, render_template, request
from json import dumps
from controller import PrologixDevice
from base64 import b64decode
from urllib.parse import unquote

app = Flask(__name__)

DEBUG = True

def return_response(result):
    return dumps({'error' : False , 'result' : result})
def return_error(error_description):
    return dumps({'error' : True, 'error_description' : str(error_description)})
done_response = return_response({"Done" : True})

prologix_device = PrologixDevice(sys.argv[1])
prologix_device.__enter__()

@app.route('/write/<int:device_id>/<command>/')
def write(device_id, command):
    try :
        print(command)
        command = b64decode(command)
        prologix_device.write(device_id, command)
    except Exception as e:
        return return_error(e)
    return done_response

@app.route('/query/<int:device_id>/<command>/')
def query(device_id, command):
    try :
        print(command)
        command = b64decode(command)
        result = prologix_device.query(device_id, command)
        return return_response({"data" : result})
    except Exception as e:
        return return_error(e)

@app.route('/read/<int:device_id>/')
def read(device_id):
    try :
        result = prologix_device.read(device_id)
        return return_response({"data" : result})
    except Exception as e:
        return return_error(e)

if __name__ == "__main__":
    try : 
        app.run(use_reloader = False, port = int(sys.argv[2]))
        prologix_device.__exit__()
    except : 
        prologix_device.__exit__()


