#!/usr/bin/env python

__author__ = 'Ilya Fateev'

from HTMLParser import HTMLParser
import string


class ScheduleParser(HTMLParser):

    @staticmethod
    def parse_html(html_page):
        ScheduleParser._reset_parser()
        parser = ScheduleParser()
        parser.feed(html_page)

        schedule_dict = {
            'schedule_table': parser.schedule_table,
            'weekend': parser._with_weekends,
            'everyday': False,
            'stations_list': parser.stations_list
        }

        # Case of '7a' bus which works every day
        if len(parser.workdays_weekends_links) == 0:
            schedule_dict["everyday"] = True

        if len(parser.workdays_weekends_links) > 1:
            schedule_dict["weekend_link"] = parser.workdays_weekends_links[1]

        return schedule_dict

    COMMON_TRANSPORT_SCHEDULE_URL = "http://transport.nov.ru/urban_trans/1/"
    EXAMPLE_OF_HTML_POST_REQUEST_FOR_19 = """select+value=&avt=19_r&trol=%23"""

    stations_number = 0
    schedule_table = []
    schedule_table_by_station = []
    stations_list = []

    _station_name_started = False
    _schedule_table_started = False
    _current_bus = []
    _current_bus_counter = 0

    _with_weekends = False
    workdays_weekends_links = []
    _weekends_schedule_link = ""

    def handle_starttag(self, tag, attrs):
        if "table" == tag:
            for attr in attrs:
                if attr == ('class', 't'):
                    ScheduleParser._schedule_table_started = True
        for attr in attrs:
            if attr == ('class', 'zagl'):
                ScheduleParser.stations_number += 1
                ScheduleParser._station_name_started = True
        if "a" == tag:
            for attr in attrs:
                if attr[0] == 'href':
                    # print attr[1]
                    if string.find(attr[1], "?mar=") == 0:
                        ScheduleParser.workdays_weekends_links.append(
                            ScheduleParser.COMMON_TRANSPORT_SCHEDULE_URL +
                            attr[1]
                        )
                        ScheduleParser._with_weekends = True
                        if len(ScheduleParser.workdays_weekends_links) == 2:
                            ScheduleParser._weekends_schedule_link = (
                                ScheduleParser.COMMON_TRANSPORT_SCHEDULE_URL +
                                ScheduleParser.workdays_weekends_links[1]
                            )

    def handle_endtag(self, tag):
        if "table" == tag:
            if ScheduleParser._schedule_table_started:
                ScheduleParser._schedule_table_started = False
        if "td" == tag:
            if ScheduleParser._station_name_started:
                ScheduleParser._station_name_started = False

    def handle_data(self, data):
        if (ScheduleParser._schedule_table_started and
                not ScheduleParser._station_name_started):
            if (ScheduleParser._current_bus_counter <
                    ScheduleParser.stations_number):
                ScheduleParser._current_bus.append(data)
                ScheduleParser._current_bus_counter += 1
            if (ScheduleParser._current_bus_counter ==
                    ScheduleParser.stations_number):
                ScheduleParser.schedule_table.append(
                    ScheduleParser._current_bus
                )
                ScheduleParser._current_bus_counter = 0
                ScheduleParser._current_bus = []
        if ScheduleParser._station_name_started:
            ScheduleParser.stations_list.append(unicode(data))

    @staticmethod
    def _reset_parser():
        ScheduleParser.stations_number = 0
        ScheduleParser.schedule_table = []
        ScheduleParser.stations_list = []
        ScheduleParser._schedule_table_started = False
        ScheduleParser._station_name_started = False
        ScheduleParser._current_bus = []
        ScheduleParser._current_bus_counter = 0
        ScheduleParser.weekend_list = []
        ScheduleParser._with_weekends = False
        ScheduleParser.workdays_weekends_links = []
        ScheduleParser._weekends_schedule_link = ""
