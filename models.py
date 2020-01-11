from datetime import datetime
from decimal import *
from pony.orm import *

db = Database()


class Sensor(db.Entity):
    name = PrimaryKey(str, 256)
    type = Required(str, 8)
    address = Optional(str, 128)
    description = Optional(str, 512)
    zone = Optional('Zone')
    data = Set('SensorData')
    hour_bad = Optional(int)
    day_bad = Optional(int)
    ten_day_bad = Optional(int)


class Zone(db.Entity):
    name = PrimaryKey(str, 256, auto=True)
    description = Optional(str, 512)
    sensors = Set(Sensor)


class SensorData(db.Entity):
    id = PrimaryKey(int, auto=True)
    sensor = Required(Sensor)
    timestamp = Required(datetime)
    value = Optional(Decimal)
    original_value = Optional(Decimal)


