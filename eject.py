#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import urllib.parse
import dbus


def get_dbus( bus_type, obj, path, interface, method, arg):
    """ utility: executes dbus method on specific interface"""
    if bus_type == "session":
        bus = dbus.SessionBus()
    if bus_type == "system":
        bus = dbus.SystemBus()
    proxy = bus.get_object(obj, path)
    method = proxy.get_dbus_method(method, interface)
    if arg:
        return method(arg)
    else:
        return method()

def get_dbus_property( bus_type, obj, path, iface, prop):
    """ utility:reads properties defined on specific dbus interface"""
    if bus_type == "session":
        bus = dbus.SessionBus()
    if bus_type == "system":
        bus = dbus.SystemBus()
    proxy = bus.get_object(obj, path)
    aux = 'org.freedesktop.DBus.Properties'
    props_iface = dbus.Interface(proxy, aux)
    try:
        props = props_iface.Get(iface, prop)
        return props
    except:
        return None

def get_mountpoint(dev_path):
    try:
        contents = [
            'system', 'org.freedesktop.UDisks2', dev_path,
            'org.freedesktop.UDisks2.Filesystem', 'MountPoints'
        ]
        data = get_dbus_property(*contents)[0]

    except:
        return None
    else:
        if len(data) > 0:
            return ''.join([chr(byte) for byte in data])


def find_partition(selected):

    contents = [
        'system', 'org.freedesktop.UDisks2', '/org/freedesktop/UDisks2',
        'org.freedesktop.DBus.ObjectManager', 'GetManagedObjects', None
    ]
    objects = get_dbus(*contents)
    for item in objects:
        try:
            if 'block_devices' in str(item):
                mountpoint = get_mountpoint(item)
                if not mountpoint:
                    continue
                mountpoint = mountpoint.replace('\x00', '')
                mp = str(type(mountpoint))
                if selected == mountpoint:
                    return  '/dev/' + item.split('/')[-1]

        except Exception as e:
            sys.stderr.write(e.__repr__())
            subprocess.call(['zenity','--error','--text',str(e)])

def main():

    uri = os.getenv("NAUTILUS_SCRIPT_SELECTED_URIS")
    uri_decoded = urllib.parse.unquote(uri)
    mountpath = uri_decoded.replace('file://','').strip()
    
    part = find_partition(mountpath)

    try:
        unmount = ['udisksctl', 'unmount', '-b', part ]
        subprocess.check_output(unmount, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        subprocess.call([ 'zenity', '--error','--text', e.output.decode()])

    # Try to power off the drive ( this is for ejecting USBs)
    # If it's a hard-drive with more than one partition in use, disk
    # won't power-off
    try:
        poweroff = ['udisksctl', 'power-off', '-b',part]
        subprocess.check_output(poweroff, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        pass


if __name__ == '__main__' : 
    try:
        main()
    except Exception as e:
        sys.stderr.write(e)
        subprocess.call(['zenity','--error','--text',str(e)])
