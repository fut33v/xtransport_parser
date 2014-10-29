import re


class SuburbanScheduleParser:

    _regex_str_one_day = r"[0-9]{1,2}-[0-9]{1,2}\([0-9]{1}\)"
    _regex_str_range_of_days = r"[0-9]{1,2}-[0-9]{1,2}\([0-9]{1}-[0-9]{1}\)"
    _regex_str_set_of_days = r"[0-9]{1,2}-[0-9]{1,2}\([0-9]{1},[0-9]{1}\)"
    _regex_str_normal_end = r"[0-9]{1,2}-[0-9]{1,2}$"
    _regex_str_normal_middle = r"([0-9]{1,2}-[0-9]{1,2}),"

    _regex_one_day = re.compile(_regex_str_one_day)
    _regex_range_of_days = re.compile(_regex_str_range_of_days)
    _regex_set_of_days = re.compile(_regex_str_set_of_days)
    _regex_normal_end = re.compile(_regex_str_normal_end)
    _regex_normal_middle = re.compile(_regex_str_normal_middle)

    _days_dict = {
        1: 'monday',
        2: 'tuesday',
        3: 'wendesday',
        4: 'thursday',
        5: 'friday',
        6: 'saturday',
        7: 'sunday',
    }

    @classmethod
    def parse_schedule(cls, schedule_string):
        schedule = {}
        all_days = cls._regex_normal_middle.findall(schedule_string)
        all_days += cls._regex_normal_end.findall(schedule_string)
        print 'all_days:', all_days

        for i in range(len(cls._days_dict)):
            schedule[cls._days_dict[i]] = all_days

        return schedule
