#!/usr/bin/python3

import json
import sys

'''
lkg_dict = {}
with open ('lib.data', "r") as fp :
    for line in fp:
        line = line.rstrip()
        if line.startswith('Cell Type'):
            cell_data = line.split()[2]
            cell_name, cell_lkg = cell_data.split(',')
            cell_family, cell_vt, cell_drive = cell_name[:-3], cell_name[-3], cell_name[-2:]
            cell_family = f'{cell_family}:{cell_drive}'
            if cell_family not in lkg_dict:
                lkg_dict[cell_family] = {}
            lkg_dict[cell_family][cell_vt] = cell_lkg

with open('lkg_dict.json', 'w') as fp:
    json.dump(lkg_dict, fp, indent=4)

print(f'Writing cell_delta_lkg.csv')
with open(f'cell_delta_lkg.csv', 'w') as fcsv:
    fcsv.write(f'from_cell,from_vt,to_cell,to_vt,delta_lkg\n')
    for cell_family, cell_dict in lkg_dict.items():
        for vt, lkg in cell_dict.items():
            x, y = cell_family.split(':')
            from_cell = f'{x}{vt}{y}'
            from_lkg = lkg
            for v in ['s', 'm', 'f']:
                to_cell = f'{x}{v}{y}'
                to_lkg = cell_dict[v]
                delta_pwr = float(to_lkg) - float(from_lkg)
                fcsv.write(f'{from_cell},{vt},{to_cell},{v},{delta_pwr}\n')

'''


with open('lib.data', 'r') as fp:
    for line in fp:
        line = line.rstrip()
        if not line or line.startswith('Parsing'):
            continue
        if line.startswith('Cell Type'):
            cell_data = line.split()[2]
            cell_name, cell_lkg = cell_data.split(',')
            continue
        if line.startswith('Timing info'):
            arc = line.split()[3]
            arc = arc[:-1]
            continue
        if line.startswith('Rise delay'):
            arc_type = 'delay'
            continue
        if line.startswith('Rise transition'):
            arc_type = 'slew'
            continue

        c_load, input_trans, arc_data = line.split(',')

        print(f'{cell_name}/{arc}', arc_type, c_load, input_trans, arc_data)
