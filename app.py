"""
"""
# todo complete file doc

import multiprocessing as mp
import os
import sys
import time
import bart_api
import timeout as timeout
from bart_plot import *
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def handle_exceptions():
    time.sleep(1)

def listener(q):
    while True:
        try:
            parsed_trains = q.get(False)
        except:
            continue
        plot_map(parsed_trains)


def cont_fetch_api(q):
    bart = bart_api.Bart()
    while True:
        try:
            current_departures = bart.fetch_multi_first_departures()
        except (ConnectionError, KeyError, timeout.TimeoutError):
            handle_exceptions()
            continue
        leaving_trains = bart.fetch_leaving_train(current_departures)
        parsed_trains = parse_for_plot(leaving_trains)
        q.put(parsed_trains)

def main():
    os.chdir(BASE_DIR)

    manager = mp.Manager()
    q = manager.Queue()
    pool = mp.Pool(2)

    watcher = pool.apply_async(listener, (q,))  # first multiprocess
    job = pool.apply_async(cont_fetch_api, (q,))  # second multiprocess
    job.get()
    pool.close()
    pool.join()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
