from picamera2 import Picamera2
from time import sleep

# Picamera2 초기화
camera = Picamera2()

def capture_image(image_path):
    camera.start()
    sleep(5)  # 카메라 준비 시간
    camera.capture_file(image_path)
    camera.stop()

capture_image('./catpure.png')