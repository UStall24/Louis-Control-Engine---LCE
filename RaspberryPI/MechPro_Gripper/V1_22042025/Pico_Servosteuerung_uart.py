

###################################################################
#---File-Informationen--------------------------------------------#
###################################################################
# File Name: Pico_Servosteuerung_uart.py
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
# Erweiterung um Servo_2 und Servo_3                                                  // 10.04.2025       // Johann Spielvogel
# Anpassung der MQTT Nachrichten                                                      // 13.04.2025       // Johann Spielvogel
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
def set_servo_1_angle(angle):
    # Mappe Winkel (0–180) auf PWM Duty in ns für MicroPython
    duty_ns = int(500_000 + (angle / 180) * 2000_000)
    servo_1.duty_ns(duty_ns)
    
#Servo_2---------------------------------------------
#def set_servo_2_angle(angle):
    # Mappe Winkel (0–180) auf PWM Duty in ns für MicroPython
    #duty_ns = int(500_000 + (angle / 180) * 2000_000)
    #servo_2.duty_ns(duty_ns)
    
#Servo_3---------------------------------------------
#def set_servo_3_angle(angle):
    # Mappe Winkel (0–180) auf PWM Duty in ns für MicroPython
    #duty_ns = int(500_000 + (angle / 180) * 2000_000)
    #servo_3.duty_ns(duty_ns)


#####################################################
#---Onboard LED-------------------------------------#
#####################################################
led = Pin(25, Pin.OUT)

# Für LED-Blink-Timing
last_blink_time = time.ticks_ms()
led_state = False
blink_interval = 500  # Millisekunden


#####################################################
#---Hauptgrogramm-----------------------------------#
#####################################################
print("Pico bereit. LED blinkt. Warte auf UART-Befehle...")
while True:
    
    # LED-Blinken
    current_time = time.ticks_ms()
    if time.ticks_diff(current_time, last_blink_time) > blink_interval:
        led_state = not led_state
        led.value(led_state)
        last_blink_time = current_time
        
    # UART0   
    if uart.any():
        message = uart.readline()
        if message:
            msg = message.decode('utf-8').strip()
            print("Empfangen:", msg)
            
            # Servo_1
            if msg == 'ServoLinksDrehen_1':
                set_servo_1_angle(180)
                print("-> Servo_1 auf 180°")
                #uart.write(b'Servo_1 auf 180\n') 

            elif msg == 'ServoRechtsDrehen_1':
                set_servo_1_angle(0)
                print("-> Servo_1 auf 0°")
                #uart.write(b'Servo_1 auf 0\n')

            elif msg == 'ServoStopp_1':
                set_servo_1_angle(90)
                print("-> Servo_1 auf 90° (Stopp)")
                #uart.write(b'Servo_1 auf 90\n')
            
            # Servo_2
            #if msg == 'ServoLinksDrehen_2':
                #set_servo_2_angle(180)
                #print("-> Servo_2 auf 180°")
                #uart.write(b'Servo_2 auf 180\n') 

            #elif msg == 'ServoRechtsDrehen_2':
                #set_servo_2_angle(0)
                #print("-> Servo_2 auf 0°")
                #uart.write(b'Servo_2 auf 0\n')

            #elif msg == 'ServoStopp_2':
                #set_servo_2_angle(90)
                #print("-> Servo_2 auf 90° (Stopp)")
                #uart.write(b'Servo_2 auf 90\n')
            
            # Servo_3
            #if msg == 'ServoLinksDrehen_3':
                #set_servo_3_angle(180)
                #print("-> Servo_3 auf 180°")
                #uart.write(b'Servo_3 auf 180\n') 

            #elif msg == 'ServoRechtsDrehen_3':
                #set_servo_3_angle(0)
                #print("-> Servo_3 auf 0°")
                #uart.write(b'Servo_3 auf 0\n')

            #elif msg == 'ServoStopp_3':
                #set_servo_3_angle(90)
                #print("-> Servo_3 auf 90° (Stopp)")
                #uart.write(b'Servo_3 auf 90\n')
    
    time.sleep(0.1)

#----------------------------------------FILE ENDE--------------------------------------------
