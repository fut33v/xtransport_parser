#!/usr/bin/env python

__author__ = 'Ilya Fateev'

import os
import logging

from parser_transport import TransportParser
from parsing_parts import parse_schedules_bus
from parsing_parts import parse_schedules_trolley
from parsing_parts import get_transport_json
from parsing_parts import parse_schedules_suburban


import parser_utils

MIX_LIST = [
    'bus_1cr',
    'bus_1418'
]

if __name__ == "__main__":

    directories = {
        "LOGS_DIR":  "logs/",
        "JSON_DIR": "json/",
        "BUSES_DIR": "json/transport/",
        "TROLLEYS_DIR": "json/transport/"
        # "BUSES_DIR": "json/buses/",
        # "TROLLEYS_DIR": "json/trolleys/"
    }

    for dir_alias, dir_name in directories.iteritems():
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    logging.basicConfig(
        filename=directories["LOGS_DIR"] + 'example.log',
        level=logging.DEBUG,
        format='%(levelname)s:%(asctime)s:%(message)s',
        datefmt='%d-%m-%Y %H:%M:%S'
    )

    logging.info("Parsing transport id's started.")
    transport_parser = TransportParser()
    html = parser_utils.download_page(
        TransportParser.TRANSPORT_PAGE_URL
    )

    transport = transport_parser.parse_html(html)
    logging.info("Parsing transport id's finished.")

    # logging.info("Parsing buses schedules started.")
    # parse_schedules_bus(transport["bus_list"])

    # logging.info("Parsing trolleys schedules started.")
    # parse_schedules_trolley(transport["trolley_list"])

    parse_schedules_suburban()

    buses_trolleys = transport["trolley_list"] + transport["bus_list"]

    regular_buses = [
        elem for elem in transport["bus_list"] if elem['id'] not in MIX_LIST
    ]

    mixed_buses = [
        elem for elem in transport["bus_list"] if elem['id'] in MIX_LIST
    ]

    buses = get_transport_json(regular_buses, 'bus')
    trolleys = get_transport_json(transport["trolley_list"], 'trolley')
    mixed = get_transport_json(mixed_buses, 'mixed')

    # for bus in regular_buses:
    #     print bus['id']
    # for bus in mixed_buses:
    #     print bus['id']

    transport_dict = {
        'buses': buses,
        'trolleys': trolleys,
        'mixed': mixed
    }

    parser_utils.save_json_file(
        directories["JSON_DIR"] + "transport.json",
        transport_dict
    )
