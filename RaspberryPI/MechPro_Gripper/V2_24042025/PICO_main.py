

###################################################################
#---File-Informationen--------------------------------------------#
###################################################################
# File Name: Pico_Servosteuerung.py
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
# Anpassung der MQTT Nachrichten                                                      // 13.04.2025       // Johann Spielvogel
# Erweiterung eines Puffers für UART-Nachrichten                                      // 23.04.2025       // Johann Spielvogel
# Speichern der letzten Position ein einzelnen Text-Files                             // 23.04.2025       // Johann Spielvogel
# Kommunikation ueber Gamepad erweitert                                               // 24.04.2025       // Johann Spielvogel
#
#
#
#


#########################################################################
#---Import--------------------------------------------------------------#
#########################################################################
from machine import UART, Pin, PWM
import time


#####################################################
#---UART Deklaration--------------------------------#
#####################################################
# UART0: RX = GP1 (Empfang)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))


#####################################################
#---Servo Konfiguration-----------------------------#
#####################################################
#Servo_1---------------------------------------------
servo_1 = PWM(Pin(2))
servo_1.freq(50)

#Servo_2---------------------------------------------
#servo_2 = PWM(Pin(XXX))
#servo_2.freq(50)

#Servo_3---------------------------------------------
#servo_3 = PWM(Pin(XXX))
#servo_3.freq(50)


#####################################################
#---Servo Funktionen--------------------------------#
#####################################################
#Servo_1---------------------------------------------
# Funktion zum Speichern der Servo-Position in eine Datei
def save_servo_1_position(angle):
    try:
        with open("Servo_1_pos.txt", "w") as f:
            f.write(str(angle))  # Schreibe die Position in die Datei
        print(f"Position {angle} gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern der Position: {e}")
        
# Funktion zum Setzen der Servo-Position
def set_servo_1_angle(angle):
    global servo_1_angle
    angle = max(0, min(180, angle))  # Begrenzung auf 0–180
    duty_ns = int(500_000 + (angle / 180) * 2000_000)
    servo_1.duty_ns(duty_ns)
    servo_1_angle = angle
    save_servo_1_position(angle)  # Speichere die neue Position
    print(f"-> Servo_1 auf {servo_1_angle}°")
    
# Funktion zum Laden der gespeicherten Servo-Position
def load_servo_1_position():
    try:
        with open("Servo_1_pos.txt", "r") as f:
            return int(f.read())  # Gibt die gespeicherte Position zurück
    except:
        print("Keine gespeicherte Position gefunden. Setze auf 90°.")
        return 90  # Wenn keine Position vorhanden ist, starte bei 90°

# Setze Servo auf Position OHNE Speicherung
def move_servo_1_without_saving(angle):
    global servo_1_angle
    angle = max(0, min(180, angle))  # Begrenzung auf gültigen Bereich
    duty_ns = int(500_000 + (angle / 180) * 2000_000)
    servo_1.duty_ns(duty_ns)
    servo_1_angle = angle
    print(f"-> Servo_1 initialisiert auf {servo_1_angle}° (ohne Speichern)")

# Lade letzte gespeicherte Position
servo_1_angle = load_servo_1_position()
print(f"Letzte gespeicherte Position: {servo_1_angle}°")

# Nur PWM aktivieren – Servo bleibt auf letzter Position steht
move_servo_1_without_saving(servo_1_angle)

servo_1_mode = "stop"  # "links", "rechts", "stop"
servo_1_step = 4       # Schrittweite in Grad; default: 2
servo_1_delay = 70     # Zeit in ms zwischen Schritten; default: 100
last_servo_1_move = time.ticks_ms()
servo_1_target_angle = None  # Zielwinkel, falls vorhanden

