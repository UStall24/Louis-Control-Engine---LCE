import time
from customLibs.hardwareHandler import HardwareHandler
from customLibs.calculator import Calculator
from customLibs.configLoader import*
from customLibs.gyroscopeMPU6050 import gyroscope
from math import atan2, sqrt

verbose = True

direction_values_path = "directionValues.json"
direction_values = read_json_file(direction_values_path)

state = 0
cycle_time = 20  # 50ms loop cycle time
hardware = HardwareHandler()
calculator = Calculator(direction_values)
last_send_address = 0x00

last_execution_time_1000ms = time.ticks_ms()  # Store the last execution time
last_execution_time_100ms = time.ticks_ms()  # Store the last execution time

led_toggles = 0

def print_verbose(msg):
    if verbose:
        print(msg)

def task_one_herz(): # Execution every second
    global state, led_toggles
    if state == 0:  # Waiting init State
        led_toggles += 4
    elif state == 1:  # Execute mode State
        led_toggles += 2
    elif state == 2:  # Error mode State
        led_toggles += 6
    
def task_ten_herz(): # Execution every 100ms
    global led_toggles
    if led_toggles > 0:
        hardware.led.value(1 - hardware.led.value())  # Toggle LED
        led_toggles -= 1  # Decrement the toggle count
    else:
        hardware.led.value(0)  # Turn off the LED
        
def apply_pwm_raw(data):
    motor_values = list(data[1:7])
    pwm_values = calculator.calc_all_motor_pwm(motor_Values, True)
    print_verbose(pwm_values)
    hardware.set_motor_speed_all(pwm_values)
    hardware.send_message_code_uart(0x02)

def apply_controller_values(data):
    controller_values = list(data[1:8])
    throttle_value = calculator.calc_throttle_value2(controller_values)
    #print_verbose("Throttle value:", throttle_value)
    pwm_values = calculator.calc_all_motor_pwm(throttle_value, False)
    #print_verbose("PWM value:", pwm_values)
    hardware.set_motor_speed_all(pwm_values)

def print_as_hex(byte_array):
    msg = "Received data (hex):" + " ".join(f"{byte:02X}" for byte in byte_array)
    print_verbose(msg)


print_verbose("Program started. Waiting for initialization...")

while True:
    start_time = time.ticks_ms()

    # Run periodic task every 1000ms (1 second)
    if time.ticks_diff(start_time, last_execution_time_1000ms) >= 1000:
        task_one_herz()
        last_execution_time_1000ms = start_time  # Reset timer
    if time.ticks_diff(start_time, last_execution_time_100ms) >= 100:
        task_ten_herz()
        last_execution_time_100ms = start_time  # Reset timer
    
    try:
        if hardware.uart.any():
            data = hardware.uart.read()
            if data:
                print_as_hex(data)
                
                if data == bytes([0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]):
                    hardware.init_motor_all()
                    print_verbose("Motors initialized")
                    hardware.send_message_code_uart(0x01)
                    state = 1
                
                if hardware.mot_pwms[0] != None:
                    if len(data) == 7 and data[0] == 0x69:
                        apply_pwm_raw(data)
                    elif len(data) == 8 and data[0] == 0x96:
                        apply_controller_values(data)
                
                if data[0] == 0x10:
                    print_verbose("Sending direction values")
                    payload = get_direction_uart_values_payload(calculator.direction_values)
                    
                    for motor_values in payload:
                        print_verbose(f"Sending: {motor_values}")  # Debugging print
                        hardware.uart.write(bytes(motor_values))
                        time.sleep(0.02)
                        
                if data[0] == 0x30:
                    print_verbose("Send PID values")
                    payload = bytes([0x31, calculator.Kp, calculator.Kd])
                    hardware.uart.write(payload)
    
                if data[0] == 0x21:
                    if len(data) == 7 * 6:
                        new_direction_values_matrix = []
                        for i in range(6):
                            # Append the slice of data from index i*7 + 1 to i*7 + 7
                            new_direction_values_matrix.append(data[i * 7 + 1:i * 7 + 7])
                            new_direction_values_matrix[i] = [calculator.byte_to_float(value) for value in new_direction_values_matrix[i]]

                        update_direction_values(calculator.direction_values, new_direction_values_matrix)
                        print(calculator.direction_values)
                        write_json_file(direction_values_path, calculator.direction_values)
                        hardware.send_message_code_uart(0x20)

    
    except Exception as e:
        print_verbose(f"[ERROR] {e.__class__.__name__}: {e}")
        state = 2
        hardware.send_message_code_uart(0x00)
    
    
    delta_time = time.ticks_diff(time.ticks_ms(), start_time)
    if delta_time < cycle_time:
        time.sleep_ms(cycle_time - delta_time)
#        print_verbose(cycle_time - delta_time)
    else:
        print_verbose(f"Warning: Cycle Time exceeded! - delay {-cycle_time + delta_time}ms")
        hardware.send_message_code_uart(0x03)
    
    
    
