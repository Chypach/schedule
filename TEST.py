import json



def get_schedule(group, week_type, day):
    with open('shedule.json', 'r', encoding='utf-8') as f:
        SCHEDULE = json.load(f)
    try:
        l = SCHEDULE[group][week_type][day]
        ls = ""
        for lesson in l:
            ls = ls + lesson + "\n"
        return ls
    except KeyError:
        return None


def get_EN_schedule(group, week_type, day):
    with open('EN_shedule.json', 'r', encoding='utf-8') as f:
        SCHEDULE = json.load(f)
    try:
        l = SCHEDULE[group][week_type][day]
        ls = ""
        for lesson in l:
            ls = ls + lesson + "\n"
        return ls
    except KeyError:
        return None


# group = "group_1"
# week_type = "odd_week"
# day = "monday"
#
# lessons = get_schedule(group, week_type, day)
# print(lessons)
# for lesson in lessons:
#     print(lesson)