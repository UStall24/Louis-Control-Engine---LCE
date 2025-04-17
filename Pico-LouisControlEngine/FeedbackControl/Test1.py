import smbus2
import time

# I2C-Adresse des LIS3DH-Sensors
LIS3DH_ADDRESS = 0x18  # Kann auch 0x19 sein, je nach Konfiguration

# Register des LIS3DH
CTRL_REG1 = 0x20
OUT_X_L = 0x28
OUT_X_H = 0x29
OUT_Y_L = 0x2A
OUT_Y_H = 0x2B
OUT_Z_L = 0x2C
OUT_Z_H = 0x2D

# I2C-Bus initialisieren
bus = smbus2.SMBus(1)

# Sensor initialisieren
bus.write_byte_data(LIS3DH_ADDRESS, CTRL_REG1, 0x47)  # Aktivieren Sie den Sensor mit 100 Hz

def read_accel_data(register):
    # Liest 2 Bytes (High und Low) und kombiniert sie zu einem 16-Bit-Wert
    low = bus.read_byte_data(LIS3DH_ADDRESS, register)
    high = bus.read_byte_data(LIS3DH_ADDRESS, register + 1)
    value = (high << 8) | low
    if value > 32767:  # Korrektur für negative Werte
        value -= 65536
    return value

try:
    while True:
        # Beschleunigungsdaten auslesen
        x = read_accel_data(OUT_X_L)
        y = read_accel_data(OUT_Y_L)
        z = read_accel_data(OUT_Z_L)

        # Ausgabe der Rohdaten
        print(f"X: {x}, Y: {y}, Z: {z}")

        time.sleep(0.1)  # 100 ms Pause

except KeyboardInterrupt:
    print("Programm beendet")