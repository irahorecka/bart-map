"""
AN APPLICATION TO MONITOR BART API
AND RETURN STATION, TRAIN LINE, AND
NO. TRAIN CARS FOR TRAINS LEAVING
STATION.
"""
from pybart.api import BART
from data_storage import *
from timeout import timeout


class Bart:
    def __init__(self):
        self.BART = BART(json_format=True)

    def fetch_leaving_train(self, first_departure_dict):
        stn_line_list = []
        for station, minute_departure in first_departure_dict.items():
            time_detail = minute_departure['time']
            station_train_key = "{}_{}".format(station, time_detail[2])
            if time_detail[0] == 'Leaving':
                stn_line_list.append(station_train_key)

        return stn_line_list

    def fetch_multi_first_departures(self):
        stn_abbr_dict = {}
        for stn_abbr, value in AllStations.items():
            departure = self.fetch_single_live_departure(stn_abbr)
            if not departure:
                continue
            first_departure = return_first_sorted_departure(departure)
            stn_abbr_dict[stn_abbr] = {'time': first_departure,
                                       'detail': AllStations[stn_abbr]}

        return stn_abbr_dict

    @timeout(5)  # timeout connection after 5 seconds of inactivity
    def fetch_single_live_departure(self, station):
        try:
            return self.BART.etd.etd(station)['station'][0]['etd']
        except KeyError:
            return 0


def return_first_sorted_departure(stn_departures):
    sorted_stn_time_departures = sort_departure_time(stn_departures)
    first_departure = sorted_stn_time_departures[0]
    if first_departure[0] == 0:
        first_departure[0] = 'Leaving'
    # does not capture multiple 0min departures if present

    return first_departure


def sort_departure_time(stn_departures):
    times_departure = []
    for index, destination in enumerate(stn_departures):
        first_estimate = destination['estimate'][0]
        minute_departure = first_estimate['minutes']
        if minute_departure == 'Leaving':
            minute_departure = 0
        seconds_delay = first_estimate['delay']
        train_key = "{}_{}".format(first_estimate['color'], first_estimate['length'])
        times_departure.append([int(minute_departure), int(seconds_delay), train_key])
    sorted_times_departure = sorted(times_departure, key=lambda x: x[0])

    return sorted_times_departure
