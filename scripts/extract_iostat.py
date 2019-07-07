#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script to extract I/O throughputs (read + write) from iostat log.

Usage: $0 IOSTAT_LOG_FILE

"""


import sys

IO_LOG_INTERVAL_IN_SECS = 3


def main():
    rkbs_idx = -1
    wkbs_idx = -1

    data_in_nextline = False

    throughputs = []

    with open(IOSTAT_LOG_FILE, 'rt') as filep:
        for line in filep:
            if rkbs_idx < 0 or wkbs_idx < 0:
                if 'rkB/s' in line:
                    headers = line.split()
                    rkbs_idx = headers.index('rkB/s')
                    wkbs_idx = headers.index('wkB/s')
                continue

            if data_in_nextline:
                if line.strip():
                    nums = line.split()
                    throughputs.append(
                        float(nums[rkbs_idx]) + float(nums[wkbs_idx]))

                data_in_nextline = False
                continue

            if 'Device:' in line:
                data_in_nextline = True

    with open('iostat_throughputs.csv', 'wt') as filep:
        for idx, value in enumerate(throughputs):
            filep.write(
                str(idx * IO_LOG_INTERVAL_IN_SECS) +
                "," +
                str(value) + ",\n"
            )

    avg_throughput = sum(throughputs) / len(throughputs)
    print('The average throughput (read + write) is ' +
          str(avg_throughput) +
          ' KB/s')


if __name__ == "__main__":
    NUM_ARGS = len(sys.argv)
    if NUM_ARGS < 2:
        print("""\
Usage: {} IOSTAT_LOG_FILE

IOSTAT_LOG_FILE:
    The log file generated by IOSTAT(1)
""".format(sys.argv[0]))
        exit(1)

    IOSTAT_LOG_FILE = sys.argv[1]
    main()
