__author__ = 'Ilya Fateev'

from functools import partial
import json
import urllib2
import time
import logging

"""
Pretty printing json function.
"""
json_pretty_dumps = partial(
    json.dumps,
    sort_keys=True,
    indent=4,
    separators=(',', ': ')
)


RETRY_SLEEP_TIME = 1


def download_page_with_retry_and_encode(url_string, data=""):
    """
    Function downloads html page by given url,
    if URLError raises, it will retry after
    RETRY_SLEEP_TIME
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

    #response = urllib2.urlopen(request)

    while not success:
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError as e:
            print e.reason
            print (
                "Connection problem, will retry in " +
                str(RETRY_SLEEP_TIME) +
                " seconds"
            )
            logging.info(
                "Connection error %s, will retry in %d seconds",
                str(e.reason),
                RETRY_SLEEP_TIME
            )
            time.sleep(RETRY_SLEEP_TIME)
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
