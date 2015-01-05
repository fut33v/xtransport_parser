__author__ = 'fat32'

import json
from os import listdir
from os.path import isfile, join

from unidecode import unidecode

from parser_configs import directories
import parser_utils


stations_dir = directories['STATIONS_DIR']
parser_utils.create_dirs([stations_dir])


transport_dir = directories['IPHONE_DIR']
onlyfiles = [
    f for f in listdir(transport_dir) if isfile(join(transport_dir, f))
]

stations = {}
stations_dict = {}

for filename in onlyfiles:
    transport_file = transport_dir + filename
    # print transport_file
    transport_file = open(transport_file).read()
    transport = json.loads(transport_file)
    # print transport
    if 'stations' in transport:
        i = 0
        for station in transport['stations']:
            station_name = station['name']
            station_name = parser_utils.replace_whitespaces(station_name)
            station_name = parser_utils.no_punctuation(station_name)
            station_name = station_name.lower()
            station_name = unidecode(station_name)
            # replacing the result of transliterating soft sign
            station_name = station_name.replace('\'', '')

            if station_name not in stations_dict:
                station_new = {
                    'name': station_name
                }
            else:
                station_new = stations_dict[station_name]

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
                # print station_new
                # print schedule_new
                # print station_name, transport_id, schedule

            stations_dict[station_name] = station_new


            # if station_name in stations:
            #     stations[station_name] += 1
            # else:
            #     stations[station_name] = 1

            i += 1

# print parser_utils.json_pretty_dumps(stations_dict)


i = 0
for station_name, station in stations_dict.iteritems():
    i += 1
# print stations_dict
# print stations
