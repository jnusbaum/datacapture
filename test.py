import os
import logging
from datetime import datetime
import paho.mqtt.client as mqtt
import time
from config import Config

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


def str_to_datetime(ans):
    if ans:
        d = datetime.strptime(ans, "%Y-%m-%d-%H-%M-%S")
        # no tz info, assumed to be in UTC
        return d
    return None


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.publish("sorrelhills/temperature/zone/BOILER", "test payload")


def on_publish(client, userdata, mid):
    time.sleep(5)
    client.publish("sorrelhills/temperature/zone/BOILER", "test payload")


client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

client.connect("192.168.0.134", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
