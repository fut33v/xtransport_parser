__author__ = 'Ilya Fateev'
import urllib2
import urllib

from parser_schedule import ScheduleParser

if __name__ == "__main__":
    url = "http://transport.nov.ru/urban_trans/1"
    """select+value=&avt=19_r&trol=%23"""
    values = {'select+value': {'avt': '19_r', 'trol': '%23'}}
    data = urllib.urlencode(values)

    data = "select+value=&avt=19_r&trol=%23"
    request = urllib2.Request(url, data)
    response = urllib2.urlopen(request)
    html = response.read().decode('windows-1251')

    parser = ScheduleParser()
    parser.feed(html)

    print "\nStations names:"
    for station_name in ScheduleParser.stations_list:
        print station_name

    for bus in ScheduleParser.schedule_table:
        for time in bus:
            print time,
        print ""
