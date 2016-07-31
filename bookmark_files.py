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
__name__ = "bookmark_file.py"

import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify
import os
import sys


def send_notification(title, text):
    '''Custom function for sending on-screen notifications'''
    try:
        if Notify.init(argv[0]):
            n = Notify.Notification.new("Notify")
            n.update(title, text)
            n.set_urgency(2)
            if not n.show():
                raise SyntaxError("sending notification failed!")
        else:
            raise SyntaxError("can't initialize notification!")
    except SyntaxError as error:
        print(error)
        if error == "sending notification failed!":
            Notify.uninit()
    else:
        Notify.uninit()

def main():

    user_home = os.path.expanduser('~')
    bookmark_dir = os.path.join( user_home,'Bookmarked_Files'  )
    file_path = os.path.abspath(sys.argv[1])

        
    # ensure the directory exists
    if not os.path.lexists( bookmark_dir  ):
       os.mkdir( bookmark_dir  )

    try:
        os.symlink(file_path, os.path.join(bookmark_dir,sys.argv[1]))
    except OSError as error :
        print("OS error: {0}".format(error))

if __name__ == '__main__':
    main()
