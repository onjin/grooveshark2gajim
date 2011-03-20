#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Script reads current song data from Grooveshark desktop status and puts it as
gajim account status message.

The file currentSong.txt is usually stored at:
  * Linux: ~/Grooveshark/currentSong.txt or ~/Documents/Grooveshark/currentSong.txt
  * Win XP: Documents and Settings\(Your User)\My Documents\Grooveshark\currentSong.txt
  * Vista/7: Users\(Your User)\Documents\Grooveshark\currentSong.txt


License, BSD.

Copyright (c) 2011, Marek Wywiał
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

  Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
  Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
  Neither the name of the <ORGANIZATION> nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import os
import sys
import time
from optparse import OptionParser
from pyinotify import WatchManager, Notifier, ProcessEvent, EventsCodes




__progname__ = 'grov2gajim.py'
__author__ = 'Marek  Wywial <marek@marekwywial.name>'
__version__ = ' %s v1.0.0        // %s' % (__progname__, __author__)

usage = """%s [gajim account name] [path to grooveshark currentSong.txt]

  Script reads current song data from Grooveshark desktop status and puts it as
  gajim account status message.

  The file currentSong.txt is usually stored at:
    * Linux: ~/Grooveshark/currentSong.txt or ~/Documents/Grooveshark/currentSong.txt
    * Win XP: Documents and Settings\(Your User)\My * Documents\Grooveshark\currentSong.txt
    * Vista/7: Users\(Your User)\Documents\Grooveshark\currentSong.txt

  Examples:
    Run grov2gajim once:
      grov2gajim.py gmail.com ~/Dokumenty/Grooveshark/currentSong

    Run grov2gajim and monitor currentSong.txt file for changes:
      grov2gajim.py -b gmail.com ~/Dokumenty/Grooveshark/currentSong

    Run grov2gajim in background and monitor currentSong.txt file for changes:
      nohup grov2gajim.py -b gmail.com ~/Dokumenty/Grooveshark/currentSong &

  %s
""" % (__progname__, __version__)

def set_status(account, grovstatus_file, options):


    # let's read metadata from grooveshark file
    grovdata = file(grovstatus_file, 'r').read()[:-1]

    try:
        title, album, author, status, play_url, album_url = grovdata.split('\t')
    except ValueError:
        # empty file, right after start of grooveshark
        status = 'empty'


    # we change status when we are really playing any song
    if status == 'playing':
        if options.verbose: print "[d] setting new status message"

        msg = """listening to "%s (%s/%s)" %s""" % (title, author, album, play_url)
        cmd = "gajim-remote change_status `gajim-remote get_status %s` '%s' %s" % (account, msg.replace("'", ""), account)

        if options.debug:
            print "[d] %s" % (cmd,)
        else:
            os.system(cmd)
    else:
        if options.verbose: print "[d] status is not 'playing', skipping ..."


parser = OptionParser(prog=__progname__, version=__version__, usage=usage)
        
parser.add_option('-v', '--verbose', dest="verbose", action="store_true",
        default=False, help="show me more")
parser.add_option('-d', '--debug', dest="debug", action="store_true",
        default=False, help="just show what would be done")
parser.add_option('-b', '--background', dest="background", action="store_true",
        default=False, help="run in background and monitor currentSong.txt file for changes")

(options, args) = parser.parse_args()


if len(args) != 2:
    print
    parser.error("incorrect number of arguments\n\nCheck help (-h) for advice.\n")

account, grovstatus_file = args

if not options.background:
    if options.verbose: print "[d] run once"
    set_status(account, grovstatus_file, options)
    sys.exit(0)

if options.verbose: print "[d] run monitoring file %s" % (grovstatus_file,)


class PClose(ProcessEvent):
    def process_IN_CLOSE(self, event):
        # wait for write to file
        time.sleep(5)
        set_status(account, grovstatus_file, options)


wm = WatchManager()
notifier = Notifier(wm, PClose())
wm.add_watch(grovstatus_file, EventsCodes.ALL_FLAGS.get('IN_CLOSE_WRITE'))
#wm.add_watch(grovstatus_file, EventsCodes.ALL_FLAGS.get('IN_CLOSE_WRITE')|EventsCodes.ALL_FLAGS.get('IN_CLOSE_NOWRITE')) 
set_status(account, grovstatus_file, options)

try:
    while 1:
        notifier.process_events()
        if notifier.check_events():
            notifier.read_events()
except KeyboardInterrupt:
    notifier.stop()


