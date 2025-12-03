from datetime import datetime, timezone, timedelta
import datetime
from zoneinfo import ZoneInfo
import time

w = [("понедельник"), ("вторник"), ("среда"), ("четверг"), ("пятница"), ("суббота"), ("воскресенье"), ("понедельник")]
w2 = [("monday"), ("tuesday"), ("wednesday"), ("thursday"), ("friday"), ("saturday"), ("sunday"), ("monday")]
Chel = timezone(timedelta(hours=5), "Челябинск")


def wtoday():
    dt = datetime.datetime.today()
    res = datetime.date(dt.year, dt.month, dt.day)
    return w2[res.weekday()]
def wtomorrow():
    dt = datetime.datetime.today()
    res = datetime.date(dt.year, dt.month, dt.day)
    return w2[res.isoweekday()]

def RUtoday():
    dt = datetime.datetime.today()
    res = datetime.date(dt.year, dt.month, dt.day)
    return w[res.weekday()]
def RUtomorrow():
    dt = datetime.datetime.today()
    res = datetime.date(dt.year, dt.month, dt.day)
    return w[res.isoweekday()]



def dataToday():
    dt = datetime.datetime.today()
    res = datetime.date(dt.year, dt.month, dt.day)
    f = f"({dt.year},{dt.month},{dt.day}), {RUtoday()}:"
    return f
def datatomorrow():
    dt1 = datetime.datetime.today() + timedelta(days=1)
    f = f"({dt1.year},{dt1.month},{dt1.day}), {RUtomorrow()}:"
    return f

def ENdataToday():
    dt = datetime.datetime.today()
    f = f"({dt.year},{dt.month},{dt.day}), {wtoday()}:"
    return f
def ENatatomorrow():
    dt1 = datetime.datetime.today() + timedelta(days=1)
    f = f"({dt1.year},{dt1.month},{dt1.day}), {wtomorrow()}:"
    return f

def TodayYear():
    today = datetime.date.today()
    today = f"{today:%j}"
    return today



