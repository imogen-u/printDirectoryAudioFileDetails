#!/usr/bin/python
# Print FLAC file details = prints the filename, artist, track, album
# and tracklength of FLAC, MP3 or M4A audio files in directory

import os, mutagen, time, datetime
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from datetime import timedelta, datetime
import pyinputplus as pyip

# Choose directory
os.chdir("DIRECTORY-HERE")

# Get files in directory and sort
entries = os.listdir()
entries.sort()

# Get track length in time object
def getTimeObject(file):
    sec = file.info.length
    ty_res = time.gmtime(sec)
    return time.strftime("%M:%S",ty_res)

# Get track's length in seconds (integer)
def getSecStr(time_str):
    m, s = time_str.split(':')
    return int(m) * 60 + int(s)

# Print artist, track name and album. For some reason all audio formats
# have very different dictionary key names for the tag data.
def printDetails(file):
    if file.endswith('.flac'):
        print('\tArtist - Track Title : ' +
        audio['ARTIST'][0] + ' - ' + audio['TITLE'][0])
        print('\tAlbum : ' + audio['ALBUM'][0])
        print('\tAlbum Artist : ' + audio['ALBUMARTIST'][0])
    elif file.endswith('.mp3'):
        print('\tArtist - Track Title : ' +
        audio['TPE1'][0] + ' - ' + audio['TIT2'][0])
        print('\tAlbum : ' + audio['TALB'][0])
        print('\tAlbum Artist : ' + audio['TPE2'][0])
    elif file.endswith('.m4a'):
        print('\tArtist - Track Title : ' +
        audio["\xa9ART"][0] + ' - ' + audio["\xa9nam"][0])
        print('\tAlbum : ' + audio["\xa9alb"][0])
        print('\tAlbum Artist : ' + audio['aART'][0])
    else:
        print("\tFile format is incompatible. Skipping.\n")

# Ask user to give a starting date/time
print("When did you start listening to this playlist?")
print("Enter the date and time in format yyyy/mm/dd hh:mm.")
realtime = str(input())
starttime = datetime.strptime(realtime, "%Y/%m/%d %H:%M")
print("You started listening to playlist at "
      + str(starttime) + "\n")

# Ask user if they listened to every track in dictory.
prompt = 'Did you listen to this playlist in full without repeats or skips?\n'
fullListen = pyip.inputYesNo(prompt)

# Ask user to give an ending date/time
if fullListen == 'no':
    prompt = 'Did you listen to every track?\n'
    everyTrack = pyip.inputYesNo(prompt)
    if everyTrack == 'no':
        print("When did you stop listening to this playlist?")
        print("Enter the date and time in format yyyy/mm/dd hh:mm.")
        realtime = str(input())
        endtime = datetime.strptime(realtime, "%Y/%m/%d %H:%M")
        print("You stopped listening to playlist at "
              + str(endtime))

# Ask user if they played a track on repeat
if fullListen == 'no':
    prompt = 'Did you put any tracks on repeat?\n'
    repeatAnyTrack = pyip.inputYesNo(prompt)

# Ask user if they skipped a track
if fullListen == 'no':
    prompt = 'Did you skip any tracks?\n'
    skipAnyTrack = pyip.inputYesNo(prompt)

print("\n")

for entry in entries:
    if entry.endswith('.flac'):
        audio = FLAC(entry)
    elif entry.endswith('.mp3'):
        audio = MP3(entry)
    elif entry.endswith('.m4a'):
        audio = MP4(entry)
    print(entry)
    printDetails(entry)
    if entry.endswith(('.flac', '.m4a', '.mp3')):
        # Print details on track length and time started.
        length = getTimeObject(audio)
        print("\tTrack Length : " + length + "\n")
        if 'skipAnyTrack' in locals() and skipAnyTrack == 'yes':
            prompt = 'Did you skip this track?\n'
            skipThisTrack = pyip.inputYesNo(prompt)
            if skipThisTrack == 'yes':
                print("\tTRACK SKIPPED\n")
                continue
        print("\tStarted listening at : " + str(starttime) + "\n")
        # Ask user if they played track on repeat and how many times
        if 'repeatAnyTrack' in locals() and repeatAnyTrack == 'yes':
            prompt = 'Did you play this track on repeat?\n'
            repeatThisTrack = pyip.inputYesNo(prompt)
            if repeatThisTrack == 'yes':
                print("How many times did you play this track?")
                repeatNo = int(input())
            print("\n")
        # Work out start time for the following track.
        length = getSecStr(length)
        if 'repeatNo' in locals() and repeatNo != None:
            starttime = starttime + (timedelta(seconds=length) * repeatNo)
        else:
            starttime = starttime + timedelta(seconds=length)
        repeatNo = None
    # Work out if next track was listened to based on user's end listening time.
    if 'endtime' in locals():
        if starttime > endtime:
            break

print('Done!')

# End of file.
