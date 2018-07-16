from functools import reduce
import datetime
import time

# START_OF_TIME = -10000
NORMALIZE_FACTOR = 24 * 60 * 60

def _separate(total_time_list, t):
    last_time_list = total_time_list[-1]
    if len(last_time_list) == 0:
        last_time_list.append(t)
    else:
        date_from_time = datetime.date.fromtimestamp(t)
        date_from_last_time = datetime.date.fromtimestamp(last_time_list[0])

        if date_from_last_time.day == date_from_time.day:
            last_time_list.append(t)
        else:
            total_time_list.append([t])
    return total_time_list


def _time_to_sec(t, base_date):
    base_time = time.mktime(base_date.timetuple())
    return int(t - base_time)


def normalize(t):
    return t/NORMALIZE_FACTOR


def restore_normalized_time(nt):
    return int(nt*NORMALIZE_FACTOR)


def preprocess_times(times):
    int_times = [int(t) for t in times]
    separated = reduce(_separate, int_times, [[]]) # list of sub-list of time classfied by day
    separated = [[_time_to_sec(time, datetime.date.fromtimestamp(
        times[0])) for time in times] for times in separated]
    flat_list = []
    for time_list in separated:
        flat_list += time_list
    flat_list.reverse()
    normalized = [normalize(t) for t in flat_list]
    return normalized


if __name__ == "__main__":
    times = [1531193532,
             1531189932,
             1531186332,
             1531182732,
             1531182732,
             1531171932,
             1531171932,
             1531171932,
             1531168332,
             1531146732,
             1531143132,
             1531143132,
             1531139532,
             1531135932,
             1531135932,
             1531128732,
             1531128732,
             1531099800,
             1531096800,
             1531088460,
             1531084980,
             1531084740,
             1531084200,
             1531081800,
             1531081260,
             1531051440,
             1531039200,
             1531038780,
             1531037880,
             1531037760,
             1531036920,
             1531028760,
             1531020600,
             1530965880,
             1530964680,
             1530963240,
             1530947880,
             1530935580,
             1530912000,
             1530906840,
             1530906540,
             1530880500,
             1530872100,
             1530840960,
             1530837360,
             1530791220,
             1530786420,
             1530786240,
             1530761820,
             1530584760,
             1530452400,
             1530448860,
             1530448200,
             1530332100,
             1530272520,
             1530060600,
             1529458800,
             1524902520,
             1524869460,
             1518325260]
    processed = preprocess_times(times)
    print(processed)
    for t in processed:
        print(restore_normalized_time(t))
