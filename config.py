import os

class Config(object):
    LOGLEVEL = os.environ.get('LOGLEVEL') or 'WARNING'
    LOGFILE = os.environ.get('LOGFILE') or "./log/datacapture"
    DATABASE = os.environ.get('DATABASE') or '/mnt/db/sqlite/automation.sqlite'
    MQTTHOST = os.environ.get('MQTTHOST') or '192.168.0.134'
    TOPIC = os.environ.get('TOPIC') or 'sorrelhills/temperature/+'