#Servo_2---------------------------------------------
# Funktion zum Speichern der Servo-Position in eine Datei
# def save_servo_2_position(angle):
#     try:
#         with open("Servo_2_pos.txt", "w") as f:
#             f.write(str(angle))  # Schreibe die Position in die Datei
#         print(f"Position {angle} gespeichert.")
#     except Exception as e:
#         print(f"Fehler beim Speichern der Position: {e}")
#         
# Funktion zum Setzen der Servo-Position
# def set_servo_2_angle(angle):
#     global servo_2_angle
#     angle = max(0, min(180, angle))  # Begrenzung auf 0–180
#     duty_ns = int(500_000 + (angle / 180) * 2000_000)
#     servo_2.duty_ns(duty_ns)
#     servo_2_angle = angle
#     save_servo_2_position(angle)  # Speichere die neue Position
#     print(f"-> Servo_2 auf {servo_2_angle}°")
#     
# # Funktion zum Laden der gespeicherten Servo-Position
# def load_servo_2_position():
#     try:
#         with open("Servo_2_pos.txt", "r") as f:
#             return int(f.read())  # Gibt die gespeicherte Position zurück
#     except:
#         print("Keine gespeicherte Position gefunden. Setze auf 90°.")
#         return 90  # Wenn keine Position vorhanden ist, starte bei 90°
# 
# # Setze Servo auf Position OHNE Speicherung
# def move_servo_2_without_saving(angle):
#     global servo_2_angle
#     angle = max(0, min(180, angle))  # Begrenzung auf gültigen Bereich
#     duty_ns = int(500_000 + (angle / 180) * 2000_000)
#     servo_2.duty_ns(duty_ns)
#     servo_2_angle = angle
#     print(f"-> Servo_2 initialisiert auf {servo_2_angle}° (ohne Speichern)")
# 
# # Lade letzte gespeicherte Position
# servo_2_angle = load_servo_2_position()
# print(f"Letzte gespeicherte Position: {servo_2_angle}°")
# 
# # Nur PWM aktivieren – Servo bleibt auf letzter Position steht
# move_servo_2_without_saving(servo_2_angle)
#
#servo_2_mode = "stop"  # "links", "rechts", "stop"
#servo_2_step = 4       # Schrittweite in Grad
#servo_2_delay = 70     # Zeit in ms zwischen Schritten; default:100
#last_servo_2_move = time.ticks_ms()


#Servo_3---------------------------------------------
# # Funktion zum Speichern der Servo-Position in eine Datei
# def save_servo_3_position(angle):
#     try:
#         with open("Servo_3_pos.txt", "w") as f:
#             f.write(str(angle))  # Schreibe die Position in die Datei
#         print(f"Position {angle} gespeichert.")
#     except Exception as e:
#         print(f"Fehler beim Speichern der Position: {e}")
#         
# # Funktion zum Setzen der Servo-Position
# def set_servo_3_angle(angle):
#     global servo_3_angle
#     angle = max(0, min(180, angle))  # Begrenzung auf 0–180
#     duty_ns = int(500_000 + (angle / 180) * 2000_000)
#     servo_3.duty_ns(duty_ns)
#     servo_3_angle = angle
#     save_servo_3_position(angle)  # Speichere die neue Position
#     print(f"-> Servo_3 auf {servo_3_angle}°")
#     
# # Funktion zum Laden der gespeicherten Servo-Position
# def load_servo_3_position():
#     try:
#         with open("Servo_3_pos.txt", "r") as f:
#             return int(f.read())  # Gibt die gespeicherte Position zurück
#     except:
#         print("Keine gespeicherte Position gefunden. Setze auf 90°.")
#         return 90  # Wenn keine Position vorhanden ist, starte bei 90°
# 
# # Setze Servo auf Position OHNE Speicherung
# def move_servo_3_without_saving(angle):
#     global servo_3_angle
#     angle = max(0, min(180, angle))  # Begrenzung auf gültigen Bereich
#     duty_ns = int(500_000 + (angle / 180) * 2000_000)
#     servo_3.duty_ns(duty_ns)
#     servo_3_angle = angle
#     print(f"-> Servo_3 initialisiert auf {servo_3_angle}° (ohne Speichern)")
# 
# # Lade letzte gespeicherte Position
# servo_3_angle = load_servo_3_position()
# print(f"Letzte gespeicherte Position: {servo_3_angle}°")
# 
# # Nur PWM aktivieren – Servo bleibt auf letzter Position steht
# move_servo_3_without_saving(servo_3_angle)
#
#servo_3_mode = "stop"  # "links", "rechts", "stop"
#servo_3_step = 4       # Schrittweite in Grad
#servo_3_delay = 70     # Zeit in ms zwischen Schritten; default:100
#last_servo_3_move = time.ticks_ms()


