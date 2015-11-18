# -*- coding: utf-8 -*-
'''
EarthPaper: Pull the daily top post from reddit.com/r/earthporn and set as wallpaper
Read README for instructions on how to run program continuously in the
background even when you close terminal.
'''
import os
import sys
import bs4
import time
import ctypes
import requests
import datetime
import subprocess

redditURL = 'https://www.reddit.com/r/earthporn/top/'

def create_dir(directory):
    '''Check to see if a directory exists. If not, create it.
    Args:
        directory: Name of the directory we want to check/create
    '''
    dPath = os.getcwd() + '\\' + directory + '\\'
    os.makedirs(dPath, exist_ok=True)
    return dPath

def get_picture(redditURL):
    '''Uses redditURL to find top post and download image from imgur
    Args:
        redditURL: link to subreddit
    '''
    # Create unique user-agent for header to get into Reddit, download page
    headers = {'user-agent': 'Mac OSX:https://github.com/jmorales2012/\
                Daily-Wallpaper:v1 (by /u/IAmAmbitious)'}
    redditPage = requests.get(redditURL, headers=headers)
    redditPage.raise_for_status()

    # Parse reddit page, find top post, class='title may-blank'
    redditParsed = bs4.BeautifulSoup(redditPage.text, "html.parser")
    topPosts = redditParsed.select('a.title.may-blank')

    # Get the imgur URL inside top reddit post
    imgurURL = topPosts[0].get('href')

    # Download the imgur page from the URL above
    imgurPage = requests.get(imgurURL, headers=headers)
    imgurPage.raise_for_status()

    # Parse imgur page, find the image selector, and get the URL
    imgurParsed = bs4.BeautifulSoup(imgurPage.text, "html.parser")
    picElem = imgurParsed.select('a.zoom')
    picURL = 'http:' + picElem[0].get('href')

    # Download image from imgur and get file extension
    print('Downloading pic from ' + picURL)
    topPic = requests.get(picURL)
    topPic.raise_for_status
    ext = ['.jpg', '.jpeg', '.png', 'gif']
    name_ext = [x for x in ext if x in picURL]

    # Create folder & file and write in picture data
    filename = create_dir('wallpapers') + str(datetime.date.today()) \
    + name_ext[0]
    with open(filename, 'wb') as imageFile:
        for chunk in topPic.iter_content(100000):
            imageFile.write(chunk)

    return filename

def set_background(filename):
    '''Set the top /r/earthporn image to background wallpaper
    Args:
        imageFile: Is the full path of the image downloaded in get_picture()
    '''
    # Used for Mac OS X (not verified working)
    if sys.platform == 'darwin':

        SCRIPT = '''/usr/bin/osascript<<END
        tell application "Finder"
        set desktop picture to POSIX file "%s"
        end tell
        '''
        subprocess.Popen(SCRIPT % filename, shell=True)

    # Used for Windows 10
    elif sys.platform == 'win32':
        print(filename)
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0,
                                                   filename, 0)

if __name__ == '__main__':

    selection = input('Want to run this continuously? Enter y/n: ').lower()

    while selection == 'y':
        # Run continuously
        print('Read the README to run the program in the background!\n')
        print('Downloading...')

        filename = get_picture(redditURL)
        set_background(filename)
        # Runs the loop every 24 hours
        time.sleep(86400)

    # Run the program only one time
    print('Downloading...')
    filename = get_picture(redditURL)
    set_background(filename)
