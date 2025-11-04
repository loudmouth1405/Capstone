# mqtt_publishers.py
import paho.mqtt.client as mqtt
import json, time, random, threading

BROKER = "localhost"
PORT = 1883

vehicles = ["Truck_1", "Truck_2", "Truck_3", "Van_1", "Van_2"]

def publish_vehicle_data(vehicle_id):
    client = mqtt.Client(client_id=vehicle_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
    client.connect(BROKER, PORT, 60)
    
    while True:
        data = {
            "Vehicle_ID": vehicle_id,
            "Engine rpm": random.randint(600, 2200),
            "Lub oil pressure": round(random.uniform(1.0, 7.0), 2),
            "Fuel pressure": round(random.uniform(1.0, 20.0), 2),
            "Coolant pressure": round(random.uniform(1.0, 7.0), 2),
            "lub oil temp": round(random.uniform(70.0, 100.0), 2),
            "Coolant temp": round(random.uniform(70.0, 100.0), 2)
        }
        client.publish(f"fleet/{vehicle_id}/data", json.dumps(data))
        time.sleep(1)

# Run all publishers concurrently
for v in vehicles:
    threading.Thread(target=publish_vehicle_data, args=(v,), daemon=True).start()

print("MQTT Publishers running. Press Ctrl+C to stop.")
while True:
    time.sleep(1)