#Allgemein: Servos 1-3
def adjust_servo_angle(servo_number, delta):
    if servo_number == 1:
        global servo_1_target_angle
        servo_1_target_angle = max(0, min(180, servo_1_angle + delta))
    #elif servo_number == 2:
        #global servo_2_target_angle
        #servo_2_target_angle = max(0, min(180, servo_2_angle + delta))
    #elif servo_number == 3:
        #global servo_3_target_angle
        #servo_3_target_angle = max(0, min(180, servo_3_angle + delta))


#####################################################
#---Onboard LED-------------------------------------#
#####################################################
led = Pin(25, Pin.OUT)

# Fuer LED-Blink-Timing
last_blink_time = time.ticks_ms()
led_state = False
blink_interval = 500  # Millisekunden


#####################################################
#---Hauptgrogramm-----------------------------------#
#####################################################
print("Pico bereit. LED blinkt. Warte auf UART-Befehle...")
while True:
    
    # Servo-1 Bewegung nach Modus
    if servo_1_mode != "stop":
        now = time.ticks_ms()
        if time.ticks_diff(now, last_servo_1_move) > servo_1_delay:
            if servo_1_mode == "links" and servo_1_angle < 180:
                set_servo_1_angle(servo_1_angle + servo_1_step)
            elif servo_1_mode == "rechts" and servo_1_angle > 0:
                set_servo_1_angle(servo_1_angle - servo_1_step)
            else:
                print("-> Servo_1 an Anschlag, stoppe automatisch")
                servo_1_mode = "stop"
            last_servo_1_move = now
    
    # Servo-2 Bewegung nach Modus
    #if servo_2_mode != "stop":
        #now = time.ticks_ms()
        #if time.ticks_diff(now, last_servo_2_move) > servo_2_delay:
            #if servo_2_mode == "links" and servo_2_angle < 180:
                #set_servo_22_angle(servo_2_angle + servo_2_step)
            #elif servo_2_mode == "rechts" and servo_2_angle > 0:
                #set_servo_2_angle(servo_2_angle - servo_2_step)
            #else:
                #print("-> Servo_2 an Anschlag, stoppe automatisch")
                #servo_2_mode = "stop"
            #last_servo_2_move = now
            
    # Servo-3 Bewegung nach Modus
    #if servo_3_mode != "stop":
        #now = time.ticks_ms()
        #if time.ticks_diff(now, last_servo_3_move) > servo_3_delay:
            #if servo_3_mode == "links" and servo_3_angle < 180:
                #set_servo_3_angle(servo_3_angle + servo_3_step)
            #elif servo_3_mode == "rechts" and servo_3_angle > 0:
                #set_servo_3_angle(servo_3_angle - servo_3_step)
            #else:
                #print("-> Servo_3 an Anschlag, stoppe automatisch")
                #servo_3_mode = "stop"
            #last_servo_3_move = now
    
    # LED-Blinken
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_blink_time) > blink_interval:
        led_state = not led_state
        led.value(led_state)
        last_blink_time = current_time
    
    
    # Servo-1: Grundstellungsfahrt
    if servo_1_target_angle is not None and servo_1_angle != servo_1_target_angle:
        now = time.ticks_ms()
        if time.ticks_diff(now, last_servo_1_move) > servo_1_delay:
            if servo_1_angle < servo_1_target_angle:
                set_servo_1_angle(min(servo_1_target_angle, servo_1_angle + servo_1_step))
            elif servo_1_angle > servo_1_target_angle:
                set_servo_1_angle(max(servo_1_target_angle, servo_1_angle - servo_1_step))
            else:
                pass  # eigentlich nie erreicht
            last_servo_1_move = now
    elif servo_1_target_angle is not None and servo_1_angle == servo_1_target_angle:
        print("-> Servo_1 Grundstellung erreicht.")
        servo_1_target_angle = None
        servo_1_mode = "stop"
        
    # Servo-2: Grundstellungsfahrt
#     if servo_2_target_angle is not None and servo_2_angle != servo_2_target_angle:
#         now = time.ticks_ms()
#         if time.ticks_diff(now, last_servo_2_move) > servo_2_delay:
#             if servo_2_angle < servo_2_target_angle:
#                 set_servo_2_angle(min(servo_2_target_angle, servo_2_angle + servo_2_step))
#             elif servo_2_angle > servo_2_target_angle:
#                 set_servo_2_angle(max(servo_2_target_angle, servo_2_angle - servo_2_step))
#             else:
#                 pass  # eigentlich nie erreicht
#             last_servo_2_move = now
#     elif servo_2_target_angle is not None and servo_2_angle == servo_2_target_angle:
#         print("-> Servo_2 Grundstellung erreicht.")
#         servo_2_target_angle = None
#         servo_2_mode = "stop"
    
    # Servo-3: Grundstellungsfahrt
