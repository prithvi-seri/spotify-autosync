from datetime import datetime
from zoneinfo import ZoneInfo

def monthly_playlist() -> str:
  est = ZoneInfo('America/New_York')
  month = datetime.now(est).strftime('%B')
  return month.lower()
