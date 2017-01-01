#!/usr/bin/env python3
# Automatically unzip any .zip files in ~/Downloads to the CWD.
# Requires watchdog.
# Copyright © 2016-2017, Chris Warrick.
# All rights reserved.
# Licensed under the 3-clause BSD license.


"""Automatically unzip any .zip files in ~/Downloads to the CWD."""

import logging
import os
import time
import watchdog
import watchdog.observers
import watchdog.events
import zipfile

logging.basicConfig(
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
l = logging.getLogger("auto-unzip")
l.setLevel(logging.DEBUG)


class Handler(watchdog.events.FileSystemEventHandler):
    """Watchdog handler that unzips files."""

    def on_modified(self, event):
        """Handle modified event."""
        fn = event.src_path
        if fn.endswith('.zip'):
            l.info("{0} --> unpacking".format(fn))
            zf = zipfile.ZipFile(fn)
            zf.extractall()
            for f in zf.filelist:
                l.info("  " + f.filename)
        else:
            l.debug(fn)


o = watchdog.observers.Observer()
o.schedule(Handler(), os.path.expanduser('~/Downloads'), recursive=True)
print("Starting observer...")
o.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    o.stop()
o.join()
