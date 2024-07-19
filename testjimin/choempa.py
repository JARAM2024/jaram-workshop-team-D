import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
TRIG_PIN = 23
ECHO_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

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
