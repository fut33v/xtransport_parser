import re
import string


class SuburbanScheduleParser:

    _regex_str_range_of_days = r"\d{1,2}-\d{1,2}\(\d{1}-\d{1}\)"
    _regex_str_set_of_days = r"\d{1,2}-\d{1,2}\(\d{1},\d{1}\)"
    _regex_str_normal_end = r"\d{1,2}-\d{1,2}$"
    _regex_str_normal_middle = r"(\d{1,2}-\d{1,2}),"
    _regex_str_one_day = r"(\d{1,2}-\d{1,2})\((\d{1})\)"

    _regex_range_of_days = re.compile(_regex_str_range_of_days)
    _regex_set_of_days = re.compile(_regex_str_set_of_days)
    _regex_normal_end = re.compile(_regex_str_normal_end)
    _regex_normal_middle = re.compile(_regex_str_normal_middle)
    _regex_one_day = re.compile(_regex_str_one_day)

    _regex_str_range_of_days_finish = (
        r"(\d{1,2}-\d{1,2})\((\d{1})-(\d{1})\)"
    )
    _regex_str_set_of_days_finish = (
        r"(\d{1,2}-\d{1,2})\(((\d{1})(,{1}\d{1})*)\)"
    )
    _regex_str_one_day_finish = r"\d{1,2}-\d{1,2}\((\d{1})\)"

    _regex_range_of_days_finish = re.compile(_regex_str_range_of_days_finish)
    _regex_set_of_days_finish = re.compile(_regex_str_set_of_days_finish)

    _days_dict = {
        1: 'monday',
        2: 'tuesday',
        3: 'wednesday',
        4: 'thursday',
        5: 'friday',
        6: 'saturday',
        7: 'sunday',
    }

    @classmethod
    def parse_schedule(cls, schedule_string):
        schedule = {}
        for k, v in cls._days_dict.iteritems():
            schedule[v] = []

        # time, that is the same for all days
        all_days = cls._regex_normal_middle.findall(schedule_string)
        all_days += cls._regex_normal_end.findall(schedule_string)
        for i in range(1, len(cls._days_dict) + 1):
            schedule[cls._days_dict[i]] = list(all_days)

        # time, that is the same for range of  days
        ranges = cls._regex_range_of_days.findall(schedule_string)
        for range_ in ranges:
            m = cls._regex_range_of_days_finish.search(range_)
            time = m.group(1)
            r = range(int(m.group(2)), int(m.group(3)) + 1)
            for i in r:
                schedule[cls._days_dict[i]].append(time)

        # time, that is the same for set of days, that presented
        # by list, separated with commas
        sets_of_days = cls._regex_set_of_days.findall(schedule_string)
        for set_ in sets_of_days:
            m = cls._regex_set_of_days_finish.search(set_)
            time = m.group(1)
            set_of_days = m.group(2)
            days = string.split(set_of_days, ',')
            days = [int(x) for x in days]
            for i in days:
                schedule[cls._days_dict[i]].append(time)

        # time for only one day e.g: 18-21(4)
        one_days = cls._regex_one_day.finditer(schedule_string)
        for m in one_days:
            time = m.group(1)
            m.group(2)


        return schedule
