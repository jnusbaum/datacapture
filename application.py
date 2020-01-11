import os
import logging
import json
import paho.mqtt.client as mqtt
from config import Config
from models import *


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sorrelhills/temperature/zone/+")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # pick zone name out of topic
    tlevels = msg.topic.split('/')
    zname = tlevels[-1]
    print(zname+" "+str(msg.payload))
    # save data to db
    # zone payload is JSON object containing sensor value for each sensor in zone
    # {
    #         'IN': {
    #             'type': 'TEMP'',
    #             'timestamp': '2020-01-11T14:33:10.772357',
    #             'value': 142.3
    #         },
    #         'OUT': {
    #             'type': 'TEMP',
    #             'timestamp': '2020-01-11T14:33:25.773748',
    #             'value': 135.7
    #         },
    #         'PUMP': {
    #              'type': 'ONOFF',
    #              'timestamp': '2020-01-11T14:33:35.774187',
    #              'value': 1
    #         },
    #         ...
    # }
    payload = json.loads(msg.payload)
    with db_session:
        for sname, sdata in payload.items():
            fsname = zname + '-' + sname
            timestamp = datetime.fromisoformat(sdata['timestamp'])
            value = sdata['value']
            sensor = Sensor[fsname]
            SensorData(sensor=sensor, timestamp=timestamp, value=value)


# set up logger
logfile = f"{Config.LOGFILE}.{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}.log"
# create log directory if it does not exist
os.makedirs(os.path.dirname(logfile), 0o777, True)
# set up basic logging
logging.basicConfig(filename=logfile, level=Config.LOGLEVEL, format='%(asctime)s - %(levelname)s - %(message)s')
# create db directory if it does not exist
os.makedirs(os.path.dirname(Config.DATABASE), 0o777, True)

db.bind(provider='sqlite', filename=Config.DATABASE, create_db=True)

db.generate_mapping(create_tables=True)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(Config.MQTTHOST)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
