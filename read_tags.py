#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Serg Kolo  
# Date: Oct 1st, 2016
# Description: read_tags.py, script for
#    reading  paths to files under 
#    specific , user-defined tag
#    in ~/.tagged_files
# Written for: http://askubuntu.com/q/827701/295286
# Tested on : Ubuntu ( Unity ) 16.04

import subprocess
import json
import sys
import os


def run_cmd(cmdlist):
    """ Reusable function for running external commands """
    new_env = dict(os.environ)
    new_env['LC_ALL'] = 'C'
    try:
        stdout = subprocess.check_output(cmdlist, env=new_env)
    except subprocess.CalledProcessError as e:
        print(str(e))
    else:
        if stdout:
            return stdout

def show_error(string):
    subprocess.call(['zenity','--error',
                     '--title',__file__,
                     '--text',string
    ])
    sys.exit(1)

def read_tags_file(file,tag):

    if os.path.exists(file):
       with open(file) as f:
            data = json.load(f)
            if tag in data.keys():
                return data[tag]
            else:
                show_error('No such tag')
    else:
       show_error('Config file doesnt exist')

def get_tags(conf_file):
    """ read the tags file, return
        a string joined with | for
        further processing """    
    if os.path.exists(conf_file):
       with open(conf_file) as f:
            data = json.load(f)
            return '|'.join(data.keys())

def main():

    user_home = os.path.expanduser('~')
    config = '.tagged_files'
    conf_path = os.path.join(user_home,config)
   
    tags = get_tags(conf_path)
    command = ['zenity','--forms','--add-combo',
               'Which tag ?', '--combo-values',tags
    ]

    tag = run_cmd(command)
    
    if not tag:
       sys.exit(0)

    tag = tag.decode().strip()
    file_list = read_tags_file(conf_path,tag)
    command = ['zenity', '--list', 
               '--text','Select a file to open',
               '--column', 'File paths'
    ]
    selected = run_cmd(command + file_list)    
    if selected:
       selected = selected.decode().strip()
       run_cmd(['xdg-open',selected])

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        show_error(str(e))
