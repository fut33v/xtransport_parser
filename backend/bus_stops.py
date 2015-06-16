__author__ = 'fat32'

import json
from os import listdir
from os.path import isfile, join

from unidecode import unidecode

from parser_configs import directories
from parser_configs import files
import parser_utils

def clear_station_name(name):
    name = parser_utils.replace_whitespaces(name)
    name = parser_utils.no_punctuation(name)
    name = name.lower()
    name = unidecode(name)
    # replacing the result of transliterating soft sign
    name = name.replace('\'', '')
    return name


if __name__ == "__main__":
    stations_dir = directories['STATIONS_DIR']
    parser_utils.create_dirs([stations_dir])

    transport_dir = directories['IPHONE_DIR']
    only_files = [
        f for f in listdir(transport_dir) if isfile(join(transport_dir, f))
    ]

    with open(directories['RESOURCES'] + files['EQUAL_STATIONS']) as f:
        equal_stations_raw = f.readlines()
    equal_stations = []
    for entry in equal_stations_raw:
        threesome = entry.split(':')
        equal_stations.append(threesome)

    equal_stations_dict = {}
    for e in equal_stations:
        equal_stations_dict[clear_station_name(e[0])] = unicode(e[2])
        equal_stations_dict[clear_station_name(e[0])] = unicode(e[2])

    print equal_stations
    print equal_stations_dict
    # exit(0)

    stations = {}
    stations_dict = {}
    stations_list = []
    test_stations_dict = {}

    for filename in only_files:
        transport_file = transport_dir + filename
        transport_file = open(transport_file).read()
        transport = json.loads(transport_file)
        if 'stations' in transport:
            i = 0
            for station in transport['stations']:
                station_name = station['name']
                if station_name in equal_stations_dict:
                    station_name = equal_stations_dict[station_name]
                    print "bismillahullialla"

                station_name = clear_station_name(station_name)

                if station_name not in stations_dict:
                    station_new = {
                        'name': station_name
                    }

                    stations_list.append(station_name)
                    test_stations_dict[station_name] = [transport['name']]
                else:
                    station_new = stations_dict[station_name]

                    test_stations_dict[station_name].append(transport['name'])

                """
                if 'schedule_workdays' in transport:
                    schedule = transport['schedule_workdays'][i]
                    transport_id = transport['id']

                    print i, transport_id, station_name, schedule

                    if 'schedule_workdays' not in station_new:
                        station_new['schedule_workdays'] = []
                    schedule_new = {
                        'transport_id': transport_id,
                        'schedule': schedule
                    }
                    station_new['schedule_workdays'].append(schedule_new)

                stations_dict[station_name] = station_new
                """
                i += 1

    # print test_stations_dict

    file = open("stations.txt", 'w')
    for station in stations_list:
        file.write("%s\n" % station)

    # print parser_utils.json_pretty_dumps(stations_dict)
