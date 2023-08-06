import routeros_api
from bottle import route, run, template
import paho.mqtt.client as mqtt
import threading
import json
import math

connection = routeros_api.RouterOsApiPool("10.45.1.1", username="admin", password="***REMOVED***", plaintext_login=True)
api = connection.get_api()


server_room_temp = None
server_room_hum = None
studio_temp = None
studio_hum = None


def on_message(_, _2, msg):
    global server_room_temp
    global server_room_hum
    global studio_temp
    global studio_hum

    if msg.topic == "zigbee2mqtt/***REMOVED***":
        print("server room updated")
        data = json.loads(msg.payload.decode())
        server_room_temp = math.ceil((data["temperature"] * 9/5) + 32)
        server_room_hum = data["humidity"]
    elif msg.topic == "zigbee2mqtt/***REMOVED***":
        print("studio updated")
        data = json.loads(msg.payload.decode())
        studio_temp = math.ceil((data["temperature"] * 9/5) + 32)
        studio_hum = data["humidity"]


@route("/")
def index():
    return template("devices", devices=sorted(api.get_resource('/ip/dhcp-server/lease').get(), key=lambda d: d["address"]), iot={
        "server_room_temp": server_room_temp,
        "server_room_hum": server_room_hum,
        "studio_temp": studio_temp,
        "studio_hum": studio_hum
    })


client = mqtt.Client("mydevices", protocol=mqtt.MQTTv5) #create new instance
client.connect("***REMOVED***") #connect to broker
client.subscribe("zigbee2mqtt/***REMOVED***")
client.subscribe("zigbee2mqtt/***REMOVED***")

client.on_message = on_message


def mqtt_thread():
    client.loop_forever()


x = threading.Thread(target=mqtt_thread, args=())
x.daemon = True
x.start()

run(host='0.0.0.0', port=8080)
