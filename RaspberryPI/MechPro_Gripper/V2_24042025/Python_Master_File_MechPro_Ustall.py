

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

#----------------------------------------------Aenderungsverzeichnis-------------------------------------------------------------
#                          Aenderung                                                  //   Datum          //      Name
# Erstellung des Skripts                                                              // 05.04.2025       // Johann Spielvogel
# Erweiterung um Servo_2 und Servo_3                                                  // 10.04.2025       // Johann Spielvogel
# Flask und MQTT Anpassung                                                            // 11.04.2025       // Johann Spielvogel
# Programmstruktur ueberarbeiten                                                      // 12.04.2025       // Johann Spielvogel
# Ueberarbeitung der Kommunikation ueber http.server                                  // 12.04.2025       // Johann Spielvogel
# Aktualisierung socket.server                                                        // 12.04.2025       // Johann Spielvogel
# Anpassung der MQTT Nachrichten                                                      // 13.04.2025       // Johann Spielvogel
# Einbinden der Funktion um den pH-Wert zu Messen                                     // 13.04.2025       // Johann Spielvogel
# Erweiterung der Funktion um den pH-Wert zu Messen                                   // 14.04.2025       // Johann Spielvogel
# Integration Steruerung ueber Gamepad                                                // 19.04.2025       // Johann Spielvogel
# Erweiterung Steuerung ueber Gamepad                                                 // 21.04.2025       // Johann Spielvogel
# Integration einer Grundstellungsfahrt                                               // 24.04.2025       // Johann Spielvogel
# Kommunikation ueber Gamepad erweitert                                               // 24.04.2025       // Johann Spielvogel
#
#
#
#
#
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

#---MQTT; Servosteuerung und Ultraschallsensor
import paho.mqtt.client as mqtt

#---HTTP Server
import http.server
import socketserver


#####################################################
#---pH-Wert Sensor; MCP3008; SPI-Bus----------------#
#####################################################
import gpiozero
# ---MCP3008 Setup (hier Kanal 0 fuer pH-Sensor)
pH_sensor = gpiozero.MCP3008(channel=0)


