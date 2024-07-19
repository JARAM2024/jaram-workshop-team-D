import RPi.GPIO as GPIO
import time
import threading
from flask import Flask, send_file
from picamera2 import Picamera2
from time import sleep

# GPIO 핀 설정
TRIG_PIN = 23
ECHO_PIN = 24
LED_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

app = Flask(__name__)
camera = Picamera2()

# 거리 측정 함수
def measure_distance():
    # 트리거 핀을 10us 동안 HIGH로 설정
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # 에코 핀이 HIGH로 변할 때까지 대기
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    # 에코 핀이 LOW로 변할 때까지 대기
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    # 시간 차이를 통해 거리 계산
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # cm로 변환

    return distance

# LED 제어 함수
def led_on():
    GPIO.output(LED_PIN, True)

def led_off():
    GPIO.output(LED_PIN, False)

# 카메라 이미지 캡처 함수
def capture_image(image_path):
    camera.start_preview()
    sleep(2)  # 카메라 준비 시간
    camera.capture_file(image_path)
    camera.stop_preview()

# 거리 측정 및 LED 제어 함수
def detect_package():
    while True:
        distance = measure_distance()
        print(f"Measured Distance: {distance} cm")
        if distance < 20:  # 예: 20cm 이내에 물체가 있으면
            led_on()
            capture_image('/home/pi/captured_image.jpg')
        else:
            led_off()
        time.sleep(1)

# 웹 서버 설정
@app.route('/image')
def get_image():
    return send_file('/home/pi/captured_image.jpg', mimetype='image/jpeg')

# 백그라운드에서 실행할 스레드 시작
threading.Thread(target=detect_package, daemon=True).start()

# 웹 서버 실행
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

