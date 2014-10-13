#!/usr/bin/env python

__author__ = 'Ilya Fateev'

# import urllib2
import hashlib
import os
import logging

from parser_schedule import ScheduleParser
from parser_transport import TransportParser
import parser_utils


if __name__ == "__main__":

    directories = {
        "LOGS_DIR":  "logs/",
        "SCHEDULES_DIR": "json/",
        "JSON_DIR": "json/"
    }

    for dir_alias, dir_name in directories.iteritems():
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            logging.info("Parsing transport id's started.")

    logging.basicConfig(
        filename=directories["LOGS_DIR"] + 'example.log',
        level=logging.DEBUG,
        format='%(levelname)s:%(asctime)s:%(message)s',
        datefmt='%d-%m-%Y %H:%M:%S'
    )

    """
    Downloading, parsing, getting list of buses and trolleys, which stores in
    TransportParser.bus_dictionary
    """

    logging.info("Parsing transport id's started.")

    transport_parser = TransportParser()
    html = parser_utils.download_page_with_retry_and_encode(
        TransportParser.TRANSPORT_PAGE_URL
    )
    transport_parser.parse_corresponding_html(html)

    logging.info("Parsing transport id's finished.")

    """
    Downloading schedule tables,
    forming json_buses_list structure, that after will be
    dumped in JSON text file.
    """
    logging.info("Parsing transport schedules started.")
    EXAMPLE_OF_HTML_POST_REQUEST = """select+value=&avt=19_r&trol=%23"""

    json_buses_list = []
    stations_set = set()

    for bus_id, bus_name in TransportParser.bus_dictionary.iteritems():

        logging.info("Parsing schedule for bus with id: %s", bus_id)
        print "Current bus_id is:", bus_id

        data = ScheduleParser.get_post_data_for_schedule_for_given_id(bus_id)
        html = parser_utils.download_page_with_retry_and_encode(
            ScheduleParser.COMMON_TRANSPORT_SCHEDULE_URL,
            data
        )
        ScheduleParser.parse_corresponding_html(html)

        """
        Filling structures for stations
        """
        for station in ScheduleParser.stations_list:
            stations_set.add(station.encode('utf-8'))
        stations_list = [
            x.encode('utf-8') for x in ScheduleParser.stations_list
        ]
        stations_list = [
            {
                "name": x,
                "id": hashlib.md5(x).hexdigest()[16:]
            }
            for x in stations_list
        ]

        """
        Filling particular bus structure
        """
        json_bus_object = {
            'type': 'bus',
            'stations': stations_list,
            'schedule': ScheduleParser.schedule_table,
            'weekend': ScheduleParser._with_weekends,
            'workdays': bus_name[1],
            'id': bus_id,
            'name': bus_name[0]
        }
        if ScheduleParser._with_weekends:
            WORKDAY_URL = 0
            WEEKEND_URL = 1
            weekend_schedule_url = ScheduleParser.workdays_weekends_links[
                WEEKEND_URL
            ]
            html = parser_utils.download_page_with_retry_and_encode(
                weekend_schedule_url
            )
            ScheduleParser.parse_corresponding_html(html)
            json_bus_object['scheduleWeekend'] = ScheduleParser.schedule_table
        json_buses_list.append(json_bus_object)
        ScheduleParser.reset_parser()

    json_text = parser_utils.json_pretty_dumps(json_buses_list)

    # JSON writing buses objs
    json_file = open(directories["JSON_DIR"] + "buses.json", 'w')
    json_file.write(json_text)
    json_file.close()
