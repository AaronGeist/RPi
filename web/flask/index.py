from flask import Flask, render_template, jsonify, Response
from features.Monitor import CpuTemperature, Memory
from features.Camera import Camera
from features.Servo import Servo
import time

app = Flask(__name__)

@app.route('/')
def hello():
     return 'Hello World'

@app.route('/name/<username>')
def hellouser(username):
     return 'Hello %s' % username

@app.route('/monitor/', methods=['GET', 'POST'])
def monitor():
    return render_template('monitor/index.html')

@app.route('/monitor/cpu/temperature', methods=['GET', 'POST'])
def monitor_cpu_temperature():
    return jsonify(CpuTemperature().history())

@app.route('/monitor/cpu/temperature/1', methods=['GET', 'POST'])
def monitor_cpu_temperature_single():
    return jsonify(CpuTemperature().latest())

@app.route('/monitor/memory/usage', methods=['GET', 'POST'])
def monitor_memory_usage():
    return jsonify(Memory().history())

@app.route('/monitor/memory/usage/1', methods=['GET', 'POST'])
def monitor_memory_usage_single():
    return jsonify(Memory().latest())

def gen(camera):
    while True:
        frame = camera.snapshot()
	yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        # sleep to make sure frame generation speed could match the show speed
        time.sleep(0.1)

@app.route('/monitor/camera/', methods=['GET', 'POST'])
def monitor_camera():
    return render_template('monitor/camera.html')

@app.route('/monitor/camera/left/', methods=['GET', 'POST'])
def monitor_camera_left():
    Servo.left()
    return ""

@app.route('/monitor/camera/right/', methods=['GET', 'POST'])
def monitor_camera_right():
    Servo.right()
    return ""

@app.route('/camera/', methods=['GET', 'POST'])
def camera():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
       app.run(host='0.0.0.0', port=8888, debug=True)
