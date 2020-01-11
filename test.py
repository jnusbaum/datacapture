import json
from datetime import datetime
import paho.mqtt.client as mqtt
import time

def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj)))


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    ts = datetime.today()
    payload = {
            'IN': {
                'type': 'TEMP',
                'timestamp': ts,
                'value': 142.3
            },
            'OUT': {
                'type': 'TEMP',
                'timestamp': ts,
                'value': 135.7
            }
    }

    jload = json.dumps(payload, default=handler)
    client.publish("sorrelhills/temperature/zone/BOILER", jload)


def on_publish(client, userdata, mid):
    time.sleep(5)
    ts = datetime.today()
    payload = {
            'IN': {
                'type': 'TEMP',
                'timestamp': ts,
                'value': 142.3
            },
            'OUT': {
                'type': 'TEMP',
                'timestamp': ts,
                'value': 135.7
            }
    }

    jload = json.dumps(payload, default=handler)
    client.publish("sorrelhills/temperature/zone/BOILER", jload)


client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

client.connect("192.168.0.134", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
