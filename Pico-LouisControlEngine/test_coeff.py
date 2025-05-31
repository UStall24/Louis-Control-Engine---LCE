from libs.calculator import *
from libs.configLoader import *
import time
import sys

print("Starting initialization")
machine.freq(200000000)
direction_values_path = "directionValues.json"
dynamic_throttle_path = "dynamic_throttle_data.json"
direction_values_data = read_json_file(direction_values_path)
dynamic_throttle_data = read_json_file(dynamic_throttle_path)

calculator = Calculator(direction_values_data, dynamic_throttle_data)

start = 0
counter = start
max_time_ms = 0  # Track maximum execution time
current_warnings = []  # Track current warnings

try:
    while True:
        throttle_values = [round(v, 2) for v in [counter, counter*2, -counter, 1 - counter, -1 + counter, 0.5]]
        start_ns = time.time_ns()
        pwm_values, force_values, current_values = calculator.dynamic_throttle_2_pwm(throttle_values)
        end_ns = time.time_ns()

        execution_time_ms = (end_ns - start_ns) / 1e6
        if execution_time_ms > max_time_ms:
            max_time_ms = execution_time_ms

        total_current = sum(current_values)
        
        # Check for current out of bounds
        if total_current < -1 or total_current > 20:
            warning_msg = f"WARNING: Current out of bounds! Value: {total_current:.2f}A at throttle values: {throttle_values}"
            current_warnings.append(warning_msg)
            print("\n!WARNING! ", warning_msg)

        print("\n" * 20)
        print("Throttle values:", [f"{v:.2f}" for v in throttle_values])
        print("PWM values:", pwm_values)
        print("Force values:", [f"{v:.2f}" for v in force_values])
        print("Current values:", [f"{v:.2f}" for v in current_values])
        print(f"Total current: {total_current:.2f}")
        print(f"Time required in ms: {execution_time_ms:.2f}")
        print(f"Max time observed: {max_time_ms:.2f} ms")
        
        time.sleep(0.4)
        counter += 0.02
        if counter > 1:
            counter = start

except KeyboardInterrupt:
    print("\n\n--- Program Interrupted ---")
    print(f"Maximum execution time observed: {max_time_ms:.2f} ms")
    
    # Print all current warnings if any occurred
    if current_warnings:
        print("\nCurrent Bound Warnings:")
        for warning in current_warnings:
            print(warning)
    else:
        print("No current bound violations detected")
    
    sys.exit(0)