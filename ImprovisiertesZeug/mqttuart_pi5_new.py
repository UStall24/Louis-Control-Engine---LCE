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
#   modified on_message funciton to old system          11.05.2024  Iheb Elleuch
#   corrected bug                                       16.05.2024  Iheb Elleuch
#   Offset Fuctionality                                 04.06.2024  Iheb Elleuch  GUI V1.0.3



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
import threading

#---Functions-------------------------------------#
def scale_and_convert_to_hex(value):
    scaled_value = int((value + 1) * 127.5)
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


def handle_motor(msg):
    motor_values = format_motor_data(msg.payload)
    formatted_data = bytearray([0x11] + [int(value, 16) for value in motor_values])
    send_via_uart(formatted_data)

greiferdata_old = bytearray([0x15] + [0x00] + [0x00] + [0x00] + [0x00] + [0x00] + [0x00])
def handle_grappler(msg):
    global greiferdata_old
    motor_values = format_motor_data(msg.payload)
    greiferdata = bytearray([0x15] + [int(value, 16) for value in motor_values] + [0x7F])
    if greiferdata_old != greiferdata:
        send_via_uart(greiferdata)
    greiferdata_old = greiferdata
    #if greiferdata != None:
    #    print(bytes_to_hex_string(greiferdata))

def handle_order(msg):
    payload = msg.payload.decode('utf-8').strip()
    if payload.startswith('RESET STM'):
        try:
            gpio_pin = int(payload.split()[-1]) 
            reset_stm(gpio_pin) 
        except ValueError:
            client.publish(config['topic_rpi_status'], 'ERROR GENERAL ORDER', qos = 1)
    if payload.startswith('SET OFFSETS AND GO'):
        data = [0x55] + [offset['m1']] + [offset['m2']]+ [offset['m3']]+ [offset['m4']]+ [offset['m5']]+ [offset['m6']] 
        send_via_uart(bytearray(data))

state = 1
def reset_stm(gpio_pin):
    global state
    # Set up the GPIO pin as an output
    try:
        
        if state == 1:
            led.off()
            state = 0
            
        elif state == 0:
            led.on()
            state = 1
        
        client.publish(config['topic_rpi_status'], 'RESET STM DONE', qos = 1)
        time.sleep(1)
        #print("Success")
        
    except:
        #print("Bad GPIO")
        client.publish(config['topic_rpi_status'], 'ERROR BAD GPIO', qos = 1)
        

def handle_sensor_data(data):    
    try:
        data_list = list(data)
        if not data_list:
            raise ValueError("Received empty data list")

        match data_list[0]:
            case 0x12:
                if len(data_list) >= 3:
                    temperature = ((data_list[1] - 40) * 0.5)
                    druck = ((data_list[2]) / 255 * 2) + 1.013
                    data = {
                        "temperature": temperature,
                        "druck": druck
                    }
                    client.publish(config['topic_scu_temperatur_druck'], json.dumps(data), qos=1)
                else:
                    raise ValueError("Incomplete temperature and pressure data")
            case 0x13:
                if len(data_list) >= 7:
                    current_values = [data_list[i] / 255 * 10 for i in range(1, 7)]
                    data = {f"m{i+1}": current_values[i] for i in range(6)}
                    client.publish(config['topic_scu_strom'], json.dumps(data), qos=1)
                else:
                    raise ValueError("Incomplete current sensor data")
            case 0x14:
                if len(data_list) >= 7:
                    fuse_values = [1 if data_list[i] == 255 else 0 for i in range(1, 7)]
                    data = {f"m{i+1}": fuse_values[i] for i in range(6)}
                    client.publish(config['topic_scu_sicherung'], json.dumps(data), qos=1)
                else:
                    raise ValueError("Incomplete fuse data")
            case 0x16:
                if len(data_list) >= 5:
                    gyroXe = (data_list[2] - 128) * 0.02
                    gyroYe = (data_list[3] - 128) * 0.02
                    gyroZe = (data_list[4] - 128) * 0.02
                    gyroXb = (data_list[2] - 128) * 0.02
                    gyroYb = (data_list[3] - 128) * 0.02
                    gyroZb = (data_list[4] - 128) * 0.02
                    gyro_data = {
                        "xe": gyroXe,
                        "ye": gyroYe,
                        "ze": gyroZe,
                        "xb": gyroXb,
                        "yb": gyroYb,
                        "zb": gyroZb
                    }
                    client.publish(config['topic_scu_gyro'], json.dumps(gyro_data), qos=1)
                else:
                    raise ValueError("Incomplete gyroscope data")
            case _:
                raise ValueError("Unknown sensor type")
    except Exception as e:
        client.publish(config['topic_rpi_status'], f'ERROR UART BAD INPUT: {str(e)}', qos=1)




    
