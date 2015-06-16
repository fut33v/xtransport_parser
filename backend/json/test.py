import json

def load_json_file(filename):
    json_f = open(filename, 'r')
    json_obj = json.loads(json_f.read())
    json_f.close()
    return json_obj

if __name__ == "__main__":
   t = load_json_file('suburban_transport.json')
   for tr in t:
       print tr['id']

   print len(t)
