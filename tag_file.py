#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Serg Kolo  
# Date: Oct 1st, 2016
# Description: tag_file.py, script for
#    recording paths to files under 
#    specific , user-defined tag
#    in ~/.tagged_files
# Written for: http://askubuntu.com/q/827701/295286
# Tested on : Ubuntu ( Unity ) 16.04

from __future__ import print_function
import subprocess
import json
import os
import sys

def show_error(string):
    subprocess.call(['zenity','--error',
                     '--title',__file__,
                     '--text',string
    ])
    sys.exit(1)

def run_cmd(cmdlist):
    """ Reusable function for running external commands """
    new_env = dict(os.environ)
    new_env['LC_ALL'] = 'C'
    try:
        stdout = subprocess.check_output(cmdlist, env=new_env)
    except subprocess.CalledProcessError:
        pass
    else:
        if stdout:
            return stdout


def write_to_file(conf_file,tag,path_list):

    # if config file exists , read it
    data = {}
    if os.path.exists(conf_file):
        with open(conf_file) as f:
            data = json.load(f)
  
    if tag in data:
        for path in path_list:
            if path in data[tag]:
               continue
            data[tag].append(path)
    else:
        data[tag] = path_list

    with open(conf_file,'w') as f:
        json.dump(data,f,indent=4,sort_keys=True)
            
def get_tags(conf_file):
    
    if os.path.exists(conf_file):
       with open(conf_file) as f:
            data = json.load(f)
            return '|'.join(data.keys())

def main():

    user_home = os.path.expanduser('~')
    config = '.tagged_files'
    conf_path = os.path.join(user_home,config)
    file_paths = [ os.path.abspath(f) for f in sys.argv[1:] ]
    tags = None

    try:
        tags = get_tags(conf_path)
    except Exception as e:
        show_error(e)

    command = [ 'zenity','--forms','--title',
                'Tag the File' 
    ]

    if tags:
       combo = ['--add-combo','Existing Tags',
                '--combo-values',tags
       ]

       command = command + combo
          
    command = command + ['--add-entry','New Tag']

    result = run_cmd(command)
    if not result: sys.exit(1)
    result = result.decode().strip().split('|')
    for tag in result:
        if tag == '':
           continue
        write_to_file(conf_path,tag,file_paths)

if __name__ == '__main__':
     main()


