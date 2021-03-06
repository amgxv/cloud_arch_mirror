#!/usr/bin/python

from ping3 import ping
from urllib.parse import urlsplit
import os
import bestmirror

def fetch_mirror():

    mirror_file="./mirrors.txt"
    if os.path.isfile(mirror_file) == False:
        print("Mirror file not detected...")
        bestmirror.get_best_mirrors()
        
    # Get mirrors from textfile and it starts rsync if ping goes well
    f = open(mirror_file,'r')
    for mirror in f:
        mirror = mirror.replace("\n", "")
        url = mirror
        base_url = "{0.netloc}".format(urlsplit(url))
        p = ping(base_url, unit='ms')

        if p is None:
            print("Error fetching mirror {mirror}".format(mirror=mirror))
            pass
        if p is not None:
            print ("Fetching latest packages from : {mirror}".format(mirror=mirror))
            os.system("rsync -rtlvH --delete-after --delay-updates --safe-links {mirror} {path}".format(mirror=mirror, path="./mirror"))
            break
    
    print("Mirror updated successfully!")

if __name__ == "__main__":
    fetch_mirror()
