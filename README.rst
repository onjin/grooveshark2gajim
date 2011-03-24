Description
===========

  Right now WORKS ONLY AT LINUX.

  Script reads current song data from Grooveshark desktop status and puts it as
  gajim account status message.

  The file currentSong.txt is usually stored at:
    * Linux: ~/Grooveshark/currentSong.txt or ~/Documents/Grooveshark/currentSong.txt
    * Win XP: Documents and Settings\(Your User)\My Documents\Grooveshark\currentSong.txt
    * Vista/7: Users\(Your User)\Documents\Grooveshark\currentSong.txt

Examples
========

    Run grov2gajim once:
      * grov2gajim.py gmail.com ~/Dokumenty/Grooveshark/currentSong.txt

    Run grov2gajim once and check what's going on:
      * grov2gajim.py -v gmail.com ~/Dokumenty/Grooveshark/currentSong.txt

    Run grov2gajim once, check what's going on and just display what would be done:
      * grov2gajim.py -vd gmail.com ~/Dokumenty/Grooveshark/currentSong.txt

    Run grov2gajim and monitor currentSong.txt file for changes:
      * grov2gajim.py -b gmail.com ~/Dokumenty/Grooveshark/currentSong.txt

    Run grov2gajim in background and monitor currentSong.txt file for changes:
      * nohup grov2gajim.py -b gmail.com ~/Dokumenty/Grooveshark/currentSong.txt &
