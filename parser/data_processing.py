#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = 'Ilya Fateev'

from os import listdir
from os.path import isfile, join

import parser_utils

JSON_REPLACE = "json/replace.json"


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
    TRANSPORT_DIR = 'json/transport/'
    onlyfiles = [
        f for f in listdir(TRANSPORT_DIR) if isfile(join(TRANSPORT_DIR, f))
    ]
    replace = parser_utils.load_json_file(JSON_REPLACE)
    if 'replace' in replace:
        replace = replace["replace"]
    for filename in onlyfiles:
        filename = TRANSPORT_DIR + filename
        transport = parser_utils.load_json_file(filename)
        # print transport['name']
        if transport['id'] == "bus_27a":
            if 'stations_workdays' in transport:
                for station in transport['stations_workdays']:
                    print station['name'] + "|"
            if 'stations_weekend' in transport:
                for station in transport['stations_weekend']:
                    print station['name'] + "|"

        do_replace(transport, replace)

        if 'stations_weekend' in transport and 'stations_workdays' in transport:
            if transport['stations_weekend'] == transport['stations_workdays']:
                transport['stations'] = transport['stations_weekend']
                print "stations is the same"
        print "##############################"
        parser_utils.save_json_file(filename, transport)
