import GPIO
LED_PIN = 18

GPIO.setup(LED_PIN, GPIO.OUT)

def led_on():
    GPIO.output(LED_PIN, True)

def led_off():
    GPIO.output(LED_PIN, False)
