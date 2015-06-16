# coding=utf-8

from parser_configs import directories
from parser_utils import load_json_file, save_json_file

__author__ = 'Ilya'

def time_key(schedule_entry):
    time = schedule_entry[1].split(':')
    if len(time) < 2:
        return ""
    hours = time[0]
    minutes = time[1]

    try:
        int(minutes)
    except UnicodeEncodeError:
        return ""

    key = ""
    # Night hours have the biggest weight
    if 0 <= int(hours) <= 3:
        key = "999" + hours + minutes
        print key
    else:
        key = "" + hours + minutes

    return int(key)

if __name__ == "__main__":
    transport_dir = directories['IPHONE_DIR']

    """ BALTIYSKIY BANK MIRA 17"""
    balt_bank_bus_list = ['bus_19', 'bus_6', 'bus_22']
    balt_bank_position = [3, 8, 9]
    balt_bank_bus_dict = {}

    for bus_id in balt_bank_bus_list:
        balt_bank_bus_dict[bus_id] = load_json_file(transport_dir + bus_id + ".json")

    station_schedule = []
    for i in range(len(balt_bank_bus_list)):
        bus_id = balt_bank_bus_list[i]
        sch = balt_bank_bus_dict[bus_id]['schedule_workdays'][balt_bank_position[i]]
        bus_id_list = [bus_id] * len(sch)
        sch = zip(bus_id_list, sch)
        station_schedule += sch
    station_schedule = [x for x in station_schedule if x[1] != "-"]
    station_schedule = sorted(station_schedule, key=time_key)
    station_schedule_workdays = station_schedule

    station_schedule = []
    for i in range(len(balt_bank_bus_list)):
        bus_id = balt_bank_bus_list[i]
        sch = balt_bank_bus_dict[bus_id]['schedule_weekend'][balt_bank_position[i]]
        bus_id_list = [bus_id] * len(sch)
        sch = zip(bus_id_list, sch)
        station_schedule += sch
    station_schedule = [x for x in station_schedule if x[1] != "-"]
    station_schedule = sorted(station_schedule, key=time_key)
    station_schedule_weekend = station_schedule

    station_schedule = {
        'name': u"Балтийский банк",
        'schedule_workdays': station_schedule_workdays,
        'schedule_weekend': station_schedule_weekend
    }

    save_json_file("station_balt_bank.json", station_schedule)

    """ DERZHAVINA"""
    derzhavina_bus_list = ['bus_20', 'bus_4', 'bus_19']
    derzhavina_position = [1, 0, 0]
    derzhavina_bus_dict = {}

    for bus_id in derzhavina_bus_list:
        derzhavina_bus_dict[bus_id] = load_json_file(transport_dir + bus_id + ".json")

    station_schedule = []
    for i in range(len(derzhavina_bus_list)):
        bus_id = derzhavina_bus_list[i]
        sch = derzhavina_bus_dict[bus_id]['schedule_workdays'][derzhavina_position[i]]
        bus_id_list = [bus_id] * len(sch)
        sch = zip(bus_id_list, sch)
        station_schedule += sch
    station_schedule = [x for x in station_schedule if x[1] != "-"]
    station_schedule = sorted(station_schedule, key=time_key)
    station_schedule_workdays = station_schedule

    station_schedule = []
    for i in range(len(derzhavina_bus_list)):
        bus_id = derzhavina_bus_list[i]
        sch = derzhavina_bus_dict[bus_id]['schedule_weekend'][derzhavina_position[i]]
        bus_id_list = [bus_id] * len(sch)
        sch = zip(bus_id_list, sch)
        station_schedule += sch
    station_schedule = [x for x in station_schedule if x[1] != "-"]
    station_schedule = sorted(station_schedule, key=time_key)
    station_schedule_weekend = station_schedule

    station_schedule = {
        'name': u"Ул. Державина",
        'schedule_workdays': station_schedule_workdays,
        'schedule_weekend': station_schedule_weekend
    }

    save_json_file("station_derzhavina.json", station_schedule)

    """ SOFIYSKAYA PLOSHAD"""
    sofiyskaya_square_bus_list = ['bus_2', 'bus_4', 'bus_19']
    sofiyskaya_square_position = [2, 2, 2]
    sofiyskaya_square_bus_dict = {}

    for bus_id in sofiyskaya_square_bus_list:
        sofiyskaya_square_bus_dict[bus_id] = load_json_file(transport_dir + bus_id + ".json")

    station_schedule = []
    for i in range(len(sofiyskaya_square_bus_list)):
        bus_id = sofiyskaya_square_bus_list[i]
        sch = sofiyskaya_square_bus_dict[bus_id]['schedule_workdays'][sofiyskaya_square_position[i]]
        bus_id_list = [bus_id] * len(sch)
        sch = zip(bus_id_list, sch)
        station_schedule += sch
    station_schedule = [x for x in station_schedule if x[1] != "-"]
    station_schedule = sorted(station_schedule, key=time_key)
    station_schedule_workdays = station_schedule

    station_schedule = []
    for i in range(len(sofiyskaya_square_bus_list)):
        bus_id = sofiyskaya_square_bus_list[i]
        sch = sofiyskaya_square_bus_dict[bus_id]['schedule_weekend'][sofiyskaya_square_position[i]]
        bus_id_list = [bus_id] * len(sch)
        sch = zip(bus_id_list, sch)
        station_schedule += sch
    station_schedule = [x for x in station_schedule if x[1] != "-"]
    station_schedule = sorted(station_schedule, key=time_key)
    station_schedule_weekend = station_schedule

    station_schedule = {
        'name': u"Софийская площадь",
        'schedule_workdays': station_schedule_workdays,
        'schedule_weekend': station_schedule_weekend
    }

    save_json_file("station_sofiyskaya_square.json", station_schedule)

    stations = [
        {'id': "station_sofiyskaya_square", 'name': u"Софийская площадь"},
        {'id': "station_balt_bank", 'name': u"Балтийский банк"},
        {'id': "station_derzhavina", 'name': u"Ул. Державина"}
    ]

    save_json_file("stations.json", stations)
