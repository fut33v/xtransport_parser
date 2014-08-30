import urllib2
import urllib


url = "http://transport.nov.ru/urban_trans/1"
"""select+value=&avt=19_r&trol=%23"""
values = {'select+value': {'avt': '19_r', 'trol': '%23'}}
data = urllib.urlencode(values)

data = "select+value=&avt=19_r&trol=%23"
request = urllib2.Request(url, data)
response = urllib2.urlopen(request)
html = response.read()

print html
