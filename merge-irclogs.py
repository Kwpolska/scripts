#!/usr/bin/env python3
# Merge IRC logs from channel.MM-DD to channel.YYYY-MM format.
# (One-off script; requires modification to work for you)
# Copyright © 2016-2017, Chris Warrick.
# All rights reserved.
# Licensed under the simplified 2-clause BSD license.

import glob
import os

channels = set()
for fn in os.listdir('freenode'):
    channels.add(fn.split('.')[0])
channels = sorted(channels)

for channel in channels:
    for month in range(1, 10):
        month = "0" + str(month)
        path = "freenode/{0}.{1}-??.log".format(channel, month)
        files = sorted(glob.glob(path))
        if files:
            with open('merged/{0}.2016-{1}.log'.format(channel, month), 'wb') as outf:
                for fn in files:
                    with open(fn, 'rb') as inf:
                        outf.write(inf.read())
            print(path)
