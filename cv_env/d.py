import RPi.GPIO as gpio
import time
import cv2
import threading
from flask import Flask, render_template_string, Response

# GPIO 핀 설정
TRIGGER = 24
ECHO = 23
LED = 18
SWITCH = 25

# GPIO 초기화
gpio.setmode(gpio.BCM)
gpio.setup(TRIGGER, gpio.OUT)
gpio.setup(ECHO, gpio.IN)
gpio.setup(LED, gpio.OUT)
gpio.setup(SWITCH, gpio.IN, pull_up_down=gpio.PUD_UP)

# 거리 및 시간 임계값 설정
MIN_DIST = 10
MAX_DIST = 30
TIME_THRESHOLD = 5  # seconds

# Flask 웹 서버 설정
app = Flask(__name__)

# 웹 페이지 템플릿
html_template = """
<!doctype html>
<html>
    <head>
        <title>택배 알리미</title>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script>
            var evtSource = new EventSource("/stream");
            evtSource.onmessage = function(event) {
                document.getElementById('distance').innerText = event.data + ' cm';
            };
        </script>
    </head>
    <body>
        <h1>택배 알리미</h1>
        <p>현재 물체와의 거리: <span id="distance">-</span></p>
        <img src="{{ url_for('video_feed') }}" alt="라이브 CCTV">
    </body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

def calculate_distance():
    while True:
        gpio.output(TRIGGER, gpio.LOW)
        time.sleep(0.1)
        gpio.output(TRIGGER, gpio.HIGH)
        time.sleep(0.00001)
        gpio.output(TRIGGER, gpio.LOW)

        while gpio.input(ECHO) == gpio.LOW:
            pulse_start = time.time()

        while gpio.input(ECHO) == gpio.HIGH:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = round(pulse_duration * 17150, 2)  # 음속 343m/s, 왕복 거리

        yield str(distance)

@app.route('/stream')
def stream():
    return Response(calculate_distance(), mimetype='text/event-stream')

def video_feed():
    camera = cv2.VideoCapture(0)

    def generate_frames():
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed')
def video_feed_route():
    return Response(video_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

def capture_loop():
    global led_on, in_range_start_time
    led_on = False
    in_range_start_time = None
    try:
        while True:
            if gpio.input(SWITCH) == gpio.LOW:  # 스위치가 눌렸을 때
                gpio.output(LED, gpio.LOW)
                led_on = False
                in_range_start_time = None
                time.sleep(1)  # 스위치 입력 안정화

            gpio.output(TRIGGER, gpio.LOW)
            time.sleep(0.1)
            gpio.output(TRIGGER, gpio.HIGH)
            time.sleep(0.00002)
            gpio.output(TRIGGER, gpio.LOW)

            while gpio.input(ECHO) == gpio.LOW:
                pulse_start = time.time()

            while gpio.input(ECHO) == gpio.HIGH:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = round(pulse_duration * 17150, 2)  # 음속 343m/s, 왕복 거리

            if MIN_DIST <= distance <= MAX_DIST:
                if in_range_start_time is None:
                    in_range_start_time = time.time()
                elif time.time() - in_range_start_time >= TIME_THRESHOLD:
                    gpio.output(LED, gpio.HIGH)
                    led_on = True
            else:
                in_range_start_time = None
                if not led_on:
                    gpio.output(LED, gpio.LOW)

    except KeyboardInterrupt:
        gpio.cleanup()

if __name__ == '__main__':
    # 센서 스레드 시작
    sensor_thread = threading.Thread(target=capture_loop)
    sensor_thread.start()

    # Flask 웹 서버 실행
    app.run(host='0.0.0.0', port=5000)
