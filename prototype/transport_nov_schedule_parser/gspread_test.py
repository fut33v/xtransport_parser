#!/usr/bin/env python

import gspread
import json
import string


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
    def __init__(self, gmail, password):
        self._gs = gspread.login(gmail, password)

    def serialize_schedule_json(self, json_filename):
        json_f_schedule = open(json_filename, 'r')
        json_txt_schedule = json_f_schedule.read()
        json_obj_schedule = json.loads(json_txt_schedule)
        # stations_list = json_obj_schedule['stations']
        schedule_table = json_obj_schedule['schedule']

        spreadsheet_name = string.split(json_filename, '.')[:-1]
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


if __name__ == "__main__":
    spreadsheet_serialization = SpreadsheetSerialization(
        GMAIL_ADDRESS,
        GMAIL_PASSWORD
    )
    spreadsheet_serialization.serialize_schedule_json(TEST_JSON_SCHEDULE)
