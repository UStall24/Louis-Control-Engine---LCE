###################################################################
#---File-Informationen--------------------------------------------#
###################################################################
# File Name: mqttuart_pi5.py
# Project: MateROV U.Stall Esslingen
# Current Developper: Iheb Elleuch


#############################################################
#---General Information-------------------------------------#
#############################################################

# Run this script using this command: python mqttuart_pi5.py
# This script requires a 'CommunicationConfig.json' file

#------------------------------Version Control----------------------------------
#                          Changes                      Date        Developer
#   Added Extensive Documentation
#   Added Code and System Monitoring via MQTT
#   Removed Argument Requirement                        21.04.2024  Iheb Elleuch
#   Hardcoded Broker/Port to local mosquitto broker     23.04.2024  Iheb Elleuch
#   Changed format_motor_data to send                   
#   motor/grappler together                             02.05.2024  Iheb Elleuch
#   Added reset_stm function / modified on_message      
#   To accomondate the reset_stm function (new topic)   07.05.2024  Iheb Elleuch



#---Required Libraries-------------------------------------#
import json
import time
import serial
import paho.mqtt.client as mqtt
import signal
import sys
import atexit #Required for the cleanup function
import subprocess #Required for executing Bash commands
import psutil #Required for reading CPU Usage
from gpiozero import LED

#---Functions-------------------------------------#
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe([(config['MotorSollwerteTopic'], 1), (config['GreiferSollwerteTopic'], 1), (config['AllgemeineBefehleTopic'], 1)])  # Subscribe to both topics with QoS 1
    
def scale_and_convert_to_hex(value):
    # Scale the value from the range [-1, 1] to [0, 255]
    scaled_value = int((value + 1) * 127.5)
    # Convert the scaled value to HEX format
    hex_value = hex(scaled_value)[2:].upper().zfill(2)
    return hex_value

def format_motor_data(data):
    try:
        parsed_data = json.loads(data.decode('utf-8').strip())
    except json.JSONDecodeError as e:
        client.publish(config['SCUStatusTopic'], 'ERROR JSON DECODE', qos = 1)
        return []  # Return an empty list or handle the error as appropriate
    hex_values = []
    for key, value in parsed_data.items():
        if isinstance(value, float):
            # Scale and convert float values to HEX
            hex_value = scale_and_convert_to_hex(value)
            hex_values.append(hex_value)
    return hex_values

def reset_stm(gpio_pin):
    print(gpio_pin)
    # Set up the GPIO pin as an output
    try:
        led = LED(gpio_pin)
        led.on()
        client.publish(config['SCUStatusTopic'], 'RESET STM DONE', qos = 1)
        time.sleep(1)
        led.off()
        
    except:
        client.publish(config['SCUStatusTopic'], 'ERROR BAD GPIO', qos = 1)
        

    
    
# Gets Executed Everytime when a message from the subscribed topics arrives
last_grappler_values = [0x15] + [0x7F] + [0x7F] + [0x7F] + [0x7F] + [0x7F] + [0x00]
def on_message(client, userdata, msg):
    global last_grappler_values
    if msg.topic == config['MotorSollwerteTopic']:
        motor_values = format_motor_data(msg.payload)
        formatted_data = bytearray([0x11] + [int(value, 16) for value in motor_values] + last_grappler_values)
        send_via_uart(formatted_data)
    elif msg.topic == config['GreiferSollwerteTopic']:
        motor_values = format_motor_data(msg.payload)
        last_grappler_values = [0x15] + [int(value, 16) for value in motor_values]
    elif msg.topic == config['AllgemeineBefehleTopic']:
        payload = msg.payload.decode('utf-8').strip()
        if payload.startswith('RESET STM'):
            try:
                gpio_pin = int(payload.split()[-1]) 
                reset_stm(gpio_pin) 
            except ValueError:
                client.publish(config['SCUStatusTopic'], 'ERROR GENERAL ORDER', qos = 1)
                
                
            
    

# Function to send data via UART
def send_via_uart(data):
    print(data)
    try:
        ser.write(data)
    except:
        client.publish(config['SCUStatusTopic'], 'ERROR UART COMMUNICATION', qos = 1)

# Funciton to get Metrics Information form RPI
def pi_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_temp_output = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
    cpu_temp = float(cpu_temp_output.split('=')[1].split("'")[0])
    
    metrics = {
        "CPU_USAGE": cpu_usage,
        "CPU_TEMPERATURE": cpu_temp
    }
    
    json_payload = json.dumps(metrics)
    return json_payload

# Function to cleanup the code
def cleanup():
    if client != None:
        client.publish(config['SCUStatusTopic'], 'OFFLINE', qos = 1)

    print("Cleaning up...")
    client.disconnect()
    send_via_uart(bytearray([0x11] + [0x7F] + [0x7F]+ [0x7F] + [0x7F]+ [0x7F] + [0x7F] + [0x15] + [0x7F] + [0x7F]+ [0x7F] + [0x7F]+ [0x7F] + [0x7F]))
    try:
        ser.close()
    except:
        print("No Serial Port")
    sys.exit(0)


# Function to terminate the process when done by bash
def signal_handler(sig, frame):
    print("Termination signal received. Cleaning up and exiting...")
    cleanup()



#---Main Code: Runs once and then keeps the code running via a loop-------------------------------------#

# Load configuration from JSON file
try:
    with open('CommunicationConfig.json', 'r', encoding='utf-8-sig') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    print("Error: Configuration file 'CommunicationConfig.json' not found.")
    sys.exit(1)

# Register the signal handler for SIGTERM (termination signal)
signal.signal(signal.SIGTERM, signal_handler)
#Assigning the method executed when terminating this file
atexit.register(cleanup)

# Initialize MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost', 1883, 60)

# Start the MQTT client loop
client.loop_start()

client.publish(config['SCUStatusTopic'], 'ONLINE', qos = 1)


# Initialize UART
try:
    ser = serial.Serial(
    port='/dev/ttyAMA0',  
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
    )
except:
    client.publish(config['SCUStatusTopic'], 'ERROR UART CONNECT', qos = 1)


# Main loop
try:
    while True:
        time.sleep(1)  # Keep the script running
        client.publish(config['SCUStatusTopic'], 'HEARTBEAT', qos = 1)
        client.publish(config['SCUMetricsTopic'], pi_metrics(), qos = 1)

except KeyboardInterrupt:
    print("\nKeyboard Interrupt")
