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

    logging.basicConfig(
        filename='example.log',
        level=logging.DEBUG,
        format='%(levelname)s:%(asctime)s:%(message)s',
        datefmt='%d-%m-%Y %H:%M:%S'
    )

    """
    Getting list of buses and trolleys, which stores in
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
            'bus': True,
            'stations': stations_list,
            'schedule': ScheduleParser.schedule_table,
            'weekend': ScheduleParser._with_weekends,
            'id': bus_id,
            'name': bus_name[0],
            'weekendOnly': bus_name[1]
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
        # print json_bus_object
        json_buses_list.append(json_bus_object)
        ScheduleParser.reset_parser()

    json_text = parser_utils.json_pretty_dumps(json_buses_list)
    # print json_text

    # JSON writing buses objs
    json_file = open("buses.json", 'w')
    json_file.write(json_text)
    json_file.close()

    # JSON dumping stations set
    stations_file = open("stations.json", 'w')
    stations_list = list(stations_set)
    stations_json_array = [
        {
            'name': station,
            'hash': hashlib.md5(station).hexdigest()[16:]
        }
        for station in stations_list
    ]
    stations_json_text = parser_utils.json_pretty_dumps(
        stations_json_array,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    )
    stations_file.write(stations_json_text)
    stations_file.close()

    SCHEDULES_DIR = "schedules"
    if not os.path.exists(SCHEDULES_DIR):
        os.makedirs(SCHEDULES_DIR)
    for bus_js_object in json_buses_list:
        temp = {
            'id': bus_js_object['id'],
            'schedule': bus_js_object['schedule'],
            'stationsNumber': (len(bus_js_object['stations'])),
            'weekend': bus_js_object['weekend']
        }
        print bus_js_object['weekend']
        if bus_js_object['weekend']:
            temp['scheduleWeekend'] = bus_js_object['scheduleWeekend']
            print "With weekend"
        json_text = parser_utils.json_pretty_dumps(temp)

        json_file = open(
            SCHEDULES_DIR +
            "/" +
            bus_js_object['id'].encode('utf-8') +
            ".json", 'w'
        )
        json_file.write(json_text)
        json_file.close()

    # for trolley_id, trolley_name in TransportParser.
    # trolley_dictionary.iteritems():
    #     print trolley_id, trolley_name
