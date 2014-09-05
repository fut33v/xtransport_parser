import urllib2
import urllib
from HTMLParser import HTMLParser

class TransportParser(HTMLParser):
	_stations_counter = 0
	_schedule_table_started = False
	_station_name_started = False 
	_stations_list = []
	_schedule_table = []
	_current_bus = []
	_current_bus_counter = 0
	
	def handle_starttag(self, tag, attrs):
		if "table" == tag:
			for attr in attrs:
				if attr == ('class', 't'):
					print "Found schedule table"
					TransportParser._schedule_table_started = True
		for attr in attrs:
			if attr == ('class', 'zagl'):
				TransportParser._stations_counter += 1
				TransportParser._station_name_started = True

	def handle_endtag(self, tag):	
		if "table" == tag:	
			if TransportParser._schedule_table_started:
				TransportParser._schedule_table_started = False
		if "td" == tag:
			if TransportParser._station_name_started:
				TransportParser._station_name_started = False

	def handle_data(self, data):
		if TransportParser._schedule_table_started and not TransportParser._station_name_started:
			if TransportParser._current_bus_counter < TransportParser._stations_counter:	
				TransportParser._current_bus.append(data)			
				TransportParser._current_bus_counter += 1
			if TransportParser._current_bus_counter == TransportParser._stations_counter:
				TransportParser._schedule_table.append(TransportParser._current_bus)
				TransportParser._current_bus_counter = 0
				TransportParser._current_bus = []
				
			print data,
		if TransportParser._station_name_started:
			TransportParser._stations_list.append(data)
			# print data
			
		


url = "http://transport.nov.ru/urban_trans/1"
"""select+value=&avt=19_r&trol=%23"""
values = {'select+value': {'avt': '19_r', 'trol': '%23'}}
data = urllib.urlencode(values)

data = "select+value=&avt=19_r&trol=%23"
request = urllib2.Request(url, data)
response = urllib2.urlopen(request)
html = response.read().decode('windows-1251')

parser = TransportParser()
parser.feed(html)

print "\nStations names:"
for station_name in TransportParser._stations_list:
	print station_name

for bus in TransportParser._schedule_table:
	for time in bus:
		print time,
	print ""
