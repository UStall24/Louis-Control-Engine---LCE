from machine import Pin, PWM, UART
import time

# Konstanten
SERVO_PINS = [18, 20, 26, 28]
NUM_SERVOS = 4
LED_PIN = 25
UART0_TX = 0
UART0_RX = 1
BAUDRATE = 115200
INTERVAL_MS = 1000  # 1 Sekunde

# Setup UART
uart = UART(0, baudrate=BAUDRATE, tx=Pin(UART0_TX), rx=Pin(UART0_RX))

# Setup LED
led = Pin(LED_PIN, Pin.OUT)
led_state = False
previous_millis = time.ticks_ms()

# Setup Servos
servos = []
for pin_num in SERVO_PINS:
    pwm = PWM(Pin(pin_num))
    pwm.freq(50)  # 50 Hz für Standard-Servos
    servos.append(pwm)

# Funktion zur Umrechnung von Winkel in PWM-Duty für Servo
def set_servo_angle(pwm, angle):
    min_us = 500
    max_us = 2500
    us = min_us + (max_us - min_us) * angle // 180
    duty = int(us * 65535 // 20000)  # 20ms Zyklus -> 50Hz
    pwm.duty_u16(duty)

# Anfangsposition
for pwm in servos:
    set_servo_angle(pwm, 20)

print("Hallo, Raspberry Pi Pico!")

# Hauptschleife
while True:
    # Prüfen, ob genug Daten vorhanden sind
    if uart.any() >= NUM_SERVOS:
        # Lese Werte ein
        values = uart.read(NUM_SERVOS)
        if values:
            for i in range(NUM_SERVOS):
                val = values[i]
                angle = int(val * 180 / 255)
                set_servo_angle(servos[i], angle)
            print("Wert:", values[1])

    # LED-Blinken (0,5 Hz)
    current_millis = time.ticks_ms()
    if time.ticks_diff(current_millis, previous_millis) >= INTERVAL_MS:
        previous_millis = current_millis
        led_state = not led_state
        led.value(led_state)
