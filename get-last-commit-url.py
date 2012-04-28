#!/usr/bin/env python

# Requirements
# pip install pyquery requests
# PyQuery: http://pypi.python.org/pypi/pyquery
# Requests: http://docs.python-requests.org/en/latest/index.html

import subprocess, sys


def main():

    output = subprocess.check_output('git log --no-merges -1 --pretty=oneline', shell=True)

    hash, title = output.split(' ', 1)

    try:
        from fabric.colors import blue
        sys.stderr.write(blue(title))
    except ImportError:
        sys.stderr.write('%s' % title)

    sys.stdout.write('https://github.com/nicksergeant/snipt/commit/%s' % hash)

if __name__ == '__main__':
    main()
