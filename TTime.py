from datetime import datetime, timezone, timedelta
import datetime
from zoneinfo import ZoneInfo
import schedule
import time

w = [("понедельник"), ("вторник"), ("среда"), ("четверг"), ("пятница"), ("суббота"), ("воскресенье"), ("понедельник")]
w2 = [("monday"), ("tuesday"), ("wednesday"), ("thursday"), ("friday"), ("saturday"), ("sunday"), ("monday")]
Chel = timezone(timedelta(hours=5), "Челябинск")


dt = datetime.datetime.today()
# print("время сейчас",dt)
# dt = datetime.datetime.now(Chel)
# print("время сейчас",dt)
# print(dt.year, dt.month, dt.day)
# print(dt.hour, dt.minute, dt.second)
res = datetime.date(dt.year, dt.month, dt.day)
# print("Сегодня", w2[res.weekday()])
# print("Завтра", w2[res.isoweekday()])

def wtoday():
    return w2[res.weekday()]
def wtomorrow():
    return w2[res.isoweekday()]



def TodayYear():
    today = datetime.date.today()
    today = f"{today:%j}"
    return today
