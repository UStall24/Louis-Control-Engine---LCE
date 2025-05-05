from machine import Pin, PWM
import time
import math
import _thread

# Define PWM pin (e.g., GP0 for LED)
leds = [PWM(Pin(0)), PWM(Pin(2)), PWM(Pin(4))]

# Set PWM frequency
for led in leds:
    led.freq(50)

def map_value(x, in_min, in_max, out_min, out_max):
    """Maps value from one range to another."""
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def sigmoid(x, k=0.1, x_0=25):
    """Sigmoid function for smooth brightness transition."""
    exp_weight = - k * (x - x_0) / 50
    print(exp_weight)
    return 1 / (1 +  math.exp(exp_weight))


def smooth_sigmoid_ramp(current, target, duration=2.0, steps=50):
    """Gradually increase brightness using a sigmoid function."""
    start_time = time.ticks_ms()
    for i in range(steps + 1):
        elapsed = time.ticks_diff(time.ticks_ms(), start_time) / (duration * 1000)
        factor = sigmoid(elapsed * 50, k=10, x_0=25)  # Apply sigmoid curve
        pwm_value = int(current + (target - current) * factor)
        for led in leds:
            led.duty_u16(pwm_value)
        print(f"Step {i}: PWM {pwm_value}")  # Debug output
        time.sleep(duration / steps)
        

duration = 2.0
steps = 50
def sigmoid_ramp():
        



values = [0, 180, 255]
index = 0
current_pwm = int(65535 * 0)  # Start at 10% brightness

while True:
    r2_trigger_value = values[index]
    index = (index + 1) % len(values)  # Cycle through values

    target_pwm = map_value(r2_trigger_value, 0, 255, int(65535 * 0), int(65535 * 1.0))

    _thread.start_new_thread(smooth_sigmoid_ramp, (current_pwm, target_pwm, 1.5, 40))
    current_pwm = target_pwm  # Update the current PWM value

    time.sleep(0.5)  # Hold before switching
