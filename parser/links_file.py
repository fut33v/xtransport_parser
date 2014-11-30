import json
from parser_utils import json_pretty_dumps


transport = json.loads(open('json/transport.json', 'r').read())
transport = transport['buses'] + transport['trolleys']
links = ["http://53bus.ru/json/iphone/" + t['id'] + ".json" for t in transport]
open('json/iphone/links.json', 'w').write(json_pretty_dumps({'links': links}))