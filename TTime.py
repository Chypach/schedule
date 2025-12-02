from datetime import datetime, timezone, timedelta
import datetime
from zoneinfo import ZoneInfo
import schedule
import time

w = [("понедельник"), ("вторник"), ("среда"), ("четверг"), ("пятница"), ("суббота"), ("воскресенье"), ("понедельник")]
w2 = [("monday"), ("tuesday"), ("wednesday"), ("thursday"), ("friday"), ("saturday"), ("sunday"), ("monday")]
Chel = timezone(timedelta(hours=5), "Челябинск")


dt = datetime.datetime.today()
dt1 = datetime.datetime.today() + timedelta(days=1)

# print("время сейчас",dt)
# dt = datetime.datetime.now(Chel)
# print("время сейчас",dt)
# print("сегодня",dt.year, dt.month, dt.day)

# print(dt.hour, dt.minute, dt.second)
res = datetime.date(dt.year, dt.month, dt.day)

def wtoday():
    return w2[res.weekday()]
def wtomorrow():
    return w2[res.isoweekday()]

def RUtoday():
    return w[res.weekday()]
def RUtomorrow():
    return w[res.isoweekday()]



def dataToday():
    f = f"({dt.year},{dt.month},{dt.day}), {RUtoday()}:"
    return f
def datatomorrow():
    f = f"({dt1.year},{dt1.month},{dt1.day}), {RUtomorrow()}:"
    return f

def ENdataToday():
    f = f"({dt.year},{dt.month},{dt.day}), {wtoday()}:"
    return f
def ENatatomorrow():
    f = f"({dt1.year},{dt1.month},{dt1.day}), {wtomorrow()}:"
    return f

def TodayYear():
    today = datetime.date.today()
    today = f"{today:%j}"
    return today


print(dataToday())

