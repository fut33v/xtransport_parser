#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = 'Ilya Fateev'

from os import listdir
from os.path import isfile, join

import parser_utils

JSON_REPLACE = "json/replace.json"

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
        if 'stations_weekend' in transport and 'stations_workdays' in transport:
            if (len(transport['stations_weekend']) ==
                    len(transport['stations_workdays'])):

                print ">", transport['name'], transport['type']

                for i in range(len(transport['stations_weekend'])):
                    wrkd = transport['stations_workdays'][i]['name']
                    wknd = transport['stations_weekend'][i]['name']
                    if transport['id'] == 'bus_8en':
                        print wrkd, '|', wknd
                    for what in replace:
                        if what['what'] == wrkd:
                            print "\t", wrkd, "=>", what['replace']
                            transport['stations_workdays'][i]['name'] = (
                                what['replace']
                            )
                            # for station in transport['stations_workdays']:
                            #     print station['name']

                        if what['what'] == wknd:
                            print "\t", wknd, "=>", what['replace']
                            transport['stations_weekend'][i]['name'] = (
                                what['replace']
                            )
                            # for station in transport['stations_workdays']:
                            #     print station['name']
                print "####################"
        parser_utils.save_json_file(filename, transport)