#---UART SEND RECIEVE--------------------------------------------------------------------------------#
def send_via_uart(data):
    try:
        if data != None:
            print(bytes_to_hex_string(data))
            ser.write(data)
    except:
        client.publish(config['topic_rpi_status'], 'ERROR UART COMMUNICATION', qos = 1)


def receive_via_uart():
    try:
        while ser.in_waiting:
            data = ser.read(7)
            if (data != None):
                handle_sensor_data(data)
    except Exception as e:
        client.publish(config['topic_rpi_status'], f'ERROR UART: {str(e)}', qos=1)
        

def bytes_to_hex_string(byte_array):
    print(''.join(['\\x{:02X}'.format(b) for b in byte_array]))

#---MQTT Stuff-----------------------------------------------------------------------------------------#
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe([(config['topic_motor_sollwerte'], 1), (config['topic_grappler_sollwerte'], 1), (config['topic_befehle'], 1)])  # Subscribe to topics with QoS 1

def on_message(client, userdata, msg):
    if msg.topic == config['topic_motor_sollwerte']:
        handle_motor(msg)
    elif msg.topic == config['topic_grappler_sollwerte']:
        handle_grappler(msg)
    elif msg.topic == config['topic_befehle']:
        handle_order(msg)
#---Status, startup and shutdown code------------------------------------------------------------------#
def publish_heartbeat_and_stats():
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_temp_output = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
    cpu_temp = float(cpu_temp_output.split('=')[1].split("'")[0])
    
    client.publish(config['topic_rpi_status']       , 'HEARTBEAT'   , qos=1)
    client.publish(config['topic_rpi_temperatur']   , str(cpu_temp) , qos=1)
    client.publish(config['topic_rpi_usage']        , str(cpu_usage), qos=1)
    
# Function to terminate the process when done by bash
def signal_handler(sig, frame):
    print("Termination signal received. Cleaning up and exiting...")
    cleanup()
    
# Function to cleanup the code
def cleanup():
    if client != None:
        client.publish(config['topic_rpi_status'], 'OFFLINE', qos = 1)

    print("Cleaning up...")
    client.disconnect()
    try:
        ser.close()
    except:
        print("No Serial Port")
    sys.exit(0)

    
#---Main Code: Runs once and then keeps the code running via a loop-------------------------------------#

# Load configuration from JSON file
try:
    with open('CommunicationConfigNew.json', 'r', encoding='utf-8-sig') as config_file:
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
client.username_pw_set(config['mqtt_username'], config['mqtt_password'])
client.connect('localhost', config['mqtt_port'], 60)

# Start the MQTT client loop
client.loop_start()

client.publish(config['topic_rpi_status'], 'ONLINE', qos = 1)

try:
    with open('offsets.json', 'r', encoding='utf-8-sig') as offset_file:
        offset = json.load(offset_file)
except FileNotFoundError:
    print("Error: offset file 'offsets.json' not found.")
    sys.exit(1)
    

# Initialize UART
try:
    ser = serial.Serial(
    port='/dev/ttyAMA0',  
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS,
    timeout=1
    )
except:
    client.publish(config['topic_rpi_status'], 'ERROR UART CONNECT', qos = 1)

led = LED(21)
led.on() 
# Main loop
startTimeHeartbeat = time.time()
startTimeUART_TX = time.time()
while True:
    receive_via_uart()
    if time.time() - startTimeHeartbeat > 1:
        publish_heartbeat_and_stats()
        startTimeHeartbeat = time.time()
    if time.time() - startTimeUART_TX > 0.5:
        startTimeUART_TX = time.time()
       # receive_via_uart()

