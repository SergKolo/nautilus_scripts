#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Serg Kolo
Date: Aug 16,2016
Written for: http://askubuntu.com/q/809925/295286
"""
import subprocess
import sys
import os.path

def display_file(textfile):
    """ Displays file containing
        directory description if 
        the file exists
    """
    subprocess.call([
                    'zenity', 
                    '--text-info', 
                    '--filename=' + textfile
                    ])

def create_file(textfile):
    """ Creates text file containing
        directory description
        if the description doesn't exist
    """
    try:
        err_text = '"This directory doesn\'t have description.' +\
                   'Would you like to create one now?"'
        subprocess.check_call([
                              'zenity',
                              '--error',
                              '--text=' + err_text
                              ])
    except subprocess.CalledProcessError:
        sys.exit()

    # ensure we create the file
    with open(textfile,'w') as text:
        text.write('')                

    try:
         
        output = subprocess.check_output([
                           'zenity', 
                           '--text-info', 
                           '--editable',
                           '--filename=' + textfile
                           ])
    except subprocess.CalledProcessError:
        sys.exit()

    with open(textfile,'w') as text:
        text.write(output.decode())
                              


def main():

    file_name = '.directory_description'
    directory = os.path.abspath(sys.argv[1])
    file_path = os.path.join(directory, file_name)
    
    if os.path.isfile(file_path):
        display_file(file_path)
    else:
        create_file(file_path )

if __name__ == '__main__':
    main()
