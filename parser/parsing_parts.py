#!/usr/bin/env python

__author__ = 'Ilya Fateev'

from parser_schedule import ScheduleParser
from parser_transport import TransportParser
from parser_suburban import SuburbanParser
import parser_configs
import parser_utils
from parser_utils import in_dict
from parser_utils import no_whitespaces

from unidecode import unidecode

import logging
import re


MIX_LIST = [
    'bus_1cr',
    'bus_1418'
]


def parse_schedules_bus(bus_list):
    for bus in bus_list:

        logging.info("Parsing schedule for bus with id: %s", bus["id"])
        print "Current bus_id is:", bus["id"]

        html = parser_utils.download_page(
            TransportParser.TRANSPORT_PAGE_URL,
            bus["post_data"]
        )
        schedule = ScheduleParser.parse_html(html)

        json_bus_object = {
            'type': 'bus',
            'id': bus["id"],
            'name': bus["name"],
            'everyday': False
        }

        if bus['id'] in MIX_LIST:
            type_ = 'mixed'
        else:
            type_ = 'bus'

        json_bus_object['type'] = type_

        # Case when bus have only weekend schedule
        if bus['weekend'] is True:
            json_bus_object['workdays'] = False
            json_bus_object['weekend'] = True
            json_bus_object['schedule_weekend'] = schedule['schedule_table']
            json_bus_object['stations_weekend'] = schedule['stations_list']

        # Case when bus have workdays, and maybe weekend schedule
        else:
            # Case of '7a' bus (everyday)
            # @TODO: could be others buses like this
            if schedule['everyday'] is True:
                json_bus_object['everyday'] = True
                json_bus_object['workdays'] = True
                json_bus_object['weekend'] = True
                json_bus_object['schedule_everyday'] = (
                    schedule['schedule_table']
                )
                json_bus_object['stations_everyday'] = schedule['stations_list']
            else:
                json_bus_object['workdays'] = True
                json_bus_object['weekend'] = False
                json_bus_object['schedule_workdays'] = (
                    schedule['schedule_table']
                )
                json_bus_object['stations_workdays'] = schedule['stations_list']
                if schedule['weekend'] is True:
                    json_bus_object['weekend'] = True
                    html = parser_utils.download_page(
                        schedule['weekend_link']
                    )
                    schedule_weekend = ScheduleParser.parse_html(html)
                    json_bus_object['schedule_weekend'] = (
                        schedule_weekend['schedule_table']
                    )
                    json_bus_object['stations_weekend'] = (
                        schedule_weekend['stations_list']
                    )
        parser_utils.save_json_file(
            parser_configs.directories["BUSES_DIR"] + bus["id"] + ".json",
            json_bus_object
        )


def parse_schedules_trolley(trolley_list):
    for trolley in trolley_list:
        logging.info("Parsing schedule for trolley with id: %s", trolley["id"])
        print "Current trolley_id is:", trolley["id"]

        html = parser_utils.download_page(
            TransportParser.TRANSPORT_PAGE_URL,
            trolley["post_data"]
        )
        schedule = ScheduleParser.parse_html(html)

        json_trolley_object = {
            'type': 'trolley',
            'id': trolley["id"],
            'name': trolley["name"],
            'workdays': False,
            'weekend': False,
            'everyday': False
        }

        # in trolley case ['workdays'] always True
        if trolley['workdays'] is True:
            # case, when trolley works only on workdays
            if schedule['workdays'] is True:
                print "Workdays only"
                json_trolley_object['workdays'] = True
                json_trolley_object['schedule_workdays'] = (
                    schedule['schedule_table']
                )
                json_trolley_object['stations_workdays'] = (
                    schedule['stations_list']
                )
            # regular case, when trolley works both on workdays and weekend
            else:
                json_trolley_object['workdays'] = True
                json_trolley_object['schedule_workdays'] = (
                    schedule['schedule_table']
                )
                json_trolley_object['stations_workdays'] = (
                    schedule['stations_list']
                )
                if schedule['weekend'] is True:
                    json_trolley_object['weekend'] = True
                    html = parser_utils.download_page(
                        schedule['weekend_link']
                    )
                    schedule_weekend = ScheduleParser.parse_html(html)
                    json_trolley_object['schedule_weekend'] = (
                        schedule_weekend['schedule_table']
                    )
                    json_trolley_object['stations_weekend'] = (
                        schedule_weekend['stations_list']
                    )

        parser_utils.save_json_file(
            (parser_configs.directories["TROLLEYS_DIR"] +
                trolley["id"] + ".json"),
            json_trolley_object
        )


def get_transport_json(transport_list, type_):
    transport = []
    for tr in transport_list:
        transport.append(
            {
                'id': tr['id'],
                'name': tr['name'],
                'type': type_
            }
        )
    return transport


def parse_schedules_suburban():
    html = parser_utils.download_page(
        SuburbanParser.SUBURBAN_TRANSPORT_PAGE_URL
    )
    suburban_buses = SuburbanParser.parse_html(html)
    for bus in suburban_buses:
        from_city = in_dict(bus, 'from_city')
        if from_city:
            from_city = no_whitespaces(from_city)

            regex_one_day = r"[0-9]{1,2}-[0-9]{1,2}\([0-9]{1}\)"
            regex_range_of_days = r"[0-9]{1,2}-[0-9]{1,2}\([0-9]{1}-[0-9]{1}\)"
            regex_set_of_days = r"[0-9]{1,2}-[0-9]{1,2}\([0-9]{1},[0-9]{1}\)"
            regex_normal_end = r"[0-9]{1,2}-[0-9]{1,2}$"
            regex_normal_middle = r"([0-9]{1,2}-[0-9]{1,2}),"

            print "------------------------------"
            print from_city
            print "one-day", re.findall(regex_one_day, from_city)
            print "range of days", re.findall(regex_range_of_days, from_city)
            print "set of days", re.findall(regex_set_of_days, from_city)
            print "normal", re.findall(regex_normal_end, from_city)
            print "normal", re.findall(regex_normal_middle, from_city)
            print "------------------------------"

        bus_id = in_dict(bus, 'number')
        bus_id = no_whitespaces(bus_id)
        bus_id = bus_id.replace(',', '_')
        bus_id = unidecode(bus_id)
        bus_id = "sub_" + bus_id
        print bus_id
        bus['id'] = bus_id
    parser_utils.save_json_file(
        (parser_configs.directories["JSON_DIR"] +
            "suburban_transport.json"),
        suburban_buses
    )
