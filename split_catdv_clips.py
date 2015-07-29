#!/usr/bin/env python
# -*- coding: utf-8 -*-
######################################################################
# Written by Tim Bielawa <timbielawa@gmail.com>
#
# The MIT License (MIT)
#
# Copyright © 2015 Tim Bielawa <timbielawa@gmail.com>
# See GitHub Contributors Graph for more information
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sub-license, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from __future__ import print_function
import argparse
import os
import re
import sys


def debug(msg):
    if args.debug:
        print("[DEBUG] %s" % msg)

parser = argparse.ArgumentParser(
    description='Split CatDV XML files into chunks')
parser.add_argument(
    'source', help='Path to the master XML source file to split')
parser.add_argument(
    '-d', '--debug', action='store_true',
    help='Enables debug information printing')
parser.add_argument(
    '-f', '--force', action='store_true',
    help='Overwrite destination clip files if they already exist')
parser.add_argument(
    '-o', '--out', default=os.path.abspath('./clips/'),
    help='Path of the location to store the split-out clip files in '
    'default: ./clips/, will be created automatically')

args = parser.parse_args()

######################################################################

HEADER = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<?xml-stylesheet type="text/css" href="http://www.squarebox.com/legacy/catdv.css"?>
<!-- Created by CatDV Pro 11.0.6 on 7/28/2015 10:51:13 -->
<CLIPS>
"""
FOOTER = """</CLIPS>
"""

SOURCE = os.path.abspath(args.source)
DEST = os.path.abspath(args.out)

if not os.path.exists(DEST):
    debug("Creating destination clips directory: %s" % DEST)
    os.mkdir(DEST)

debug("Reading in source file from: %s" % SOURCE)
debug("Writing out clips into: %s" % DEST)


# A list of clip names we discovered
FOUND_CLIPS = []


def clip_name(c):
    for line in c.split('\n'):
        if "<NAME>" in line:
            _l = line.strip()
            _name = _l.replace("<NAME>", "").replace("</NAME>", "")
            _name += ".xml"
            if _name in FOUND_CLIPS:
                _name = _name + "_02"
            else:
                FOUND_CLIPS.append(_name)
            return _name


def fix_index(c):
    for i in xrange(len(c)):
        if "CLIP INDEX=" in c[i]:
            c[i] = re.sub(r'([0-9]+)', '0', c[i])
            break
    return '\n'.join(c)


def write_clip(c):
    cname = clip_name(c)
    cfile = os.path.join(DEST, cname)
    if os.path.exists(cfile) and not args.force:
        print("[ERROR] Destination clip file already exists: %s" % cfile)
        print("[INFO] Run this script again with the --force option to overwrite existing files")
        raise SystemExit(1)
    else:
        with open(cfile, 'w') as out:
            out.write(HEADER)
            out.write(c)
            out.write(FOOTER)
        sys.stdout.write('.')


with open(SOURCE, 'r') as _source:
    all_clips = []
    i = 0
    clip_start = None
    clip_end = None
    for line in _source.readlines():
        if "<CLIP INDEX" in line:
            clip_start = i

        elif "</CLIP>" in line:
            clip_end = i
            all_clips.append((clip_start, clip_end))

        i += 1

    actual_clips = []

    _source.seek(0)
    everything = [l.rstrip() for l in _source.readlines()]
    for segment in all_clips:
        start = segment[0]
        end = segment[1]
        fixed_index_clip = fix_index(everything[start:end + 1])
        actual_clips.append(fixed_index_clip)

    print("%s clips to write out..." % len(actual_clips))
    for final_clip in actual_clips:
        write_clip(final_clip)

    print("""

All done. Your %s clips are located in: %s""" % (len(actual_clips), args.out))
