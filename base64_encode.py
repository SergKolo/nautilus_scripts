#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from base64 import b64encode
from stat import *
import urllib.parse
import subprocess
import os
import sys

def popup(message,dialog):
    subprocess.call(['zenity','--' + dialog,
                     '--text',message])
def encode_file(path):
    f = open(path,'r')

    if S_ISREG(os.fstat(f.fileno()).st_mode):
       base = os.path.basename(path)
       f2 = open(base + '.base64','wb')
       for line in f:
           encoded_line = b64encode(line.encode())
           f2.write(encoded_line)
       f2.close()
    else:
       popup('Not a regular file ! Skipped ','error')
       return False

    f.close()
    return True

def main():
    uri_list = os.getenv("NAUTILUS_SCRIPT_SELECTED_URIS").strip().split()
    counter = 0
    for uri in uri_list:
        uri_decoded = urllib.parse.unquote(uri)
        path = uri_decoded.replace('file://','').strip()
        if encode_file(path):
            counter += 1
    message = sys.argv[0] + ' finished.'
    message += 'Processed ' + str(counter) + ' files'
    popup(message,'info')

if __name__ == '__main__': 
    try:
        main()
    except Exception as e:
        popup(repr(e),'error')
