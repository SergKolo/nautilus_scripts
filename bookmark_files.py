#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Sergiy Kolodyazhnyy
# Contact: 1047481448@qq.com
# Description: Creates a symlink to user-selected file in 
#              /home/username/Bookmarked_Files
#
# The MIT License (MIT)
# 
# Copyright (c) 2016 Sergiy Kolodyazhnyy 
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
__author__ = "Sergiy Kolodyazhnyy <1047481448@qq.com>"

import os
import sys
import subprocess

def main():

    user_home = os.path.expanduser('~')
    bookmark_dir = os.path.join( user_home,'Bookmarked_Files'  )
    file_path = os.path.abspath(sys.argv[1])

        
    # ensure the directory exists
    if not os.path.lexists( bookmark_dir  ):
       os.mkdir( bookmark_dir  )

    # check if the directory is already added as bookmark
    try:

        bookmarks = os.path.join(user_home,'.config/gtk-3.0/bookmarks')
        with open(bookmarks ,'a+') as file:
            file.seek(0)
            data = file.read()  
            if not bookmark_dir in data:
                file.write('file://' + bookmark_dir )   

    except IOError:
         text = '--text="Cannot auto-add bookmark directory to panel.'
         subprocess.call(['zenity','--error',text])             

    # create symlink to file
    try:
        basename = sys.argv[1].split('/')[-1]
        os.symlink(file_path, os.path.join(bookmark_dir,basename))
    except OSError as error :
        text = '--text="' + str(error) + '"'
        subprocess.call( ['zenity','--error',text] ) 

if __name__ == '__main__':
    main()
