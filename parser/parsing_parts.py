import logging

from parser_schedule import ScheduleParser
from parser_transport import TransportParser
import parser_utils
import parser_configs


def parse_schedules_bus(bus_list):
    for bus in bus_list:

        logging.info("Parsing schedule for bus with id: %s", bus["id"])
        print "Current bus_id is:", bus["id"]

        html = parser_utils.download_page(
            TransportParser.TRANSPORT_PAGE_URL,
            bus["post_data"]
        )
        schedule = ScheduleParser.parse_html(html)

        json_bus_object = {
            'type': 'bus',
            # 'stations': schedule['stations_list'],
            'id': bus["id"],
            'name': bus["name"],
            'everyday': False
        }

        # Case when bus have only weekend schedule
        if bus['weekend'] is True:
            json_bus_object['workdays'] = False
            json_bus_object['weekend'] = True
            json_bus_object['schedule_weekend'] = schedule['schedule_table']
            json_bus_object['stations_weekend'] = schedule['stations_list']

        # Case when bus have workdays, and maybe weekend schedule
        else:
            # Case of '7a' bus (everyday)
            # @TODO: could be others buses like this
            if schedule['everyday'] is True:
                json_bus_object['everyday'] = True
                json_bus_object['workdays'] = True
                json_bus_object['weekend'] = True
                json_bus_object['schedule_everyday'] = (
                    schedule['schedule_table']
                )
                json_bus_object['stations_everyday'] = schedule['stations_list']
            else:
                json_bus_object['workdays'] = True
                json_bus_object['weekend'] = False
                json_bus_object['schedule_workdays'] = (
                    schedule['schedule_table']
                )
                json_bus_object['stations_workdays'] = schedule['stations_list']
                if schedule['weekend'] is True:
                    json_bus_object['weekend'] = True
                    html = parser_utils.download_page(
                        schedule['weekend_link']
                    )
                    schedule_weekend = ScheduleParser.parse_html(html)
                    json_bus_object['schedule_weekend'] = (
                        schedule_weekend['schedule_table']
                    )
                    json_bus_object['stations_weekend'] = (
                        schedule_weekend['stations_list']
                    )
        parser_utils.save_json_file(
            parser_configs.directories["BUSES_DIR"] + bus["id"] + ".json",
            json_bus_object
        )


def parse_schedules_trolley(trolley_list):
    for trolley in trolley_list:
        logging.info("Parsing schedule for trolley with id: %s", trolley["id"])
        print "Current trolley_id is:", trolley["id"]

        html = parser_utils.download_page(
            TransportParser.TRANSPORT_PAGE_URL,
            trolley["post_data"]
        )
        schedule = ScheduleParser.parse_html(html)

        json_trolley_object = {
            'type': 'trolley',
            'id': trolley["id"],
            'name': trolley["name"],
            'workdays': False,
            'weekend': False,
            'everyday': False
        }

        # in trolley case ['workdays'] always True
        if trolley['workdays'] is True:
            # case, when trolley works only on workdays
            if schedule['workdays'] is True:
                print "Workdays only"
                json_trolley_object['workdays'] = True
                json_trolley_object['schedule_workdays'] = (
                    schedule['schedule_table']
                )
                json_trolley_object['stations_workdays'] = (
                    schedule['stations_list']
                )
            # regular case, when trolley works both on workdays and weekend
            else:
                json_trolley_object['workdays'] = True
                json_trolley_object['schedule_workdays'] = (
                    schedule['schedule_table']
                )
                json_trolley_object['stations_workdays'] = (
                    schedule['stations_list']
                )
                if schedule['weekend'] is True:
                    json_trolley_object['weekend'] = True
                    html = parser_utils.download_page(
                        schedule['weekend_link']
                    )
                    schedule_weekend = ScheduleParser.parse_html(html)
                    json_trolley_object['schedule_weekend'] = (
                        schedule_weekend['schedule_table']
                    )
                    json_trolley_object['stations_weekend'] = (
                        schedule_weekend['stations_list']
                    )

        parser_utils.save_json_file(
            (parser_configs.directories["TROLLEYS_DIR"] +
                trolley["id"] + ".json"),
            json_trolley_object
        )


def get_transport_json(transport_list, type_):
    transport = []
    for tr in transport_list:
        transport.append(
            {
                'id': tr['id'],
                'name': tr['name'],
                'type': type_
            }
        )
    return transport
