#!/usr/bin/python3
# Animal extractor
import sys
import json

data = {}
data['animals'] = []
data['animals'].append({
    'tag':'cat',
    'name':'Tom'
    })
data['animals'].append({
    'tag':'dog',
    'name':'Pluto'
    })
data['animals'].append({
    'tag':'vermin',
    'name':'Jeez'
    })


result={}

try:
    arguments = json.load(sys.stdin)
except:
    sys.exit('Error reading input arguments')

if 'tag' in arguments:
    try:
        result = json.dumps(next(filter(lambda animal: animal['tag']==arguments['tag'], data['animals'])))
    except:
        sys.exit('Tax extraction from data failed, perhaps there is no such tag : "'+arguments['tag']+'"')
    print(result)
else:
    sys.exit('Error, at least some "tag" of animal is expected like - cat, dog, vermin')
