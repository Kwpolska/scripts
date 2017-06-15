#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# WeeChat script for factoids.
# Copyright © 2017, Chris Warrick.
# All rights reserved.
# Licensed under the 3-clause BSD license.
# Config:
#     var.plugins.python.kwfactoids.path — path to JSON file with factoids
# Commands:
#     /factoid [factoid] [nicks]
#     /factreload

"""WeeChat script for factoids."""

import io
import json
import weechat
SCRIPT_NAME = "kwfactoids"
FACTOIDS = {}
weechat.register(SCRIPT_NAME, "Chris Warrick", "0.1.0", "3-clause BSD", "A simple factoids plugin.", "", "")
script_options = {
    "path": "%h/kwfactoids.json"
}

for option, default_value in script_options.items():
    if not weechat.config_is_set_plugin(option):
        weechat.config_set_plugin(option, default_value)


def load_factoids():
    """Load all factoids from file."""
    global FACTOIDS
    path = weechat.config_string(weechat.config_get("plugins.var.python.kwfactoids.path"))
    path = weechat.string_eval_path_home(path, {}, {}, {})
    try:
        with io.open(path, 'r', encoding='utf-8') as fh:
            FACTOIDS = json.load(fh)
        weechat.prnt("", "Loaded %d factoids." % len(FACTOIDS))
    except IOError as e:
        weechat.prnt("", "Failed to load factoids from %s. Reason: %s" % (len(path), e))
        return weechat.WEECHAT_RC_ERROR
    return weechat.WEECHAT_RC_OK


def config_cb(data, option, value):
    """Callback called when a script option is changed."""
    return load_factoids()


def command_factoid(data, buffer, args):
    """Send a factoid to channel."""
    args = args.decode('utf-8').split(' ', 1)
    fname = args[0]
    if fname in FACTOIDS:
        ftext = FACTOIDS[fname]
    else:
        weechat.prnt(weechat.current_buffer(), "%sUnknown factoid: %s" % (weechat.prefix("error"), fname.encode('utf-8')))
        return weechat.WEECHAT_RC_ERROR
    if len(args) == 2:
        msg = u": ".join((args[1], ftext))
    else:
        msg = ftext
    weechat.command(buffer, msg.encode("utf-8"))
    return weechat.WEECHAT_RC_OK


def command_factreload(data, buffer, args):
    """Reload factoids."""
    return load_factoids()


def kwfactoids_completion_cb(data, completion_item, buffer, completion):
    """Add completion for factoids."""
    for factoid in FACTOIDS:
        weechat.hook_completion_list_add(completion, factoid, 0, weechat.WEECHAT_LIST_POS_SORT)
    return weechat.WEECHAT_RC_OK

load_factoids()

weechat.hook_command("factoid", "Send a factoid to channel.", "[factoid] [user]",
                     "factoid is name of factoid, user (optional) is user to direct the factoid at.",
                     "%(kwfactoidsc) %(nicks)", "command_factoid", "")
weechat.hook_command("factreload", "Reload factoids.", "", "", "", "command_factreload", "")
weechat.hook_completion("kwfactoidsc", "Factoid completion", "kwfactoids_completion_cb", "")
weechat.hook_config("plugins.var.python." + SCRIPT_NAME + ".*", "config_cb", "")
