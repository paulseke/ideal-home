# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 17:10:50 2016

@author: paul
"""

inputcsv = "path_way_base.csv" # CHANGE ME

import csv
#from collections import Counter # ADD THIS
import copy # ADD THIS
import ast
####################################################################

import affinity
import multiprocessing
affinity.set_process_affinity_mask(0,8**multiprocessing.cpu_count()-1)

def remove_dict_key(elem, key):
    # removes a key without mutating the dictionary    
    new_element = copy.deepcopy(elem)
    del new_element[key]
    return new_element


def csv_opener(inputcsv):
    ''' the name should be a str'''
    data = []
    data_transf = []
    with open(inputcsv, "rb") as f:
        datum = csv.reader(f)
        for row in datum:
            data.append(row)
        
        for i in range(len(data)):
            row_ok = ast.literal_eval(data[i][0])
            data_transf.append(row_ok)
        
        return data_transf


def tag_id_adder(inputcsv):
    # Adding 'id' to tags and nd
    path_way = csv_opener(inputcsv)    
    # Adding 'id' to tags and nd and parsing path_way
    tags_major = {'node', 'way', 'relation'}
    for i in range(len(path_way) - 1):
        if path_way[i]['el_tag'] != path_way[i+1]['el_tag']:
            if path_way[i]['el_tag'] in tags_major:
                if path_way[i+1]['el_tag'] == 'tag':
                    path_way[i+1]['id'] = path_way[i]['id']
                if path_way[i+1]['el_tag'] == 'nd':
                    path_way[i+1]['id'] = path_way[i]['id']
                    
    for i in range(len(path_way) - 1):
        if path_way[i]['el_tag'] == 'nd' and path_way[i+1]['el_tag'] == 'tag':
                path_way[i+1]['id'] = path_way[i]['id']
        elif path_way[i]['el_tag'] == path_way[i+1]['el_tag']:            
            if path_way[i+1]['el_tag'] == 'tag' or path_way[i+1]['el_tag'] == 'nd':
                path_way[i+1]['id'] = path_way[i]['id']
##            elif path_way[i+1]['el_tag'] == 'nd' and path_way[i]['el_tag'] == 'tag':
##                path_way[i+1]['id'] = path_way[i]['id']           
    return path_way 



def nd_counter(all_nd):
    # get position counts for nd elements
    counter = 0
    all_nd.append(all_nd[len(all_nd) - 1]) # appends a copy of last element (same id)
    
    for i in range(len(all_nd)-1):
        if all_nd[i]['id'] == all_nd[i+1]['id']:
            all_nd[i]['position'] = counter
            all_nd[i] = [all_nd[i]] 
            counter += 1
        else:
            all_nd[i]['position'] = 0       
            all_nd[i] = [all_nd[i]]
            counter = 1
    
    return all_nd


def tag_separator(inputcsv):
    path_way = tag_id_adder(inputcsv)
    node_fields = [] 
    way_fields = [] 
    all_tag = [] 
    all_nd = []        
    # extracts groups of node+way, tag and nd
    # not relation, not requested
    for i in range(len(path_way)):
        if path_way[i]['el_tag'] == 'node':
            node_field = path_way[i]
            node_fields.append([node_field]) 
        elif path_way[i]['el_tag'] == 'way':
            way_field = path_way[i]
            way_fields.append([way_field]) 
        elif path_way[i]['el_tag'] == 'tag':
            tagg_tag = path_way[i]
            all_tag.append([remove_dict_key(tagg_tag, 'el_tag')])  
        elif path_way[i]['el_tag'] == 'nd':
            tagg_nd = path_way[i]
            all_nd.append(remove_dict_key(tagg_nd, 'el_tag'))          
    
    return node_fields, way_fields, all_tag, all_nd    


def print_it(output_csv, file_to_print):
    with open(output_csv, "w") as f:
        writer = csv.writer(f)
        writer.writerows(file_to_print)
        
def csv_printing(inputcsv):
    node_fields, way_fields, all_tag, all_nd = tag_separator(inputcsv)       
    nd_mod = nd_counter(all_nd)
    del nd_mod[-1] # removes last element
    
    print "creating some CSVs..."
    print_it("node_fields.csv", node_fields)
    print_it("way_fields.csv", way_fields)            
    print_it("all_tag.csv", all_tag)
    print_it("all_nd.csv", nd_mod)

    print "Now run osm2csv_step2.py & osm2csv_step2b.py from the same directory, in 2 IDEs"        

if __name__ == '__main__':
    csv_printing(inputcsv)
