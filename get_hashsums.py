#!/usr/bin/env python3
import sys
import urllib.parse
import hashlib
import os
import subprocess
import tempfile
from collections import OrderedDict as od

def get_hashsums(file_path):
    hash_sums = od()
    hash_sums['md5sum'] = hashlib.md5()
    hash_sums['sha1sum'] = hashlib.sha1()
    hash_sums['sha224sum'] = hashlib.sha224()
    hash_sums['sha256sum'] = hashlib.sha256()
    hash_sums['sha384sum'] = hashlib.sha384()
    hash_sums['sha512sum'] = hashlib.sha512()

    with open(file_path, 'rb') as fd:
        data_chunk = fd.read(1024)
        while data_chunk:
              for hashsum in hash_sums.keys():
                  hash_sums[hashsum].update(data_chunk)
              data_chunk = fd.read(1024)

    results = od()
    for key,value in hash_sums.items():
         results[key] = value.hexdigest()         
    return results

def puke(message):
    sys.stderr.write(message + '\n')
    subprocess.call(['zenity', '--error', '--text', message])
    sys.exit(2)

def write_temp_file(data):
    temp = tempfile.mkstemp()[1]
    with open(temp, 'w') as fd:
        fd.write(data)
    return temp


def main():
    uri_list = os.getenv("NAUTILUS_SCRIPT_SELECTED_URIS").strip().split()
    output_lines = []
    for uri in uri_list:
        uri_decoded = urllib.parse.unquote(uri)
        path = uri_decoded.replace('file://','').strip()
        if not os.path.isfile(path):
             puke(path+" is not a regular file")
        text = ""
        text = path + "\n" 
        hashsums = get_hashsums(path)
        for key,value in hashsums.items():
              text = text + key + " " + value + "\n"
        output_lines.append(text)

    output_file = write_temp_file("\n".join(output_lines))
    subprocess.call(['zenity','--text-info',
                     '--title','Hash Sums',
                     '--filename',output_file])
    os.unlink(output_file)

if __name__ == '__main__': 
    try:
        main()
    except Exception as e:
        puke(repr(e))