#     if servo_3_target_angle is not None and servo_3_angle != servo_3_target_angle:
#         now = time.ticks_ms()
#         if time.ticks_diff(now, last_servo_3_move) > servo_3_delay:
#             if servo_3_angle < servo_3_target_angle:
#                 set_servo_3_angle(min(servo_3_target_angle, servo_3_angle + servo_3_step))
#             elif servo_3_angle > servo_3_target_angle:
#                 set_servo_3_angle(max(servo_3_target_angle, servo_3_angle - servo_3_step))
#             else:
#                 pass  # eigentlich nie erreicht
#             last_servo_3_move = now
#     elif servo_3_target_angle is not None and servo_3_angle == servo_3_target_angle:
#         print("-> Servo_3 Grundstellung erreicht.")
#         servo_3_target_angle = None
#         servo_3_mode = "stop"

    
    # UART0
    uart_buffer = ""
    while uart.any():
        char = uart.read(1)
        if char:
            uart_buffer += char.decode('utf-8')

            if '\n' in uart_buffer:
                lines = uart_buffer.split('\n')
                for line in lines[:-1]:
                    msg = line.strip()
                    print("Empfangen:", msg)

                    # Servo_1
                    if msg == 'ServoLinksDrehen_1':
                        servo_1_mode = "links"

                    elif msg == 'ServoRechtsDrehen_1':
                        servo_1_mode = "rechts"

                    elif msg == 'ServoStopp_1':
                        servo_1_mode = "stop"
               
                    # Servo_2
                    #if msg == 'ServoLinksDrehen_2':
                        #servo_2_mode = "links" 

                    #elif msg == 'ServoRechtsDrehen_2':
                        #servo_2_mode = "rechts"

                    #elif msg == 'ServoStopp_2':
                        #servo_2_mode = "stop"
                    
                    # Servo_3
                    #if msg == 'ServoLinksDrehen_3':
                        #servo_3_mode = "links" 

                    #elif msg == 'ServoRechtsDrehen_3':
                        #servo_3_mode = "rechts"

                    #elif msg == 'ServoStopp_3':
                        #servo_3_mode = "stop"
                    
                    # Grundstellungsfahrt
                    elif msg == 'Grundstellungsfahrt':
                        print("Starte Grundstellungsfahrt...")
                        servo_1_target_angle = 90  # Zielwinkel
                        servo_1_mode = "stop"  # Damit nicht gleichzeitig 'links' oder 'rechts' aktiv ist

                        #servo_2_target_angle = 90  # Zielwinkel
                        #servo_2_mode = "stop"  # Damit nicht gleichzeitig 'links' oder 'rechts' aktiv ist

                        #servo_3_target_angle = 90  # Zielwinkel
                        #servo_3_mode = "stop"  # Damit nicht gleichzeitig 'links' oder 'rechts' aktiv ist

                        print("Grundstellung erreicht.")
                    
                    
                    #Steuerkreuz Gamepad
                    elif msg == 'ausfahren_Gamepad':
                        print("-> AUSFAHREN via Gamepad")
                        #adjust_servo_angle(1, 10)--Nicht benoetigt
                        #adjust_servo_angle(2, 10)
                        #adjust_servo_angle(3, 10)

                    elif msg == 'einfahren_Gamepad':
                        print("-> EINFHAREN via Gamepad")
                        #adjust_servo_angle(1, -10)--Nicht benoetigt
                        #adjust_servo_angle(2, -10)
                        #adjust_servo_angle(3, -10)

                    elif msg == 'hoch_Gamepad':
                        print("-> HOCH via Gamepad")
                        #adjust_servo_angle(2, -10)--Nicht benoetigt
                        #adjust_servo_angle(3, +10)

                    elif msg == 'runter_Gamepad':
                        print("-> RUNTER via Gamepad")
                        #adjust_servo_angle(2, +10)--Nicht benoetigt
                        #adjust_servo_angle(3, -10)

                    
                    
                    
                    
                uart_buffer = lines[-1]  # Übriggebliebener Text bleibt im Buffer
                
                
                
    time.sleep_ms(100)
#----------------------------------------FILE ENDE--------------------------------------------



