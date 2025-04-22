

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

#----------------------------------------------Änderungsverzeichnis-------------------------------------------------------------
#                          Änderung                                                   //   Datum          //      Name
# Erstellung des Skripts                                                              // 21.04.2025       // Johann Spielvogel
# Konfiguration und Einrichtung der MQTT Kommunikation                                // 21.04.2025       // Johann Spielvogel
# Erweiterung um Gamepad Initialisierung und Steuerung                                // 22.04.2025       // Johann Spielvogel
#
#
#
#
#
#
#
#
#
#
#
#
#


#####################################################
#---Import------------------------------------------#
#####################################################

import paho.mqtt.client as mqtt
import pygame
import time


#####################################################
#---MQTT--------------------------------------------#
#####################################################
# MQTT-Einstellungen
MQTT_BROKER = "192.168.0.3"  # IP deines Raspberry Pi
MQTT_PORT = 1883
MQTT_TOPIC = "gamepad/input"


#####################################################
#---Deklaration-------------------------------------#
#####################################################
# Pygame-Setup für Gamepad
pygame.init()
pygame.joystick.init()

# Stelle sicher, dass das Gamepad erkannt wurde
if pygame.joystick.get_count() == 0:
    print("Kein Gamepad erkannt!")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()


#####################################################
#---MQTT--------------------------------------------#
#####################################################
# MQTT-Client
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

print("Drücke 'X' für Servo nach rechts, 'Y' für Servo nach links. Loslassen stoppt den Servo. Beende mit ESC oder Fenster schließen.")


######################################################################
#---MAIN-------------------------------------------------------------#
######################################################################
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            # Wenn eine Taste gedrückt oder losgelassen wird
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:  # "X"-Taste gedrückt (nach rechts drehen)
                    message = "Servo1_rechts_drehen"
                    client.publish(MQTT_TOPIC, message)
                    print(f"Gesendet: {message}")

                elif event.key == pygame.K_y:  # "Y"-Taste gedrückt (nach links drehen)
                    message = "Servo1_links_drehen"
                    client.publish(MQTT_TOPIC, message)
                    print(f"Gesendet: {message}")

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_x or event.key == pygame.K_y:  # Wenn "X" oder "Y" losgelassen wird
                    message = "ServoStopp_1"
                    client.publish(MQTT_TOPIC, message)
                    print(f"Gesendet: {message} (Stopp)")

            # Wenn ESC gedrückt wird
            elif event.type == pygame.K_ESCAPE:
                running = False

    time.sleep(0.1)

client.disconnect()
pygame.quit()
print("Programm beendet.")


#----------------------------------------FILE ENDE--------------------------------------------
