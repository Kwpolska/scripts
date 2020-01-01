#!/usr/bin/env python3
# Generate https://chriswarrick.com/pub/factoids.html
# Copyright © 2017-2020, Chris Warrick.
# All rights reserved.
# Licensed under the 3-clause BSD license.

import datetime
import json
import platform
import re
from jinja2 import Template
from os.path import expanduser

LINK_RE = re.compile(r'https?://([A-Za-z0-9.-]+.[a-z]+?)\S*')


def linkify(match):
    if match.group(1).endswith(('chriswarrick.com', 'github.com')):
        return '<a href="{0}">{0}</a>'.format(match.group())
    else:
        return '<a href="{0}" rel="nofollow">{0}</a>'.format(match.group())


with open(expanduser('~/.weechat/kwfactoids.json'), 'r', encoding='utf-8') as fh:
    raw_data = json.load(fh)

factoids = []
for f in sorted(raw_data):
    text = LINK_RE.sub(linkify, raw_data[f])
    factoids.append((f, text))

with open('factoids_template.html', 'r', encoding='utf-8') as fh:
    template = Template(fh.read())

with open('/srv/chriswarrick.com/pub/factoids.html', 'w', encoding='utf-8') as fh:
    fh.write(template.render(
        factoids=factoids,
        python_version=platform.python_version(),
        last_update=datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z',
    ))
