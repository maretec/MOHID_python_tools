# -*- coding: utf-8 -*-
# Author: Alexandre Correia / MARETEC
# Email: alexandre.c.correia@tecnico.ulisboa.pt
# Last update: 2002-03-06

from datetime import datetime


def process_keywords(key, value):
    # if the keyword is START or END change it to a python datetime object
    if key.upper() == 'START' or key.upper() == 'END':
        try:
            value = datetime.strptime(value, '%Y %m %d %H %M %S')
        except ValueError:
            try:
                value = datetime.strptime(value, '%Y %m %d')
            except ValueError:
                print('Please use START and END in %Y %m %d %H %M %S or %Y %m %d format')
                exit(1)
    
    # if the keyword value is 'true' or 'false' string converts it to python boolean variable
    if value.upper() == 'TRUE':
        value = True
    if value.upper() == 'FALSE':
        value = False
    
    return key, value


def get_mohid_dat(file):
    f = open(file)
    # creates an empty python dictionary
    dat = {}
    while True:
        l = f.readline()
        if l == '':
            break
        # if line starts with ! then it's a comment, skipping
        if l.startswith('!'):
            continue
        # if there's a ! somewhere on the line keep only what's on the left of the !
        elif l.find('!') != -1:
            l = l[:l.find('!')]
        # keyword and value need to be separated by a : character
        if l.find(':') != -1:
            # key is on the left of the : and value on the right
            key = l[:l.find(':')]
            value = l[l.find(':')+1:]
            # removes whitespaces and end of line characters from beggining and end of strings
            key = key.strip(' \n')
            value = value.strip(' \n')
            # runs key and value through the keyword processor
            key, value = process_keywords(key, value)
            # adds key and value to the dat dictionary
            dat.update({key: value})
    f.close()
    return dat
