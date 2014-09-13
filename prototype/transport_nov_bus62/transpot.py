#!/usr/bin/env python
import urllib2
import urllib


url = "http://bus62.ru/novgorod/"
"""select+value=&avt=19_r&trol=%23"""

query = "/php/getVehiclesMarkers.php?rids=6-0,7-0,69-0,70-0,8-0,9-0,71-0,72-0,12-0,13-0,10-0,11-0,73-0,74-0,86-0,87-0,14-0,15-0,75-0,76-0,77-0,78-0,16-0,17-0,19-0,20-0,21-0,22-0,23-0,24-0,27-0,28-0,25-0,26-0,29-0,30-0,31-0,"
# values = {'select+value': {'avt': '19_r', 'trol': '%23'}}
# data = urllib.urlencode(values)

# data = "select+value=&avt=19_r&trol=%23"
# request = urllib2.Request(url, data)
# response = urllib2.urlopen(request)
response = urllib2.urlopen(url + query)
html = response.read()

print html
