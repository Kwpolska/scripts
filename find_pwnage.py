#!/usr/bin/env python3
# Find password pwnage. Uses Troy Hunt’s Pwned Passwords service.
# Input format: CSV file with 'Title' and 'Password' columns.
# (Perfect for KeePassXC exports, for example)
# Copyright © 2019-2020, Chris Warrick. All rights reserved.
# License: 3-clause BSD.
import csv
import hashlib
import requests
import collections
import time
import sys

found_breaches = []
hash_sets = collections.defaultdict(set)
hash_values = collections.defaultdict(list)
session = requests.Session()


def progress(char="."):
    sys.stderr.write(char)
    sys.stderr.flush()


def print_breaches(full_hash):
    print(full_hash)
    for t, p in hash_values[full_hash]:
        print("\t{}\t{}".format(t, p))


with open("passwords.csv") as fh:
    data = csv.DictReader(fh)

    for line in data:
        title = line["Title"]
        password = line["Password"]
        full_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
        hash_first, hash_last = full_hash[:5], full_hash[5:]
        hash_sets[hash_first].add(hash_last)
        hash_values[full_hash].append((title, password))
    title = password = None
    all_count = sum(len(s) for s in hash_sets.values())
    print("Checking", all_count, "passwords...")
    for hash_first, hash_lasts in hash_sets.items():
        r = session.get("https://api.pwnedpasswords.com/range/" + hash_first)
        for hash_last in hash_lasts:
            if hash_last in r.text:
                progress("!\n")
                full_hash = hash_first + hash_last
                print_breaches(full_hash)
                found_breaches.append(full_hash)
            else:
                progress(".")
        # The API does not require rate-limiting, so we can query it with full speed.
        # time.sleep(0.05)

print("\nFound", len(found_breaches), "breaches.")
for full_hash in found_breaches:
    print_breaches(full_hash)
sys.exit(len(found_breaches))
