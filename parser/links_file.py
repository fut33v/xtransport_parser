import json
from parser_utils import json_pretty_dumps


transport = json.loads(open('json/transport.json', 'r').read())
transport = transport['buses'] + transport['trolleys']
urban_links = [
    "http://53bus.ru/json/iphone/" + t['id'] + ".json" for t in transport
]
links = {
    'urban_links': urban_links,
    'suburban_links': ["http://53bus.ru/json/suburban_transport.json"],
    'service': "http://53bus.ru/json/transport.json"
}
print links
open('json/iphone/links.json', 'w').write(json_pretty_dumps(links))
