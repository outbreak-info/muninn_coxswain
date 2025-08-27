#! /usr/bin/python3

import sys
import re

"""
The converted variable names will be lowercase of the original names
"""
set_pattern = re.compile(r'export\s+(\w+)\s*=\s*[\'\"]([\w/\-\.]+)[\'\"]')

with open(sys.argv[1], 'r') as f:
    for l in f.readlines():
        l = l.strip() 
        if l.startswith('#') or l == '':
            print(l)
        else:
            match = set_pattern.match(l)
            name = match.group(1)
            value = match.group(2)
            new_name = name.lower()
            print(f"{new_name}: '{value}'")