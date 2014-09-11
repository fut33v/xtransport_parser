#!/usr/bin/env python

__author__ = 'Ilya Fateev'
import urllib2
import urllib
import json

from parser_schedule import ScheduleParser
from parser_transport import TransportParser


if __name__ == "__main__":
   
    transport_parser = TransportParser() 

    response = urllib2.urlopen(TransportParser.TRANSPORT_PAGE_URL)
    html = response.read().decode('windows-1251')
    transport_parser.parse_corresponding_html(html)

    schedule_parser = ScheduleParser()
    common_transport_schedule_url = "http://transport.nov.ru/urban_trans/1"
    example_of_html_post_request = """select+value=&avt=19_r&trol=%23"""
    
    bus_json_objects_list = []
    counter = 0
    for bus_id, bus_name in TransportParser.bus_dictionary.iteritems():
        print "Current bus_id is:", bus_id 
        data = "select+value=&" + "avt=" + bus_id + "&trol=%23"
        request = urllib2.Request(common_transport_schedule_url, data)
        response = urllib2.urlopen(request)
        html = response.read().decode('windows-1251')
        schedule_parser.feed(html)

        # print "\nStations names:"
        # for station_name in ScheduleParser.stations_list:
        #     print station_name

        # for bus in ScheduleParser.schedule_table:
        #     for time in bus:
        #         print time,

        stations_list = [x.encode('utf-8') for x in ScheduleParser.stations_list]
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
    
    json_text = json.dumps(bus_json_objects_list, sort_keys=True, indent=4, separators=(',', ': '))        
    print json_text
    json_file = open("out.json", 'w')
    json_file.write(json_text)
    json_file.close()

    
    # for trolley_id, trolley_name in TransportParser.trolley_dictionary.iteritems():
    #     print trolley_id, trolley_name



