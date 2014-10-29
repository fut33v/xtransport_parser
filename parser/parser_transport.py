#!/usr/bin/env python

__author__ = 'Ilya Fateev'

from HTMLParser import HTMLParser
import urllib2
import string


class TransportParser(HTMLParser):

    _bus_number_list = []
    _trolley_number_list = []
    _bus_descriptor_list = []
    _trolley_descriptor_list = []

    _transport_bus_started = False
    _transport_trolley_started = False
    _current_bus_number = 0
    _current_trolley_number = 0

    TRANSPORT_PAGE_URL = "http://transport.nov.ru/urban_trans/1"

    @staticmethod
    def parse_html(html_page):
        TransportParser._reset_parser()
        parser = TransportParser()
        parser.feed(html_page)

        print parser._bus_descriptor_list, parser._bus_number_list

        i = 0
        TransportParser.bus_dictionary = {}
        bus_list = []
        for bus_number in TransportParser._bus_number_list:
            print i, ')', bus_number, TransportParser._bus_descriptor_list[i]
            if TransportParser._bus_descriptor_list[i] != '#':
                bus_id = string.split(
                    TransportParser._bus_descriptor_list[i], '_'
                )
                weekend = TransportParser._check_weekend(bus_id)
                workdays = TransportParser._check_workdays(bus_id)
                bus_list.append(
                    {
                        "id": 'bus_' + bus_id[0],
                        "name": bus_number,
                        "post_data": (
                            TransportParser._get_post_data_bus(
                                TransportParser._bus_descriptor_list[i]
                            )
                        ),
                        "workdays": workdays,
                        "weekend": weekend
                    }
                )
            i += 1

        i = 0
        trolley_list = []
        for trolley_number in TransportParser._trolley_number_list:
            if TransportParser._trolley_descriptor_list[i] != "#":
                trolley_id = string.split(
                    TransportParser._trolley_descriptor_list[i], '_'
                )
                weekend = TransportParser._check_weekend(trolley_id)
                workdays = TransportParser._check_workdays(trolley_id)
                trolley_list.append(
                    {
                        "id": 'trolley_' + trolley_id[0][:-1],
                        "name": trolley_number,
                        "post_data": (
                            TransportParser._get_post_data_trolley(
                                TransportParser._trolley_descriptor_list[i]
                            )
                        ),
                        "workdays": workdays,
                        "weekend": weekend,
                    }
                )
            i += 1
        return {
            'trolley_list': trolley_list,
            'bus_list': bus_list
        }

    def handle_starttag(self, tag, attrs):
        if "select" == tag:
            for attr in attrs:
                if attr == ('name', 'avt'):
                    TransportParser._transport_bus_started = True
            for attr in attrs:
                if attr == ('name', 'trol'):
                    TransportParser._transport_trolley_started = True
        if "option" == tag:
            if TransportParser._transport_bus_started:
                for attr in attrs:
                    if attr[0] == "value":  # and attr[1] != "#":
                        TransportParser._bus_descriptor_list.append(attr[1])
            if TransportParser._transport_trolley_started:
                for attr in attrs:
                    if attr[0] == "value":  # and attr[1] != "#":
                        TransportParser._trolley_descriptor_list.append(attr[1])

    def handle_endtag(self, tag):
        if "select" == tag:
            if TransportParser._transport_bus_started:
                TransportParser._transport_bus_started = False
            if TransportParser._transport_trolley_started:
                TransportParser._transport_trolley_started = False

    def handle_data(self, data):
        # if data != u"\r\n  " and data != u"\r\n" and data != u"\r\n\r\n":
        if self._check_not_rn(data):
            if TransportParser._transport_bus_started:
                TransportParser._bus_number_list.append(data)
            if TransportParser._transport_trolley_started:
                TransportParser._trolley_number_list.append(data)

    @staticmethod
    def _check_not_rn(data):
        if '\r' in data or '\n' in data:
            return False
        else:
            return True

    @staticmethod
    def _check_weekend(transport_id):
        weekend = False
        if len(transport_id) > 1:
            if transport_id[1] == u'v':
                weekend = True
        return weekend

    @staticmethod
    def _check_workdays(transport_id):
        workdays = False
        if len(transport_id) > 1:
            if transport_id[1] == u'r':
                workdays = True
        return workdays

    @staticmethod
    def _get_post_data_bus(bus_id):
        return "select+value=&" + "avt=" + bus_id + "&trol=%23"

    @staticmethod
    def _get_post_data_trolley(trolley_id):
        return "select+value=&" + "trol=" + trolley_id

    @classmethod
    def _reset_parser(cls):
        cls._bus_number_list = []
        cls._trolley_number_list = []
        cls._bus_descriptor_list = []
        cls._trolley_descriptor_list = []
        cls._transport_bus_started = False
        cls._transport_trolley_started = False
        cls._current_bus = []
        cls._current_bus_counter = 0

if __name__ == "__main__":
    import pprint

    response = urllib2.urlopen(TransportParser.TRANSPORT_PAGE_URL)
    html = response.read().decode('windows-1251')

    transport = TransportParser.parse_html(html)
    pprint.pprint(transport, width=1)
    # print transport
    # for bus in transport['bus_list']:
    #     print bus

    # for trolley in transport['trolley_list']:
    #     print trolley
