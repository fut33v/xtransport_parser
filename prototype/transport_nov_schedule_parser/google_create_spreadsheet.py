#!/usr/bin/env python

import urllib2
import json


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
        try:
            urllib2.urlopen(request)
        except urllib2.URLError as e:
            print e.reason

    def _load_credentials(self, credentials_filename):
        json_f_credentials = open(credentials_filename, 'r')
        json_txt_credentials = json_f_credentials.read()
        json_obj_credentials = json.loads(json_txt_credentials)
        return json_obj_credentials


spreadsheet_creator = SpreadsheetCreator('credentials.json')
spreadsheet_creator.create_spreadsheet('bus_20')
