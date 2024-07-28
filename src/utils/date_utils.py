#utils.dateutils
from datetime import datetime, timedelta

def increment_datetime(start_datetime, increment_minutes):
    new_datetime = start_datetime + timedelta(minutes=increment_minutes)
    return new_datetime

def format_datetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M")
