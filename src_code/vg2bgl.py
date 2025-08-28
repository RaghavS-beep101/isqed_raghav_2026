#!/usr/bin/python3

import json
import sys
import gzip


v_dict = {}
type_dict = {}
n_dict = {}
arc_dict = {}
bgl_vertices = []
net_Ceff_dict = {}

connectivity_file = sys.argv[1]
basename = connectivity_file.rsplit('/', maxsplit=1)[1]
basename = basename.split('.')[0]

spef_file = sys.argv[2]
with gzip.open(spef_file, 'rt') as fp:
    for line in fp:
        if 'D_NET' in line:
            line_info = line.rstrip().split()
            net_name, ceff = line_info[1], line_info[2]
            net_Ceff_dict[net_name] = ceff

with open(connectivity_file) as fp:
    for line in fp:
        bgl_v_name, end = line.rstrip().split(',')
        cell_inst, pin_name = bgl_v_name.split('/')
        net_name, cell_type = end.split(':')
        
        if cell_inst not in type_dict:
            type_dict[cell_inst] = cell_type

        if cell_inst not in arc_dict:
            arc_dict[cell_inst] = {}
        arc_dict[cell_inst][pin_name] = net_name

for inst_name, pin_connection in arc_dict.items():
    for pin, inp_net in pin_connection.items():
        if pin == 'o': continue
        if pin == 'ck': continue
        out_net = pin_connection['o']
        type_name = type_dict[inst_name]
        bgl_v_name = f'{inst_name}:{type_name}/{pin}->o'
        bgl_vertices.append(bgl_v_name)
        v_dict[bgl_v_name] = len(v_dict)

        if inp_net in n_dict:
             n_dict[inp_net].append(f'i${bgl_v_name}')
        else:
             n_dict[inp_net] = [f'i${bgl_v_name}']

        if out_net in n_dict:
             n_dict[out_net].append(f'o${bgl_v_name}')
        else:
             n_dict[out_net] = [f'o${bgl_v_name}']

print(f'Writing to {basename}.vertices')
with open(f'{basename}.vertices', 'w') as fv:
    for v in bgl_vertices:
        fv.write(f'{v}\n')
 
 
print(f'Writing to {basename}.edges')
with open(f'{basename}.edges', 'w') as fe:
    for net_name, arc_list in n_dict.items():

        ceff = net_Ceff_dict[net_name]

        # find the input arc in the arc_list
        for arc in arc_list:
            if arc.startswith('i$'):
                n_type, input_arc = arc.split('$')
                input_arc_v = v_dict[input_arc]
                break

        for arc in arc_list:
            if arc.startswith('i$'):
                continue
            n_type,output_arc = arc.split('$')
            output_arc_v = v_dict[output_arc]
            fe.write(f'{output_arc_v},{input_arc_v},{ceff}\n')
            #print(f'{output_arc} -> {net_name} ({ceff}) -> {input_arc}')

'''
with open('arc_dict.json', 'w') as fx:
    json.dump(arc_dict, fx, indent=4) 

with open('n_dict.json', 'w') as fx:
    json.dump(n_dict, fx, indent=4)

with open('v_dict.json', 'w') as fx:
   json.dump(v_dict, fx, indent=4)

with open('type_dict.json', 'w') as fx:
    json.dump(type_dict, fx, indent=4)

with open(f'ceff.json', 'w') as fx:
   json.dump(net_Ceff_dict, fx, indent=4)
'''
