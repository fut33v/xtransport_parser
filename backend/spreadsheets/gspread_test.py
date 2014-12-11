#!/usr/bin/env python

__author__ = 'Ilya Fateev'

import gspread
import json
import string
import urllib2
from os import listdir
from os.path import isfile, join
# import parser_utils


GMAIL_ADDRESS = 'brd.work.mail@gmail.com'
GMAIL_PASSWORD = 'casAph7N'


def load_json_file(filename):
    json_f = open(filename, 'r')
    json_obj = json.loads(json_f.read())
    json_f.close()
    return json_obj


class SpreadsheetSerialization:
    def __init__(self, credentials):
        self._gs = gspread.authorize(credentials)
        self._spreadsheet_creator = SpreadsheetCreator(credentials)

    def serialize_transport_json(self, json_filename):
        transport = load_json_file(json_filename)
        # schedule_table = transport['schedule_workdays']

        spreadsheet_name = string.split(json_filename, '.')[:-1]
        print spreadsheet_name
        spreadsheet_name = string.split(spreadsheet_name[0], '/')[-1]
        print spreadsheet_name
        self._spreadsheet_creator.create_spreadsheet(spreadsheet_name)
        spreadsheet = self._gs.open(spreadsheet_name)

        # worksheet = spreadsheet.add_worksheet('workdays', 1, 1)
        worksheet = spreadsheet.add_worksheet('stations', 1, 1)
        # worksheet = spreadsheet.sheet1
        stations_workdays = [
            station['name'] for station in transport['stations_workdays']
        ]
        stations_weekend = [
            station['name'] for station in transport['stations_weekend']
        ]

        if transport['weekend'] is True and transport['workdays'] is True:
            i = 0
            max_length = max(len(stations_workdays), len(stations_weekend))
            stations = []
            for i in range(max_length):
                try:
                    st_wrk = stations_workdays[i]
                except IndexError:
                    st_wrk = ''
                try:
                    st_wknd = stations_weekend[i]
                except IndexError:
                    st_wknd = ''

                tmp = [st_wrk, st_wknd]
                stations.append(tmp)

            for row in stations:
                worksheet.append_row(row)

        # worksheet.append_row(stations_workdays)
        # worksheet.append_row(stations_weekend)

        # for bus_entry in schedule_table:
        #     print bus_entry
        #     worksheet.append_row(bus_entry)

        # self._fill_time(worksheet, schedule_table)

    def _fill_stations(self, stations_list):
        print "hello"

    def _fill_time(self, worksheet, schedule_table):
        column = 1
        row = 1
        for bus_entry in schedule_table:
            column = 1
            for time_entry in bus_entry:
                print time_entry
                worksheet.update_cell(row, column, time_entry)
                column += 1
            row += 1


class Credentials (object):
    def __init__(self, credentials_filename):
        credentials = load_json_file(credentials_filename)
        token_response = credentials['token_response']
        self.access_token = token_response['access_token']
        self.token_type = token_response['token_type']

    def refresh(self, http):
        raise Exception("Not implemented")
        # get new access_token
        # this only gets called if access_token is None


class SpreadsheetCreator:
    MIME_SPREADSHEET = "application/vnd.google-apps.spreadsheet"
    API_ENDPOINT = "https://www.googleapis.com/drive/v2/files"
    REQUEST_BODY_EXAMPLE = (
        """
        {
            "mimeType": "application/vnd.google-apps.spreadsheet",
            "title": "allahakbar"
        }
        """
    )

    def __init__(self, credentials):
        self._access_token = credentials.access_token
        self._token_type = credentials.token_type

    def create_spreadsheet(self, spreadsheet_filename):
        title = spreadsheet_filename
        request_body = {
            'mimeType': SpreadsheetCreator.MIME_SPREADSHEET,
            'title': title
        }
        request_body = json.dumps(request_body)
        print "request_body:", request_body
        request = urllib2.Request(
            url=SpreadsheetCreator.API_ENDPOINT,
            data=request_body
        )
        request.add_header(
            'Content-type',
            'application/json'
        )
        request.add_header(
            'Authorization',
            self._token_type + " " + self._access_token
        )
        response = None
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError as e:
            print e.reason
            # raise e
        return response


def main():
    credentials = Credentials('credentials.json')
    print credentials.access_token
    spreadsheet_serialization = SpreadsheetSerialization(credentials)
    TRANSPORT_DIR = 'json/transport/'
    # spreadsheet_serialization.serialize_transport_json(
    #     TRANSPORT_DIR +
    #     'bus_1.json'
    # )
    onlyfiles = [
        f for f in listdir(TRANSPORT_DIR) if isfile(join(TRANSPORT_DIR, f))
    ]
    print onlyfiles
    for filename in onlyfiles:
        spreadsheet_serialization.serialize_transport_json(
            TRANSPORT_DIR + filename
        )


if __name__ == "__main__":
    main()
