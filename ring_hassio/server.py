from flask import Flask, request
from flask_restful import Resource, Api
import json
from flask import jsonify
import subprocess
import os

app = Flask(__name__)
api = Api(app)

pid = None

@app.route('/state')
def state():
    global pid
    res = ''
    if pid != None:
        try:
            os.kill(pid, 0)
        except OSError:
            res = 'off'
        else:
            res = 'on'
    else:
        res = 'off'
    resDict = { "state" : res }
    return json.dumps(resDict, sort_keys=True, indent=3)

@app.route('/start')
def start():
    global pid
    if pid == None:
        proc = subprocess.Popen("node livestream.js", stdout=subprocess.PIPE)
        pid = proc.pid
    return state()
    

@app.route('/stop')
def stop():
    global pid
    if pid != None:
        os.kill(pid, 9)
        pid = None
    return state()


if __name__ == '__main__':
    app.run(port='5002')
