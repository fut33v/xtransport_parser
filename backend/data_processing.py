#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = 'Ilya Fateev'

from os import listdir
from os.path import isfile, join
import os

import parser_utils

JSON_REPLACE = "json/replace.json"
TRANSPORT_DIR = 'json/transport/'
IPHONE_DIR = "json/iphone/"


def do_replace(transport, replace):
    if 'stations_workdays' in transport:
        for i in range(len(transport['stations_workdays'])):
            station = transport['stations_workdays'][i]['name']
            for what in replace:
                if what['what'] == station:
                    print "\t", station, "=>", what['replace']
                    transport['stations_workdays'][i]['name'] = (
                        what['replace']
                    )
    if 'stations_weekend' in transport:
        for i in range(len(transport['stations_weekend'])):
            station = transport['stations_weekend'][i]['name']
            for what in replace:
                if what['what'] == station:
                    print "\t", station, "=>", what['replace']
                    transport['stations_weekend'][i]['name'] = (
                        what['replace']
                    )


if __name__ == "__main__":
    onlyfiles = [
        f for f in listdir(TRANSPORT_DIR) if isfile(join(TRANSPORT_DIR, f))
    ]
    replace = parser_utils.load_json_file(JSON_REPLACE)
    if 'replace' in replace:
        replace = replace["replace"]
    for filename in onlyfiles:
        filename = TRANSPORT_DIR + filename
        print filename
        transport = parser_utils.load_json_file(filename)

        print transport['name']

        # if transport['id'] == "bus_27a":
        #     if 'stations_workdays' in transport:
        #         for station in transport['stations_workdays']:
        #             print station['name'] + "|"
        #     if 'stations_weekend' in transport:
        #         for station in transport['stations_weekend']:
        #             print station['name'] + "|"

        do_replace(transport, replace)

        if 'stations_weekend' in transport and 'stations_workdays' in transport:
            if transport['stations_weekend'] == transport['stations_workdays']:
                transport['stations'] = transport['stations_weekend']
                transport.pop('stations_workdays')
                transport.pop('stations_weekend')
                print "stations is the same"
        print "##############################"

        # serializating web version JSON
        parser_utils.save_json_file(filename, transport)

        # transpose schedules, serializating phone version JSON
        if 'schedule_workdays' in transport:
            schedule = [list(i) for i in zip(*transport['schedule_workdays'])]
            transport['schedule_workdays'] = schedule
        if 'schedule_weekend' in transport:
            schedule = [list(i) for i in zip(*transport['schedule_weekend'])]
            transport['schedule_weekend'] = schedule

        if not os.path.exists(IPHONE_DIR):
            os.makedirs(IPHONE_DIR)
        filename = IPHONE_DIR + transport['id'] + ".json"
        parser_utils.save_json_file(filename, transport)
