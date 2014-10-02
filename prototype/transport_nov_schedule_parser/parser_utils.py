__author__ = 'Ilya Fateev'

from functools import partial
import json
import urllib2
import time

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

    response = None
    success = False

    if data == "":
        while not success:
            try:
                response = urllib2.urlopen(url_string)
                success = True
            except urllib2.URLError as e:
                print e
                print (
                    "Connection problem, will retry in " +
                    str(RETRY_SLEEP_TIME) +
                    " seconds"
                )
                time.sleep(RETRY_SLEEP_TIME)
    else:
        request = urllib2.Request(
            url_string,
            data
        )
        response = urllib2.urlopen(request)

    html = response.read().decode('windows-1251')
    print "Page with URL:", url_string, "data:", data, "downloaded."
    return html
