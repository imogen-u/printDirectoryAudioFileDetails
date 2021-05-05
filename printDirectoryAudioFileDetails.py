#!/usr/bin/python
# Print FLAC file details = prints the filename, artist, track, album
# and tracklength of FLAC or MP3 audio files in directory

import os, mutagen,time
from mutagen.flac import FLAC
from mutagen.mp3 import MP3

# Choose directory
os.chdir('DIRECTORY-HERE')

# Get files in directory and sort
entries = os.listdir()
entries.sort()

for entry in entries:
    if entry.endswith('.flac'):
        audio = FLAC(entry)
        # Track length
        sec = audio.info.length
        ty_res = time.gmtime(sec)
        length = time.strftime("%M:%S",ty_res)
        # Print details. For some reason flac and mp3 tags are different.
        print(entry)
        print('\tArtist - Track Title : ' +
        audio['ARTIST'][0] + ' - ' + audio['TITLE'][0])
        print('\tAlbum : ' + audio['ALBUM'][0])
        print("\tTrack Length : " + length + "\n")
    elif entry.endswith('.mp3'):
        audio = MP3(entry)
        # Track length
        sec = audio.info.length
        ty_res = time.gmtime(sec)
        length = time.strftime("%M:%S",ty_res)
        # Print details. Different to above flac details.
        print(entry)
        print('\tArtist - Track Title : ' +
        audio['TPE1'][0] + ' - ' + audio['TIT2'][0])
        print('\tAlbum : ' + audio['TALB'][0])
        print("\tTrack Length : " + length + "\n")
    else:
        print(entry)
        print("\tFile format is not MP3 or FLAC. Incompatible.")

# End of file.
