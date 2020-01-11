import os

class Config(object):
    LOGLEVEL = os.environ.get('LOGLEVEL') or 'INFO'
    LOGFILE = os.environ.get('LOGFILE') or "./log/datacapture"
    DATABASE = os.environ.get('DATABASE') or './db/database.sqlite'
    MQTTHOST = os.environ.get('MQTTHOST') or '192.168.0.134'
