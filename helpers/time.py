import pytz
from datetime import datetime

def timestamp_to_localize(timestamp, timezone):
  time = datetime.fromtimestamp(timestamp/1000)
  
  tz = pytz.timezone(timezone)
  return tz.localize(time).strftime("%Y-%m-%d %H:%M:%S")
