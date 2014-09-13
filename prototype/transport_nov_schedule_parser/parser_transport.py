#!/usr/bin/env python

__author__ = 'Ilya Fateev'

from HTMLParser import HTMLParser
import urllib2


class TransportParser(HTMLParser):

    bus_number_list = []
    trolley_number_list = []
    bus_descriptor_list = []
    trolley_descriptor_list = []
    bus_dictionary = {}
    trolley_dictionary = {}

    _transport_bus_started = False
    _transport_trolley_started = False
    _current_bus_number = 0
    _current_trolley_number = 0

    TRANSPORT_PAGE_URL = "http://transport.nov.ru/urban_trans/1"

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
                    if attr[0] == "value": #and attr[1] != "#":
                        TransportParser.bus_descriptor_list.append(attr[1])
            if TransportParser._transport_trolley_started:
                for attr in attrs:
                    if attr[0] == "value":# and attr[1] != "#":
                        TransportParser.trolley_descriptor_list.append(attr[1])


    def handle_endtag(self, tag):
        if "select" == tag:
            if TransportParser._transport_bus_started:
                TransportParser._transport_bus_started = False
            if TransportParser._transport_trolley_started:
                TransportParser._transport_trolley_started = False

    def handle_data(self, data):
        if data != u"\r\n  " and data != u"\r\n":
            if TransportParser._transport_bus_started:
                TransportParser.bus_number_list.append(data)
            if TransportParser._transport_trolley_started:
                TransportParser.trolley_number_list.append(data)

    @staticmethod
    def parse_corresponding_html(html_page):
        parser = TransportParser()
        parser.feed(html_page)

        i = 0
        TransportParser.bus_dictionary = {}
        for bus_number in TransportParser.bus_number_list:
            if TransportParser.bus_descriptor_list[i] != "#":
                TransportParser.bus_dictionary[TransportParser.bus_descriptor_list[i]] = bus_number
            i += 1

        i = 0
        TransportParser.trolley_dictionary = {}
        for trolley_number in TransportParser.trolley_number_list:
            if TransportParser.trolley_descriptor_list[i] != "#":
                TransportParser.trolley_dictionary[TransportParser.trolley_descriptor_list[i]] = trolley_number
            i += 1

    @staticmethod
    def reset_parser():
        TransportParser.bus_number_list = []
        TransportParser.trolley_number_list = []
        TransportParser.bus_descriptor_list = []
        TransportParser.trolley_descriptor_list = []
        TransportParser._transport_bus_started = False
        TransportParser._transport_trolley_started = False
        TransportParser._current_bus = []
        TransportParser._current_bus_counter = 0

if __name__ == "__main__":
    response = urllib2.urlopen(TransportParser.TRANSPORT_PAGE_URL)
    html = response.read().decode('windows-1251')

    TransportParser.parse_corresponding_html(html)

    for bus_id, bus_name in TransportParser.bus_dictionary.iteritems():
        print bus_id, bus_name
    print ""

    for trolley_id, trolley_name in TransportParser.trolley_dictionary.iteritems():
        print trolley_id, trolley_name

