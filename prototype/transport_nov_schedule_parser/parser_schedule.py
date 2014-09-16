#!/usr/bin/env python

__author__ = 'Ilya Fateev'

from HTMLParser import HTMLParser


class ScheduleParser(HTMLParser):

    stations_number = 0
    schedule_table = []
    schedule_table_by_station = []
    stations_list = []

    _schedule_table_started = False
    _station_name_started = False
    _current_bus = []
    _current_bus_counter = 0

    def handle_starttag(self, tag, attrs):
        if "table" == tag:
            for attr in attrs:
                if attr == ('class', 't'):
                    ScheduleParser._schedule_table_started = True
        for attr in attrs:
            if attr == ('class', 'zagl'):
                ScheduleParser.stations_number += 1
                ScheduleParser._station_name_started = True

    def handle_endtag(self, tag):
        if "table" == tag:
            if ScheduleParser._schedule_table_started:
                ScheduleParser._schedule_table_started = False
        if "td" == tag:
            if ScheduleParser._station_name_started:
                ScheduleParser._station_name_started = False

    def handle_data(self, data):
        if ScheduleParser._schedule_table_started and not ScheduleParser._station_name_started:
            if ScheduleParser._current_bus_counter < ScheduleParser.stations_number:
                ScheduleParser._current_bus.append(data)
                ScheduleParser._current_bus_counter += 1
            if ScheduleParser._current_bus_counter == ScheduleParser.stations_number:
                ScheduleParser.schedule_table.append(ScheduleParser._current_bus)
                ScheduleParser._current_bus_counter = 0
                ScheduleParser._current_bus = []
        if ScheduleParser._station_name_started:
            ScheduleParser.stations_list.append(data)
    
    @staticmethod
    def reset_parser():
        ScheduleParser.stations_number = 0
        ScheduleParser.schedule_table = []
        ScheduleParser.stations_list = []
        ScheduleParser._schedule_table_started = False
        ScheduleParser._station_name_started = False
        ScheduleParser._current_bus = []
        ScheduleParser._current_bus_counter = 0
