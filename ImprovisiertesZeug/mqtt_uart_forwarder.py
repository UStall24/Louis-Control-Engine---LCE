import json
import serial
import paho.mqtt.client as mqtt

# Konfiguration
MQTT_BROKER = "192.168.0.3"        # IP des Brokers (oder localhost wenn lokal)
MQTT_PORT = 1883
MQTT_TOPIC = "gripper/values"
UART_PORT = "/dev/ttyAMA0"     # Oder /dev/ttyAMA0 je nach Setup
UART_BAUDRATE = 115200

# UART initialisieren
ser = serial.Serial(UART_PORT, UART_BAUDRATE, timeout=1)

# Callback bei Verbindung
def on_connect(client, userdata, flags, rc):
    print("MQTT verbunden mit Code", rc)
    client.subscribe(MQTT_TOPIC)

# Callback bei Nachricht
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())

        print(f"Empfangene Nachricht: {payload}")

        gripper_values = payload.get("GripperValues", [])
        if isinstance(gripper_values, list):
            ser.write(bytes(gripper_values))
            print(">> Gesendet an UART:", gripper_values)
    except Exception as e:
        print("Fehler beim Verarbeiten der Nachricht:", e)

# MQTT-Client einrichten
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Start
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
