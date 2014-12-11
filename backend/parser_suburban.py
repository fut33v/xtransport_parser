#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Ilya Fateev'

from HTMLParser import HTMLParser

from parser_utils import no_whitespaces
# import string


class SuburbanParser(HTMLParser):
    SUBURBAN_TRANSPORT_PAGE_URL = "http://transport.nov.ru/suburban_trans/3"
    COLUMNS_NUMBER = 9
    COLUMNS_HEADERS = {
        u"№": 'number',
        u"направление": 'station',
        u"отправ.савтовокзалав.новгорода": 'from_city',
        u"отправ.скон.пункта": 'to_city',
        u"времявпути": 'time',
        u"расст-евкм.": 'distance',
        u"стоимостьпроездаруб.": 'cost'
    }

    def __init__(self):
        HTMLParser.__init__(self)
        self._schedule_table_started = False
        self._table_header_started = False
        self._column_counter = 0
        self._current_bus_counter = 0
        self._table_header = []
        self._table_header_dict = {}
        self._current_bus = []
        self._current_bus_dict = {}
        self._result = []

    @classmethod
    def parse_html(cls, html_page):
        parser = SuburbanParser()
        parser.feed(html_page)
        h = parser._table_header_dict
        suburban_buses = []
        for row in parser._result:
            bus = {}
            for column_header, eng_key in cls.COLUMNS_HEADERS.iteritems():
                bus[eng_key] = row[h[eng_key]]
            suburban_buses.append(bus)
            # print bus
        return suburban_buses

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            for attr in attrs:
                if attr == ('class', 't'):
                    self._schedule_table_started = True
        if tag == 'td' and self._schedule_table_started is True:
            for attr in attrs:
                if attr == ('class', 'zagl'):
                    self._table_header_started = True
                    self._column_counter += 1
                if attr == ('class', 'nonzagl1'):
                    self._table_header_started = False

    def handle_endtag(self, tag):
        if tag == 'table':
            if self._schedule_table_started is True:
                self._schedule_table_started = False

    def handle_data(self, data):
        if self._schedule_table_started:
            if self._table_header_started:
                d = no_whitespaces(unicode(data)).lower()
                self._table_header.append(d)
                if d in SuburbanParser.COLUMNS_HEADERS:
                    self._table_header_dict[
                        SuburbanParser.COLUMNS_HEADERS[d]
                    ] = (
                        self._column_counter - 1
                    )
            elif self._current_bus_counter < self._column_counter:
                self._current_bus.append(unicode(data))
                self._current_bus_counter += 1
                if self._current_bus_counter == self._column_counter:
                    self._result.append(self._current_bus)
                    self._current_bus_counter = 0
                    self._current_bus = []


if __name__ == "__main__":
    from parser_utils import download_page
    html = download_page(SuburbanParser.SUBURBAN_TRANSPORT_PAGE_URL)
    SuburbanParser.parse_html(html)
