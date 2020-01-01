#!/usr/bin/env python3
# Find password pwnage. Uses Troy Hunt’s Pwned Passwords service.
# Input format: CSV file with 'Title' and 'Password' columns.
# (Perfect for KeePassXC exports, for example)
# Copyright © 2019-2020, Chris Warrick. All rights reserved.
# License: 3-clause BSD.
import csv
import hashlib
import requests
import time
import sys

found_breaches = 0


def progress(char='.'):
    sys.stderr.write(char)
    sys.stderr.flush()


with open("passwords.csv") as fh:
    data = csv.DictReader(fh)

    for line in data:
        title = line['Title']
        password = line['Password']
        full_hash = hashlib.sha1(password.encode('utf-8')).hexdigest()
        hash_first, hash_last = full_hash[:5], full_hash[5:]
        r = requests.get("https://api.pwnedpasswords.com/range/" + hash_first)
        if hash_last in r.text:
            progress('!\n')
            print(title, password)
            found_breaches += 1
        else:
            progress('.')
        time.sleep(1.6)

print("\nFound", found_breaches, "breaches.")
sys.exit(found_breaches)

