
#python Python_Master_File_MechPro_Ustall.py
#passwort: s
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
# Optimierung der Greifersteuerung                                                    // 10.05.2025       // Johann Spielvogel
# Anpassung der Namensbezeichnung                                                     // 11.05.2025       // Johann Spielvogel
# Anpassung der Funktion um den pH-Wert zu Messen                                     // 12.05.2025       // Johann Spielvogel
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
    if direction == 'SLD_1':
        print("ServoLinksDrehen_1 AKTIV")
        uart.write(b'SLD_1\n')
        client.publish("Ustall/Status", "Servo_1: links drehend")

    elif direction == 'SRD_1':
        print("ServoRechtsDrehen_1 AKTIV")
        uart.write(b'SRD_1\n')
        client.publish("Ustall/Status", "Servo_1: rechts drehend")

    elif direction == 'S_1_S':
        print("ServoStopp_1 AKTIV")
        uart.write(b'S_1_S\n')
        client.publish("Ustall/Status", "Servo_1: stopp")

    #Servo_2------------------------------------------------------------------------------------------------
    if direction == 'SLD_2':
        print("ServoLinksDrehen_2 AKTIV")
        uart.write(b'SLD_2\n')
        #uart.write(b'ServoLinksDrehen_2\n')
        client.publish("Ustall/Status", "Servo_2: links drehend")

    elif direction == 'SRD_2':
        print("ServoRechtsDrehen_2 AKTIV")
        #uart.write(b'ServoRechtsDrehen_2\n')
        uart.write(b'SRD_2\n')
        client.publish("Ustall/Status", "Servo_2: rechts drehend")

    elif direction == 'S_2_S':
        print("ServoStopp_2 AKTIV")
        uart.write(b'S_2_S\n')
        client.publish("Ustall/Status", "Servo_2: stopp")

    #Servo_3------------------------------------------------------------------------------------------------
    if direction == 'SLD_3':
        print("ServoLinksDrehen_3 AKTIV")
        uart.write(b'SLD_3\n')
        client.publish("Ustall/Status", "Servo_3: links drehend")

    elif direction == 'SRD_3':
        print("ServoRechtsDrehen_3 AKTIV")
        uart.write(b'SRD_3\n')
        client.publish("Ustall/Status", "Servo_3: rechts drehend")

    elif direction == 'S_3_S':
        print("ServoStopp_3 AKTIV")
        uart.write(b'S_3_S\n')
        client.publish("Ustall/Status", "Servo_3: stopp")

    #Pumpe------------------------------------------------------------------------------------------------
    if direction == 'P_ein' or direction == 'P_ein_G':
        print("Pumpe_einschalten AKTIV")
        uart.write(b'P_ein_G\n')
        client.publish("Ustall/Status", "Pumpe eingeschaltet")

    elif direction == 'P_aus' or direction == 'P_aus_G':
        print("Pumpe_ausschalten AKTIV")
        uart.write(b'P_aus_G\n')
        client.publish("Ustall/Status", "Pumpe ausgeschaltet")

    #pH-Wert Sensor---------------------------------------------------------------------------------------
    if direction == 'Start_pH_Messung' or direction == 'pH_Messung_Gamepad':
        print("pH_Messung AKTIV")
        rohwert = pH_sensor.value  # zwischen 0.0 und 1.0
        #spannung = rohwert * 3.3   # Referenzspannung 3.3V
        #pH_wert = -spannung / 0.05916 + 7  # lineare Umrechnung -> pH = -U / (59.16 mV) + 7
        (x1, y1) = (0.54, 4)
        (x2, y2) = (0.69, 7)
        (x3, y3) = (0.81, 10)
        pH_wert = 22.13 * rohwert - 8.05

        # Liste der Kalibrierpunkte: (rohwert, pH-Wert)
        messpunkte = [
            (0.54, 4),
            (0.61, 6.86),
            (0.66, 9.18)
        ]

        # Anzahl der Punkte
        n = len(messpunkte)

        # Summen berechnen
        sum_x = sum(x for x, y in messpunkte)
        sum_y = sum(y for x, y in messpunkte)
        sum_x2 = sum(x**2 for x, y in messpunkte)
        sum_xy = sum(x * y for x, y in messpunkte)

        # Regressionskoeffizienten berechnen
        a = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
        b = (sum_y - a * sum_x) / n

        # pH-Wert berechnen
        pH_wert = a * rohwert + b

        print(f"pH-Wert gesendet: {pH_wert:.2f}")

        print(f"pH-Wert gesendet: {rohwert:.2f}")

        client.publish("Ustall/Status", "pH-Messung durchgeführt")
        client.publish("Ustall/pH_Wert", f"{pH_wert:.2f}")  # fuer WebInterface
    elif direction == 'Stopp_pH_Messung':
        print("pH_Messung beendet")

    #Grundtellungsfahrt-----------------------------------------------------------------------------------
    if direction == 'GSF' or direction == 'GSF_G':
        print("Grundstellungsfahrt")
        uart.write(b'GSF\n')
        client.publish("Ustall/Status", "Grundstellungsfahrt")

    #Gamepad-Controller Steuerkreuz-----------------------------------------------------------------------
    # ausfahren -> Taste "nach rechts"
    elif direction == 'afg':  
        print("ausfahren (via Gamepad) AKTIV")
        uart.write(b'afg\n')
        client.publish("Ustall/Status", "ausfahren (via Gamepad)")
    
    # einfahren -> Taste "nach links"
    elif direction == 'efg':  
        print("einfahren (via Gamepad) AKTIV")
        uart.write(b'efg\n')
        client.publish("Ustall/Status", "einfahren (via Gamepad)")
    
    # hoch -> Taste "nach oben"
    elif direction == 'hg':  
        print("hoch (via Gamepad) AKTIV")
        uart.write(b'hg\n')
        client.publish("Ustall/Status", "hoch (via Gamepad)")
    
    # runter -> Taste "nach unten"
    elif direction == 'rg':  
        print("runter (via Gamepad) AKTIV")
        uart.write(b'rg\n')
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
