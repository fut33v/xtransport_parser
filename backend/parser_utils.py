#!/usr/bin/env python

__author__ = 'Ilya Fateev'

from functools import partial
import json
import urllib2
import time
import logging


json_pretty_dumps = partial(
    json.dumps,
    sort_keys=True,
    indent=4,
    separators=(',', ': ')
)


def load_json_file(filename):
    json_f = open(filename, 'r')
    json_obj = json.loads(json_f.read())
    json_f.close()
    return json_obj


def save_json_file(filename, data):
    json_txt = json_pretty_dumps(data)
    json_f = open(filename, 'w')
    json_f.write(json_txt)
    json_f.close()


def download_page(url_string, data="", retry_sleep_time=1):
    """
    Function downloads html page by given url,
    if URLError raises, it will retry after
    retry_sleep_time.

    Decodes windows-1251.
    """

    request = None
    response = None
    success = False

    if data == "":
        request = urllib2.Request(url_string)
    else:
        request = urllib2.Request(
            url_string,
            data
        )

    while not success:
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError as e:
            print e.reason
            print (
                "Connection problem, will retry in " +
                str(retry_sleep_time) +
                " seconds"
            )
            logging.info(
                "Connection error %s, will retry in %d seconds",
                str(e.reason),
                retry_sleep_time
            )
            time.sleep(retry_sleep_time)
            success = False
        else:
            success = True

    html = response.read().decode('windows-1251')
    if data == "":
        logging.info(
            "Page with URL: %s downloaded", url_string
        )
    else:
        logging.info(
            "Page with URL: %s and POST data: %s downloaded", url_string, data
        )

    return html


def no_whitespaces(string_):
    return "".join(string_.split())


def in_dict(dictionary, key):
    if key in dictionary:
        return dictionary[key]
    else:
        return None

if __name__ == "__main__":
    save_json_file("test.json", {"id": 1})
