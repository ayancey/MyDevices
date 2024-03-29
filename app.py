import routeros_api
from bottle import route, run, template
import paho.mqtt.client as mqtt
import threading
import json
import math
import requests


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


def get_all_dns():
    mikrotik_dns = {}

    for rec in api.get_resource('/ip/dns/static').get():
        mikrotik_dns[rec["name"]] = rec["address"]

    s = requests.session()
    s.headers.update({
        "Authorization": "Bearer ***REMOVED***"
    })
    r = s.get("https://api.cloudflare.com/client/v4/zones/***REMOVED***/dns_records")

    services = []

    for record in r.json()["result"]:
        internal_url = None
        external_url = None

        if record["content"].startswith("10.45."):
            rec_type = "Internal"
            internal_url = "http://" + record["name"]
        elif (record["type"] == "CNAME" and record["content"] == "***REMOVED***") or record["content"] == "***REMOVED***":
            rec_type = "External"
            if record["name"] in mikrotik_dns:
                internal_url = "https://" + record["name"]
                rec_type = "Internal/External"
            else:
                internal_url = "https://" + record["content"]
            external_url = "https://" + record["name"]
        elif "cfargotunnel" in record["content"]:
            rec_type = "External (ZTNA)"
            if record["name"] in mikrotik_dns:
                internal_url = "https://" + record["content"]
                rec_type = "Internal/External (ZTNA)"
            external_url = "https://" + record["name"]
        else:
            continue

        services.append({
            "name": record["name"],
            "type": rec_type,
            "internal_url": internal_url,
            "external_url": external_url
        })

    for int_record in mikrotik_dns:
        if int_record not in list(map(lambda s: s["name"], services)):
            services.append({
                "name": int_record,
                "type": "Internal",
                "internal_url": "http://" + int_record,
                "external_url": None
            })

    return services


@route("/")
def index():
    return template("devices", devices=sorted(api.get_resource('/ip/dhcp-server/lease').get(), key=lambda d: d["address"]), iot={
        "server_room_temp": server_room_temp,
        "server_room_hum": server_room_hum,
        "studio_temp": studio_temp,
        "studio_hum": studio_hum
    }, services=sorted(get_all_dns(), key=lambda s: s["name"]))


client = mqtt.Client("mydevices") #create new instance
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
