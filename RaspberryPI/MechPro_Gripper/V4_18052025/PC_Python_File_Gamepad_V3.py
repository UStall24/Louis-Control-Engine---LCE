

###################################################################
#---File-Informationen--------------------------------------------#
###################################################################
# File Name: PC_Python_File_Gamepad.py
# Projekt: Mechatronisches Projekt
# Gruppe: Johann Spielvogel, Tim Richer, Jennifer Gastgeb, Pascal Roskamp
# Semester: 6
# Hochschule Esslingen


#####################################################
#---Allgemeines-------------------------------------#
#####################################################
#----------------------------------------------Aenderungsverzeichnis-------------------------------------------------------------
#                          Aenderung                                                  //   Datum          //      Name
# Erstellung des Skripts                                                              // 21.04.2025       // Johann Spielvogel
# Konfiguration und Einrichtung der MQTT Kommunikation                                // 21.04.2025       // Johann Spielvogel
# Erweiterung um Gamepad Initialisierung und Steuerung                                // 22.04.2025       // Johann Spielvogel
# Pygame Events einrichten fuer Bewegungssteuerung                                    // 24.04.2025       // Johann Spielvogel
# Anpassung auf Gamepad ohne Hat-Unterstuetzung (SNES)                                // 10.05.2025       // Johann Spielvogel
# Optimierung der Greifersteuerung                                                    // 10.05.2025       // Johann Spielvogel
# Anpassung der Namensbezeichnung                                                     // 11.05.2025       // Johann Spielvogel
# 
#
#
#
#
#


#####################################################
#---Belegung Gamepad-Controller---------------------#
#####################################################
#Taste am Controller	Pygame Event	        Index
#A	                JOYBUTTONDOWN/UP	1
#B	                JOYBUTTONDOWN/UP	2
#X	                JOYBUTTONDOWN/UP	0
#Y	                JOYBUTTONDOWN/UP	3
#Select	                JOYBUTTONDOWN/UP	8
#Start	                JOYBUTTONDOWN/UP	9


#####################################################
#---Import------------------------------------------#
#####################################################
import paho.mqtt.client as mqtt
import pygame
import time


#####################################################
#---MQTT--------------------------------------------#
#####################################################
MQTT_BROKER = "192.168.0.3"  # IP Raspberry Pi
MQTT_PORT = 1883
MQTT_TOPIC = "gamepad/input"


#####################################################
#---Deklaration-------------------------------------#
#####################################################
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Kein Gamepad erkannt!")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

print("Benutze das Steuerkreuz:")
print("Nach rechts: Einfahren")
print("Nach links: Ausfahren")
print("Nach oben: Hoch")
print("Nach unten: Runter")
print("Taste B: pH-Messung durchfuehren")
print("Taste Select: Pumpe einschalten")
print("Taste Start: Grundstellungsfahrt durchfuehren")
print("Beende mit ESC oder Fenster schließen.")


######################################################################
#---MAIN-------------------------------------------------------------#
######################################################################
deadzone = 0.5  # Zum Herausfiltern kleiner Bewegungen
running = True

last_select_state = False  # Anfangszustand von SELECT-Taste
last_start_state = False   # Für Start (Button 9)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0: # Taste X
                message = "Reserve_Gamepad"
            elif event.button == 1: # Taste A
                message = "Reserve_Gamepad"
            elif event.button == 2: # Taste B
                message = "pH_Messung_Gamepad"
            elif event.button == 3: # Taste Y
                message = "Reserve_Gamepad"
            else:
                message = None

            if message:
                client.publish(MQTT_TOPIC, message)
                print(f"Gesendet: {message}")

    # Abfrage des Steuerkreuzes ueber Achsen
    axis_x = joystick.get_axis(0)
    axis_y = joystick.get_axis(1)

    if axis_x < -deadzone:
        message = "afg"
        client.publish(MQTT_TOPIC, message)
        print(f"Gesendet: {message}")
    elif axis_x > deadzone:
        message = "efg"
        client.publish(MQTT_TOPIC, message)
        print(f"Gesendet: {message}")

    if axis_y < -deadzone:
        message = "hg"
        client.publish(MQTT_TOPIC, message)
        print(f"Gesendet: {message}")
    elif axis_y > deadzone:
        message = "rg"
        client.publish(MQTT_TOPIC, message)
        print(f"Gesendet: {message}")

    # Zustand der SELECT-Taste (Button 8)
    current_select_state = joystick.get_button(8)

    if current_select_state and not last_select_state:
        message = "P_ein_G"
        client.publish(MQTT_TOPIC, message)
        print(f"Gesendet: {message}")
    elif not current_select_state and last_select_state:
        message = "P_aus_G"
        client.publish(MQTT_TOPIC, message)
        print(f"Gesendet: {message}")

    last_select_state = current_select_state

    # START-Taste (Button 9)
    current_start_state = joystick.get_button(9)

    if current_start_state and not last_start_state:
        message = "GSF_G"
        client.publish(MQTT_TOPIC, message)
        print(f"Gesendet: {message}")

    last_start_state = current_start_state


    time.sleep(0.1)


client.disconnect()
pygame.quit()
print("Programm beendet.")


#----------------------------------------FILE ENDE--------------------------------------------

