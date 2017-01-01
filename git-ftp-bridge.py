#!/usr/bin/env python3
# Git ↔ FTP bridge
# Takes incoming HTTP requests (from eg. GitHub or BitBucket webhooks), pulls a git repo, and sends it through FTP.
# Requires ncftp.
# I know shell=True is unsafe. This was thrown together in five minutes for a private project, and it runs in tmux. I don’t care.
# Copyright © 2016-2017, Chris Warrick.
# Licensed under the simplified 2-clause BSD license.

"""Simple and unsafe Git ↔ FTP bridge. Requires ncftp."""

from flask import Flask
import datetime
import subprocess
import os
app = Flask(__name__)

ACCEPTED_REPOS = ['repo1', 'repo2']


@app.route("/<repo_name>", methods=['POST', 'GET'])
def on_push(repo_name):
    """Handle incoming requests and push to FTP."""
    cwd = os.getcwd()
    if not repo_name:
        return "Must specify a name", 400
    elif repo_name not in ACCEPTED_REPOS:
        return "Unknown repository", 403

    # change command and path according to repo_name!
    PATH = "/PATH/TO/GIT/REPOS/DIR/" + repo_name
    os.chdir(PATH)
    subprocess.Popen("git pull && ncftpput -Ru 'USERNAME' -p 'PASSWORD' HOST /REMOTE/DESTDIR " + PATH + "/* && echo -n 'Done ' && date", shell=True)
    os.chdir(cwd)
    return "Done " + datetime.datetime.utcnow().isoformat()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)
