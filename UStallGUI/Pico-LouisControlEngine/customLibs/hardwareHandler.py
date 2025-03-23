from machine import UART, Pin, PWM
import time
import asyncio

class HardwareHandler:
    def __init__(self):
        # Motor setup
        self.mot_pwm_pins = [0, 2, 4, 6, 8, 10]
        self.mot_pwms = [None] * len(self.mot_pwm_pins)
        
        # UART setup
        self.uart = UART(0, baudrate=115200, tx=Pin(12), rx=Pin(13))

        # LED setup
        self.led = Pin(25, Pin.OUT)
        
        self.last_message_sent = None

    def init_motor_all(self):
        """Initialize all motors."""
        for i in range(len(self.mot_pwm_pins)):
            self.mot_pwms[i] = PWM(Pin(self.mot_pwm_pins[i]))
            self.mot_pwms[i].freq(50)

    def set_motor_speed_all(self, pwm_values):
        """Set speed for all motors based on throttle input."""
        for i in range(len(self.mot_pwms)):
            self.mot_pwms[i].duty_u16(int(pwm_values[i] * 65535 / 20000))
            
    def send_message_code_uart(self, message_code):
        if self.last_message_sent is not message_code:
            self.uart.write(bytes([message_code] * 7))
            last_message_sent = message_code



        

