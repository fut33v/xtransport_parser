#!/usr/bin/env python

__author__ = 'Ilya Fateev'

# import urllib2
import os
import logging

from parser_schedule import ScheduleParser
from parser_transport import TransportParser
import parser_utils

# def encode_stations(stations):
#     return [
#         {"name": x.encode('utf-8')} for x in stations
#     ]

if __name__ == "__main__":

    directories = {
        "LOGS_DIR":  "logs/",
        "JSON_DIR": "json/",
        "BUSES_DIR": "json/buses/",
        "TROLLEYS_DIR": "json/trolleys/"
    }
    """
    Creating dirs for data, if not they not exist.
    """
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

    logging.info("Parsing transport schedules started.")

    for bus in transport["bus_list"]:

        logging.info("Parsing schedule for bus with id: %s", bus["id"])
        print "Current bus_id is:", bus["id"]

        html = parser_utils.download_page(
            TransportParser.TRANSPORT_PAGE_URL,
            bus["post_data"]
        )
        schedule = ScheduleParser.parse_html(html)

        json_bus_object = {
            'type': 'bus',
            # 'stations': schedule['stations_list'],
            'id': bus["id"],
            'name': bus["name"],
            'everyday': False
        }

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
                json_bus_object['schedule_everyday'] = (
                    schedule['schedule_table']
                )
                json_bus_object['stations_everyday'] = schedule['stations_list']
            else:
                json_bus_object['workdays'] = True,
                json_bus_object['weekend'] = False,
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

        parser_utils.save_json_file(
            directories["BUSES_DIR"] + bus["id"] + ".json",
            json_bus_object
        )

    for trolley in transport["trolley_list"]:
        logging.info("Parsing schedule for trolley with id: %s", trolley["id"])
        print "Current trolley_id is:", trolley["id"]

        html = parser_utils.download_page(
            TransportParser.TRANSPORT_PAGE_URL,
            trolley["post_data"]
        )
        schedule = ScheduleParser.parse_html(html)

        json_trolley_object = {
            'type': 'trolley',
            'stations': schedule['stations_list'],
            'id': trolley["id"],
            'name': trolley["name"]
        }
        parser_utils.save_json_file(
            directories["TROLLEYS_DIR"] + trolley["id"] + ".json",
            json_trolley_object
        )