#####################################################
#---UART Deklaration--------------------------------#
#####################################################
import serial
# UART-Verbindung einrichten (ttyAMA0 fuer UART0 auf dem Pi)
uart = serial.Serial(
    port='/dev/ttyAMA0',
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

        UPLOAD_FOLDER = '/home/julia'
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
        
        app.run(host='192.168.0.3', port=5000)


#####################################################
#---MQTT--------------------------------------------#
#####################################################
def on_message(client, userdata, message):
    direction = message.payload.decode("utf-8")
    #Servo_1------------------------------------------------------------------------------------------------
    if direction == 'ServoLinksDrehen_1':
        print("ServoLinksDrehen_1 AKTIV")
        uart.write(b'ServoLinksDrehen_1\n')
        client.publish("Ustall/Status", "Servo_1: links drehend")

    elif direction == 'ServoRechtsDrehen_1':
        print("ServoRechtsDrehen_1 AKTIV")
        uart.write(b'ServoRechtsDrehen_1\n')
        client.publish("Ustall/Status", "Servo_1: rechts drehend")

    elif direction == 'ServoStopp_1':
        print("ServoStopp_1 AKTIV")
        uart.write(b'ServoStopp_1\n')
        client.publish("Ustall/Status", "Servo_1: stopp")

    #Servo_2------------------------------------------------------------------------------------------------
    if direction == 'ServoLinksDrehen_2':
        print("ServoLinksDrehen_2 AKTIV")
        uart.write(b'ServoLinksDrehen_2\n')
        client.publish("Ustall/Status", "Servo_2: links drehend")

    elif direction == 'ServoRechtsDrehen_2':
        print("ServoRechtsDrehen_2 AKTIV")
        uart.write(b'ServoRechtsDrehen_2\n')
        client.publish("Ustall/Status", "Servo_2: rechts drehend")

    elif direction == 'ServoStopp_2':
        print("ServoStopp_2 AKTIV")
        uart.write(b'ServoStopp_2\n')
        client.publish("Ustall/Status", "Servo_2: stopp")

    #Servo_3------------------------------------------------------------------------------------------------
    if direction == 'ServoLinksDrehen_3':
        print("ServoLinksDrehen_3 AKTIV")
        uart.write(b'ServoLinksDrehen_3\n')
        client.publish("Ustall/Status", "Servo_3: links drehend")

    elif direction == 'ServoRechtsDrehen_3':
        print("ServoRechtsDrehen_3 AKTIV")
        uart.write(b'ServoRechtsDrehen_3\n')
        client.publish("Ustall/Status", "Servo_3: rechts drehend")

    elif direction == 'ServoStopp_3':
        print("ServoStopp_3 AKTIV")
        uart.write(b'ServoStopp_3\n')
        client.publish("Ustall/Status", "Servo_3: stopp")

    #Pumpe------------------------------------------------------------------------------------------------
    if direction == 'Pumpe_einschalten' or direction == 'Pumpe_einschalten_Gamepad':
        print("Pumpe_einschalten AKTIV")
        uart.write(b'Pumpe_einschalten\n')
        client.publish("Ustall/Status", "Pumpe eingeschaltet")

    elif direction == 'Pumpe_ausschalten':
        print("Pumpe_ausschalten AKTIV")
        uart.write(b'Pumpe_ausschalten\n')
        client.publish("Ustall/Status", "Pumpe ausgeschaltet")

    #pH-Wert Sensor---------------------------------------------------------------------------------------
    if direction == 'Start_pH_Messung' or direction == 'pH_Messung_Gamepad':
        print("pH_Messung AKTIV")
        #rohwert = pH_sensor.value  # zwischen 0.0 und 1.0
        rohwert= 0.0177
        spannung = rohwert * 3.3   # angenommen: 3.3V Referenzspannung
        pH_wert = 16.9 * spannung + 7.0 #Steigung m = ΔpH / ΔU = (14 - 7) / (0.41412 - 0) ≈ 16.9  -> Offset b = 7.0 (bei 0V)
        print(f"pH-Wert gesendet: {pH_wert:.2f}")

        client.publish("Ustall/Status", "pH-Messung durchgeführt")
        client.publish("Ustall/pH_Wert", f"{pH_wert:.2f}")  # fuer WebInterface
    elif direction == 'Stopp_pH_Messung':
        print("pH_Messung beendet")

    #Grundtellungsfahrt-----------------------------------------------------------------------------------
    if direction == 'Grundstellungsfahrt' or direction == 'Grundstellungsfahrt_Gamepad':
        print("Grundstellungsfahrt")
        uart.write(b'Grundstellungsfahrt\n')
        client.publish("Ustall/Status", "Grundstellungsfahrt")

    #Gamepad-Controller Steuerkreuz-----------------------------------------------------------------------
    # ausfahren -> Taste "nach rechts"
    elif direction == 'ausfahren_Gamepad':  
        print("ausfahren (via Gamepad) AKTIV")
        uart.write(b'ausfahren\n')
        client.publish("Ustall/Status", "ausfahren (via Gamepad)")
    
    # einfahren -> Taste "nach links"
    elif direction == 'einfahren_Gamepad':  
        print("einfahren (via Gamepad) AKTIV")
        uart.write(b'einfahren\n')
        client.publish("Ustall/Status", "einfahren (via Gamepad)")
    
    # hoch -> Taste "nach oben"
    elif direction == 'hoch_Gamepad':  
        print("hoch (via Gamepad) AKTIV")
        uart.write(b'hoch\n')
        client.publish("Ustall/Status", "hoch (via Gamepad)")
    
    # runter -> Taste "nach unten"
    elif direction == 'runter_Gamepad':  
        print("runter (via Gamepad) AKTIV")
        uart.write(b'runter\n')
        client.publish("Ustall/Status", "runter (via Gamepad)")
    


# MQTT client setup
client = mqtt.Client()
client.on_message = on_message
client.connect("192.168.0.3", 1883)
client.subscribe("Ustall/MechPro")
client.subscribe("gamepad/input")
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
    #update_ip_in_html("templates/WebInterface_MechPro_Ustall.html")
    #update_ip_in_html("Python_Master_File_MechPro_Ustall.py")
    Handler = http.server.SimpleHTTPRequestHandler

    http_server_thread = threading.Thread(target=run_http_server)
    http_server_thread.daemon = True
    http_server_thread.start()

    background_thread_1 = Server_Background_Thread()
    background_thread_1.start()


#----------------------------------------FILE ENDE--------------------------------------------
