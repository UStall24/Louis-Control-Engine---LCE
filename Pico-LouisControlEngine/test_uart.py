from machine import UART, Pin
import time

def print_as_hex(byte_array):
    msg = "Received data (hex): " + " ".join(f"{byte:02X}" for byte in byte_array)
    print(msg)

# Initialize UART on TX=12, RX=13 (using UART1 for these GPIOs)
uart = UART(0, baudrate=115200, tx=Pin(12), rx=Pin(13))

start_time = time.ticks_ms()
last_send = time.ticks_ms()

while True:
    # Check for incoming data
    if uart.any():
        data = uart.read()  # Read available bytes
        if data:
            print_as_hex(data)

    # Send uptime every 0.1s
    if time.ticks_diff(time.ticks_ms(), last_send) >= 100:
        uptime = time.ticks_diff(time.ticks_ms(), start_time) / 1000
        uart.write("Uptime: {:.1f} sec\n".format(uptime))
        last_send = time.ticks_ms()

    time.sleep_ms(1000)
