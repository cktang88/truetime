import heapq
import os
import tempfile
from datetime import datetime, timedelta
from time import ctime
from typing import List, Optional

import ntplib
from uptime import boottime, uptime

u = uptime()
print(u, "ms since uptime")
# b = boottime()  # based on local clock, don't trust
# print(b)


def all_files_within(path: str):
    """Iterates through all files that are under the given path."""
    for cur_path, _, filenames in os.walk(path):
        for filename in filenames:
            yield os.path.join(cur_path, filename)


def get_millis_gaps(sorted_millis: List[float]):
    """
    Gets gaps between a list of milliseconds
    """

    TOLERANCE = timedelta(minutes=15)
    BIG_TOLERANCE = timedelta(hours=12)

    for i in range(len(sorted_millis) - 1):
        first = datetime.fromtimestamp(sorted_millis[i])
        second = datetime.fromtimestamp(sorted_millis[i + 1])
        if first - second > BIG_TOLERANCE:
            print("skipping ", first, second)
            continue
        if first - second > TOLERANCE:
            yield first, second, i


def get_ntp_time() -> Optional[datetime]:
    """
    Gets time from a public NTP server
    """
    c = ntplib.NTPClient()
    truetime = None
    try:
        response = c.request("pool.ntp.org", version=3)
        truetime = ctime(response.tx_time)
    except Exception as e:
        print("Exception caught: ", e)
    return truetime


def get_estimate_from_temp_dir():
    """
    Tries to estimate time from system temp directory files.
    Assumes system interacts w/ temp dir files on a roughly continuous and consistent basis.
    Steps:
    1. get earliest timestamp that appears trustable
        - scan all files in temp dir, storing timestamps for file creation, file modification, and file last accessed
        - calculate gaps between those timestamps
        - earliest trustable timestamp is the time before earliest gap
    2. calculate how much time has elapsed since that time
        -
    3. add the offset to the earlier timestamp
    """

    MAX_FILES = 20000

    tempdir = tempfile.gettempdir()
    print(tempdir)

    files = list(all_files_within(tempdir))

    alltimes = [os.path.getmtime(e) for e in files]
    alltimes.extend(os.path.getctime(e) for e in files)
    alltimes.extend(os.path.getatime(e) for e in files)
    most_recent = heapq.nlargest(MAX_FILES, alltimes)
    gaps = list(get_millis_gaps(most_recent))
    for i in gaps:
        print(i)
    print(len(gaps), "gaps found.")

    print(len(files), " files.")


# truetime = get_ntp_time()
# if not truetime:
#     truetime = get_estimate_from_temp_dir()

print(get_ntp_time())
print(get_estimate_from_temp_dir())
