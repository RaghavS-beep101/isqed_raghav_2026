#!/usr/bin/python3

import json
import sys


v_dict = {}
n_dict = {}
arc_dict = {}
bgl_vertices = []
net_Ceff_dict = {}
opin_Ceff_dict = {}

connectivity_file = sys.argv[1]
basename = connectivity_file.rsplit('/', maxsplit=1)[0]
basename = basename.split('.')[0]

spef_file = sys.argv[2]
with open(spef_file, 'r') as fp:
    for line in fp:
        if 'D_NET' in line:
            line_info = line.rstrip().split()
            net_name, ceff = line_info[1], line_info[2]
            net_Ceff_dict[net_name] = ceff

with open(connectivity_file) as fp:
    for line in fp:
        bgl_v_name, net_name = line.rstrip().split(',')
        cell_inst, pin_name = bgl_v_name.split('/')
        bgl_vertices.append(bgl_v_name)
        v_dict[bgl_v_name] = len(v_dict)

        if net_name in n_dict:
            n_dict[net_name].append(bgl_v_name)
        else:
            n_dict[net_name] = [bgl_v_name]
        #arc edges
        if cell_inst in arc_dict:
            arc_dict[cell_inst].append(bgl_v_name)
        else:
            arc_dict[cell_inst] = [bgl_v_name]


with open(f'{basename}.vertices', 'w') as fv:
    for v in bgl_vertices:
        fv.write(f'{v}\n')


with open(f'{basename}.edges', 'w') as fe:
    for net_name, connected_pin_list in n_dict.items():
        output_pin = [ pin for pin in connected_pin_list if pin.endswith('/o') ]
        if not output_pin:
            print(f'Error: Unable to find driver pin for {net_name} : {connected_pin_list}\n')
        else:
            output_pin = output_pin[0]

            if net_name in net_Ceff_dict:
                opin_Ceff_dict[output_pin] = net_Ceff_dict[net_name]
            else:
                print(f'Err: {net_name} not found in Ceff')

            output_v = v_dict[output_pin]
            for input_pin in connected_pin_list:
                if input_pin != output_pin:
                    input_v = v_dict[input_pin]
                    fe.write(f'{input_v},{output_v}\n')
    print (f"------Cell Arcs -------\n");
    for cell_inst, arcs_list in arc_dict.items():
        output_arc_pin = [ pin for pin in arcs_list if pin.endswith('/o') ]
        if not output_arc_pin:
            print(f'Error: Unable to find output pin for {cell_inst} : {arc_list}\n')
        else:
            output_arc_pin = output_arc_pin[0]
            output_arc_v = v_dict[output_arc_pin]
            for input_arc_pin in arcs_list:
                if input_arc_pin != output_arc_pin:
                    input_arc_v = v_dict[input_arc_pin]
                    fe.write(f'{input_arc_v},{output_arc_v}\n')

#with open('n_dict.json', 'w') as fx:
#    json.dump(n_dict, fx, indent=4)
#with open('v_dict.json', 'w') as fx:
#    json.dump(v_dict, fx, indent=4)
#with open('arc_dict.json', 'w') as fx:
#    json.dump(arc_dict, fx, indent=4) 


with open(f'{basename}.pin.ceff', 'w') as fx:
    for k, v in opin_Ceff_dict.items():
        fx.write(f'{k},{v}\n')

#with open(f'{basename}.net.ceff', 'w') as fx:
#    for k, v in net_Ceff_dict.items():
#        fx.write(f'{k},{v}\n')
