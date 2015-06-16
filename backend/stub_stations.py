from parser_configs import directories
from parser_utils import load_json_file

__author__ = 'Ilya'

def time_key(schedule_entry):
    time = schedule_entry[1].split(':')
    print "" + time[0] + time[1]
    return int("" + time[0] + time[1])

if __name__ == "__main__":
    transport_dir = directories['IPHONE_DIR']

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
        # print sch

    print station_schedule

    station_schedule = sorted(station_schedule, key=time_key)

    print station_schedule