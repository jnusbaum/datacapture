import os
import logging
from datetime import datetime
import json
import paho.mqtt.client as mqtt
from config import Config
import sqlite3

MIN_TEMP = 25

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.info(f"Connected with result code {rc}")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(Config.TOPIC)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # save data to db
    # zone payload is JSON object containing sensor value
    #         {
    #             'sensor': 'BOILER-IN',
    #             'timestamp': '2020-01-11T14:33:10.772357',
    #             'value': 142.3
    #         }
    con = userdata
    print(str(msg.payload))
    payload = json.loads(msg.payload)
    with con:
        fsname = payload['sensor']
        timestamp = datetime.fromisoformat(payload['timestamp'])
        value = payload['value']
        ovalue = value
        if value < MIN_TEMP:
            logging.warning(f"replacing {value} with {MIN_TEMP} for {fsname}, {timestamp}")
            value = MIN_TEMP
        logging.debug(f"inserting {fsname}, {timestamp}, {value}")
        con.execute("insert into heating_sensordata(sensor_id, timestamp, value, original_value) values (?, ?, ?, ?)", (fsname, timestamp, value, ovalue))


# set up logger
logfile = f"{Config.LOGFILE}.{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}.log"
# create log directory if it does not exist
os.makedirs(os.path.dirname(logfile), 0o777, True)
# set up basic logging
logging.basicConfig(filename=logfile, level=Config.LOGLEVEL, format='%(asctime)s - %(levelname)s - %(message)s')
# create db directory if it does not exist
os.makedirs(os.path.dirname(Config.DATABASE), 0o777, True)

con = sqlite3.connect(Config.DATABASE)
client = mqtt.Client(userdata=con)
client.on_connect = on_connect
client.on_message = on_message
client.connect(Config.MQTTHOST)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
