from machine import Pin, PWM
import time

# Servo-Setup
SERVO_PINS = [18, 20, 26, 28]
servos = []

# PWM-Frequenz für Servos (50Hz)
for pin_num in SERVO_PINS:
    pwm = PWM(Pin(pin_num))
    pwm.freq(50)
    servos.append(pwm)

# Servo-Winkel in Mikrosekunden-Puls umwandeln und setzen
def set_servo_angle(pwm, angle):
    # Bereich: -70° bis +70°, Offset 90° (Mittelstellung)
    total_angle = 90 + angle  # ergibt Bereich 20° bis 160°
    min_us = 500
    max_us = 2500
    us = min_us + (max_us - min_us) * total_angle // 180
    duty = int(us * 65535 // 20000)
    pwm.duty_u16(duty)

# Testbewegung: Hin- und Herfahren zwischen -70° und +70°
while True:
    # Vorwärts von -70 bis +70
    for angle in range(-70, 71, 2):
        for pwm in servos:
            set_servo_angle(pwm, angle)
        time.sleep(0.02)

    # Rückwärts von +70 bis -70
    for angle in range(70, -71, -2):
        for pwm in servos:
            set_servo_angle(pwm, angle)
        time.sleep(0.02)
