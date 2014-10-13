#!/usr/bin/env python

import gspread
import json
import string
import urllib2
from os import listdir
from os.path import isfile, join


GMAIL_ADDRESS = 'brd.work.mail@gmail.com'
GMAIL_PASSWORD = 'casAph7N'
TEST_JSON_SCHEDULE = 'json/19.json'

CLIENT_ID = (
    '350893716146-0es56dkljga1b18hg5l9r1pserisnb8d.apps.googleusercontent.com'
)
CLIENT_SECRET = "SZKNTFrROcsEj6NeMg-JJTw7"
"""Redirect URIS"""
"""
urn:ietf:wg:oauth:2.0:oob
http://localhost
"""


class SpreadsheetSerialization:
    def __init__(self, gmail, password, credentials_filename):
        self._gs = gspread.login(gmail, password)
        self._spreadsheet_creator = SpreadsheetCreator(credentials_filename)

    def serialize_schedule_json(self, json_filename):
        json_f_schedule = open(json_filename, 'r')
        json_txt_schedule = json_f_schedule.read()
        json_obj_schedule = json.loads(json_txt_schedule)
        # stations_list = json_obj_schedule['stations']
        schedule_table = json_obj_schedule['schedule']

        spreadsheet_name = string.split(json_filename, '.')[:-1]
        print spreadsheet_name
        spreadsheet_name = string.split(spreadsheet_name[0], '/')[-1]
        print spreadsheet_name
        self._spreadsheet_creator.create_spreadsheet(spreadsheet_name)
        worksheet = self._gs.open(spreadsheet_name).sheet1
        self._fill_time(worksheet, schedule_table)

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

    def __init__(self, credentials_filename):
        self._credentials = self._load_credentials(credentials_filename)
        self._token_response = self._credentials['token_response']
        self._access_token = self._token_response['access_token']
        self._token_type = self._token_response['token_type']

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

    def _load_credentials(self, credentials_filename):
        json_f_credentials = open(credentials_filename, 'r')
        json_txt_credentials = json_f_credentials.read()
        json_obj_credentials = json.loads(json_txt_credentials)
        return json_obj_credentials


if __name__ == "__main__":
    spreadsheet_serialization = SpreadsheetSerialization(
        GMAIL_ADDRESS,
        GMAIL_PASSWORD,
        'credentials.json'
    )
    JSON_DIR = 'json/'
    onlyfiles = [f for f in listdir(JSON_DIR) if isfile(join(JSON_DIR, f))]
    print onlyfiles
    for filename in onlyfiles:
        spreadsheet_serialization.serialize_schedule_json(JSON_DIR + filename)
