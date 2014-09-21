#!/usr/bin/env python

__author__ = 'Ilya Fateev'
import urllib2
import json
import hashlib
from functools import partial

from parser_schedule import ScheduleParser
from parser_transport import TransportParser


if __name__ == "__main__":

    # Pretty printing json function
    json_pretty_dumps = partial(
        json.dumps,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    )

    transport_parser = TransportParser()

    response = urllib2.urlopen(TransportParser.TRANSPORT_PAGE_URL)
    html = response.read().decode('windows-1251')
    transport_parser.parse_corresponding_html(html)

    schedule_parser = ScheduleParser()
    common_transport_schedule_url = "http://transport.nov.ru/urban_trans/1"
    example_of_html_post_request = """select+value=&avt=19_r&trol=%23"""

    bus_json_objects_list = []
    stations_set = set()
    for bus_id, bus_name in TransportParser.bus_dictionary.iteritems():
        print "Current bus_id is:", bus_id
        data = "select+value=&" + "avt=" + bus_id + "&trol=%23"
        request = urllib2.Request(common_transport_schedule_url, data)
        response = urllib2.urlopen(request)
        html = response.read().decode('windows-1251')
        schedule_parser.feed(html)

        for station in ScheduleParser.stations_list:
            print station
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
        bus_json_objects_list.append(
            {
                'bus': True,
                'stations': stations_list,
                'schedule': ScheduleParser.schedule_table,
                'id': bus_id,
                'name': bus_name
            }
        )
        ScheduleParser.reset_parser()

    json_text = json_pretty_dumps(bus_json_objects_list)
    print json_text

    # JSON writing buses objs
    json_file = open("buses.json", 'w')
    json_file.write(json_text)
    json_file.close()

    # JSON dumping stations list
    stations_file = open("stations.json", 'w')
    stations_list = list(stations_set)
    stations_json_array = [
        {
            'name': station,
            'hash': hashlib.md5(station).hexdigest()[16:]
        }
        for station in stations_list
    ]
    stations_json_text = json_pretty_dumps(
        stations_json_array,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    )
    stations_file.write(stations_json_text)
    stations_file.close()

    for bus_js_object in bus_json_objects_list:
        json_text = json_pretty_dumps(
            {
                'id': bus_js_object['id'],
                'schedule': bus_js_object['schedule'],
                'stationsNumber': (len(bus_js_object['stations']))
            }
        )
        json_file = open(bus_js_object['id'].encode('utf-8') + ".json", 'w')
        json_file.write(json_text)
        json_file.close()

    # for trolley_id, trolley_name in TransportParser.
    # trolley_dictionary.iteritems():
    #     print trolley_id, trolley_name
