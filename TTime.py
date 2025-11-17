from datetime import datetime, timezone, timedelta
import datetime
import schedule
import time
def Get_number_of_academic_week(a) -> int:
    """

    :rtype: int
    """
    match a:
        case 0:
            start_date = date_local
        case 1:
            start_date = date_local + timedelta(days=1)
    if date_local.month < 9:
        start_date = datetime.date(date_local.year - 1, 9, 1)
    else:
        start_date = datetime.date(date_local.year, 9, 1)
    start_week_monday = start_date - timedelta(days=start_date.weekday())
    current_week_monday = date_local - timedelta(days=date_local.weekday())
    weeks_delta = (start_week_monday - current_week_monday).days // 7
    return 1 if weeks_delta % 2 == 0 else 2

global Number_of_academic_week

Chel = timezone(timedelta(hours=5), "Челябинск")
date_local = datetime.datetime.now(Chel)
date_local = datetime.date(date_local.year, date_local.month, date_local.day)

Number_of_academic_week = Get_number_of_academic_week(0)


