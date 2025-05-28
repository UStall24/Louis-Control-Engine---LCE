import paho.mqtt.client as mqtt

# Konfiguration
MQTT_BROKER = "0.0.0.0"        # Oder IP des Senders (z.B. PC)
MQTT_PORT = 1883
MQTT_TOPIC = "#"               # "#" empfängt ALLE Topics (Wildcard)

# Callback bei Verbindung
def on_connect(client, userdata, flags, rc):
    print("Verbunden mit MQTT Broker. Rückgabecode:", rc)
    client.subscribe(MQTT_TOPIC)
    print(f"Abonniert auf Topic: {MQTT_TOPIC}")

# Callback bei eingehender Nachricht
def on_message(client, userdata, msg):
    print(f"[{msg.topic}] {msg.payload.decode('utf-8', errors='ignore')}")

# MQTT-Client einrichten
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Verbindung herstellen und starten
client.connect(MQTT_BROKER, MQTT_PORT, 60)
print("Starte MQTT Listener...")
client.loop_forever()
