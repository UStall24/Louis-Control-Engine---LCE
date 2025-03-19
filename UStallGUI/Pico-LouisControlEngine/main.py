from machine import UART, Pin, PWM
import time

motV1_out_pwm = 8
motV2_out_pwm = 2
motV3_out_pwm = 4
motH1_out_pwm = 6
motH2_out_pwm = 0
motH3_out_pwm = 10

motV1_pwm = None
motV2_pwm = None
motV3_pwm = None
motH1_pwm = None
motH2_pwm = None
motH3_pwm = None

maxPWM = 1700
minPWM = 1300
deadZoneMin = 1464
deadZoneMax = 1536
deadZoneDefault = 1500

uart = UART(0, baudrate=115200, tx=Pin(12), rx=Pin(13))

motorvalues = [deadZoneDefault] * 6


def set_motor_speed_all(throttle_values):
    global motV1_pwm, motV2_pwm, motV3_pwm, motH1_pwm, motH2_pwm, motH3_pwm
    pwm_values = [0] * len(throttle_values)
    for i in range(len(throttle_values)):
        pwm_values[i] = calculate_pwm_value(throttle_values[i])
        
    print(pwm_values)

    motV1_pwm.duty_u16(int(pwm_values[0] * 65535 / 20000))
    motV2_pwm.duty_u16(int(pwm_values[1] * 65535 / 20000))
    motV3_pwm.duty_u16(int(pwm_values[2] * 65535 / 20000))
    motH1_pwm.duty_u16(int(pwm_values[3] * 65535 / 20000))
    motH2_pwm.duty_u16(int(pwm_values[4] * 65535 / 20000))
    motH3_pwm.duty_u16(int(pwm_values[5] * 65535 / 20000))

def calculate_pwm_value(throttle_value):
    reverse_range = deadZoneDefault - minPWM
    forward_range = maxPWM - deadZoneDefault
    throttle_value = (throttle_value / 127.5) - 1
    
    if throttle_value <= 0:
        pwmVal = deadZoneDefault + throttle_value * reverse_range
    else:
        pwmVal = deadZoneDefault + throttle_value * forward_range
    
    if deadZoneMin < pwmVal < deadZoneMax:
        pwmVal = deadZoneDefault
    return pwmVal
   
    
def init_motor_all():
    global motV1_pwm, motV2_pwm, motV3_pwm, motH1_pwm, motH2_pwm, motH3_pwm
    motV1_pwm = PWM(Pin(motV1_out_pwm))
    motV2_pwm = PWM(Pin(motV2_out_pwm))
    motV3_pwm = PWM(Pin(motV3_out_pwm))
    motH1_pwm = PWM(Pin(motH1_out_pwm))
    motH2_pwm = PWM(Pin(motH2_out_pwm))
    motH3_pwm = PWM(Pin(motH3_out_pwm))
    
    motV1_pwm.freq(50)
    motV2_pwm.freq(50)
    motV3_pwm.freq(50)
    motH1_pwm.freq(50)
    motH2_pwm.freq(50)
    motH3_pwm.freq(50)
    
    set_motor_speed_all([0x7F, 0x7F, 0x7F, 0x7F, 0x7F, 0x7F])

print("Prog started")
motors_init = False

while True:
    try:       
        if uart.any():  
            data = uart.read()  
            if data:
                print("Received data (hex):", " ".join(f"{byte:02X}" for byte in data))
                if motors_init and len(data) == 7:
                    if data[0] == 0x69:
                        motor_values = [byte for byte in data[1:7]]
                        set_motor_speed_all(motor_values)
            
                if not motors_init:
                    if data == bytes([0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]):
                        init_motor_all()
                        motors_init = True
                        print("Motors initialized")
                        uart.write(b"init motors success")

    except Exception as e:
        print(f"Error: {e}")
    time.sleep(0.1)

print("Prog finished")

