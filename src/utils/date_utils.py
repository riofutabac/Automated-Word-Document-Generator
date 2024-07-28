#utils.dateutils
from datetime import datetime, timedelta

def increment_datetime(start_datetime, increment_minutes):
    return start_datetime + timedelta(minutes=increment_minutes)

def format_datetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M")
