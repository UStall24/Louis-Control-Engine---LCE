

###################################################################
#---File-Informationen--------------------------------------------#
###################################################################
# File Name: Python_Master_File_MechPro_Ustall.py
# Projekt: Mechatronisches Projekt
# Gruppe: Johann Spielvogel, Tim Richer, Jennifer Gastgeb, Pascal Roskamp
# Semester: 6
# Hochschule Esslingen


#####################################################
#---Allgemeines-------------------------------------#
#####################################################

#----------------------------------------------Änderungsverzeichnis-------------------------------------------------------------
#                          Änderung                                                   //   Datum          //      Name
# Erstellung des Skripts                                                              // 05.04.2025       // Johann Spielvogel
#
#
#


#########################################################################
#---Import--------------------------------------------------------------#
#########################################################################
from flask import Flask, request, render_template, jsonify, redirect
import os
import subprocess
import threading
import socket
import re

#---MQTT; Motorsteuerung und Ultraschallsensor
import paho.mqtt.client as mqtt

#---HTTP Server
import http.server
import socketserver

#####################################################
#---UART Deklaration--------------------------------#
#####################################################
import serial
# UART-Verbindung einrichten (ttyAMA0 für UART0 auf dem Pi)
uart = serial.Serial(
    port='/dev/ttyAMA0',  # Nutze /dev/serial0 wenn du flexibel bleiben willst
    baudrate=9600,
    timeout=1
)

import atexit


# UART schließen beim Beenden
@atexit.register
def cleanup_uart():
    if uart and uart.is_open:
        uart.close()

#####################################################
#---Deklaration-------------------------------------#
#####################################################
PORT = 8080 #HTTP Port



#####################################################
#---IP-Adresse abrufen------------------------------#
#####################################################

def get_current_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


#####################################################
#---Flask-------------------------------------------#
#####################################################
running_process = None

class Server_Background_Thread(threading.Thread):
    def run(self):
        app = Flask(__name__)

        UPLOAD_FOLDER = '/home/USTALL'
        ALLOWED_EXTENSIONS = {'py'}

        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        running_process = None

        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        def execute_script(filepath):
            global running_process
            running_process = subprocess.Popen(['python', filepath])
            running_process.wait()

        @app.route('/')
        def index():
            return render_template('WebInterface_MechPro_Ustall.html')
        
        app.run(host='0.0.0.0', port=5000)


#####################################################
#---MQTT--------------------------------------------#
#####################################################

def on_message(client, userdata, message):
    direction = message.payload.decode("utf-8")
    if direction == 'MotorLinksDrehen':
        print("MotorLinksDrehen AKTIV")
        uart.write(b'MotorLinksDrehen\n')

    elif direction == 'MotorRechtsDrehen':
        print("MotorRechtsDrehen AKTIV")
        uart.write(b'MotorRechtsDrehen\n')

    elif direction == 'MotorStopp':
        print("MotorStopp AKTIV")
        uart.write(b'MotorStopp\n')






# MQTT client setup
client = mqtt.Client()
client.on_message = on_message
client.connect("test.mosquitto.org", 1883)
client.subscribe("Ustall/MechPro")
client.loop_start()




#########################################################################################
#---Funktion zur IP-Aktualisierung------------------------------------------------------#
#########################################################################################
def update_ip_in_html(file_path):
    """Aktualisiere die IP-Adressen in der HTML-Datei auf die aktuelle IP-Adresse."""

    current_ip = get_current_ip()
    print(f'Aktuelle IP-Adresse: {current_ip}')

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    old_ip_pattern = re.compile(r'http://192\.168\.\d+\.\d+:8080')
    updated_content = re.sub(old_ip_pattern, f'http://{current_ip}:8080', content)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

    print('IP-Adressen erfolgreich aktualisiert.')

def run_http_server():
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"HTTP-Server läuft auf Port {PORT}")
        httpd.serve_forever()


######################################################################
#---MAIN-------------------------------------------------------------#
######################################################################
if __name__ == '__main__':
    update_ip_in_html("templates/WebInterface_MechPro_Ustall.html")
    update_ip_in_html("Python_Master_File_MechPro_Ustall.py")
    Handler = http.server.SimpleHTTPRequestHandler

    http_server_thread = threading.Thread(target=run_http_server)
    http_server_thread.daemon = True
    http_server_thread.start()

    background_thread_1 = Server_Background_Thread()
    background_thread_1.start()


#----------------------------------------FILE ENDE--------------------------------------------