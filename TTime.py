from datetime import datetime, timezone, timedelta
import datetime
from zoneinfo import ZoneInfo
import schedule
import time

w = [("понедельник"), ("вторник"), ("среда"), ("четверг"), ("пятница"), ("суббота"), ("воскресенье"), ("понедельник")]

Chel = timezone(timedelta(hours=5), "Челябинск")


dt = datetime.datetime.today()
print("время сейчас",dt)
dt = datetime.datetime.now(Chel)
print("время сейчас",dt)
print(dt.year, dt.month, dt.day)
print(dt.hour, dt.minute, dt.second)
res = datetime.date(dt.year, dt.month, dt.day)
print("Сегодня", w[res.weekday()])
print("Завтра", w[res.isoweekday()])


def job():
    global Nomber_of_weak
    if Nomber_of_weak == 1:
        Nomber_of_weak += 1
        print(Nomber_of_weak)
    elif Nomber_of_weak == 2:
        Nomber_of_weak -= 1
        print(Nomber_of_weak)


Nomber_of_weak = 2
schedule.every().seconds.do(job)
schedule.every().sunday.at("00:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)