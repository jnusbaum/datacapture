import os
import logging
from statistics import mean
import paho.mqtt.client as mqtt
from config import Config
from models import *

MAX_TEMP_MOVE = 25
MIN_TEMP = 30

# set up logger
# make file unique
# we will be running multiple processes behind gunicorn
# we do not want all the processes writing to the same log file as this can result in garbled data in the file
# so we need a unique file name each time we run
# we will add date and time down to seconds (which will probably be the same for all processes)
# and add process id to get uniqueness
fparts = Config.LOGFILE.split('.')
bname = fparts[0]
ename = fparts[1]
nname = "%s.%s.%d.%s" % (bname, datetime.today().strftime("%Y-%m-%d-%H-%M-%S"), os.getpid(), ename)
logfile = Config.LOGDIR + nname
# create log directory if it does not exist
os.makedirs(Config.LOGDIR, 0o777, True)
# set up basic logging
logging.basicConfig(filename=logfile, level=Config.LOGLEVEL,
                    format='%(asctime)s - %(levelname)s - %(message)s')


db.bind(provider='postgres', host=Config.DBHOST,
        database=Config.DATABASE,
        user=Config.DBUSER,
        password=Config.DBPWD)

db.generate_mapping()


def str_to_datetime(ans):
    if ans:
        d = datetime.strptime(ans, "%Y-%m-%d-%H-%M-%S")
        # no tz info, assumed to be in UTC
        return d
    return None


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sorrelhills/temperature/zone/+")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    # save data to db
    # zone payload is JSON object containing sensor value for each sensor in zone
    # {
    #         'IN': {
    #             'type': 'TEMP'',
    #             'timestamp': <value>,
    #             'value': '142.3'
    #         },
    #         'OUT': {
    #             'type': 'TEMP',
    #             'timestamp': < value >,
    #             'value': '135.7'
    #         },
    #         'PUMP': {
    #              'type': 'ONOFF',
    #              'timestamp': <value>,
    #              'value': 'on'
    #         },
    #         ...
    # }


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(Config.MQTTHOST)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
