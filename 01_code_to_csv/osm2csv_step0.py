# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 16:56:06 2016

@author: paul
"""

from collections import Counter # ADD THIS
#import StringIO # ADD THIS
import copy # ADD THIS

####################################################################

import csv
# import codecs
import re
import xml.etree.cElementTree as ET

import affinity
import multiprocessing
affinity.set_process_affinity_mask(0,8**multiprocessing.cpu_count()-1)


##0
OSM_PATH = "fredericton_sample.osm"
##1
#OSM_PATH = "durban_south-africa.osm"
##2
#OSM_PATH = "fredericton_canada.osm"
##3
##OSM_PATH = "halifax_canada.osm"##OSM_PATH = "quebec_canada.osm"
##4
##OSM_PATH = "quebec_canada.osm"
##5
##OSM_PATH = "lausanne_switzerland.osm"
##6
##OSM_PATH = "nairobi_kenya.osm"
##7
##OSM_PATH = "saint-louis_senegal.osm"
##8
##OSM_PATH = "turin_italy.osm"
##9
##OSM_PATH = "verona_italy.osm"




LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

#SCHEMA = schema.Schema

def is_float_try(element, tested_str):
    try:
        float(element.attrib['lat'])
        return True
    except ValueError:
        return False


def assertion_try_dict(dictionary, tested_str):
    try:
        dictionary[tested_str]
        return True
    except KeyError:
        return False


def assertion_try(element, tested_str):
    try:
        element.attrib[tested_str]
        return True
    except KeyError:
        return False


def remove_dict_key(elem, key):
    # removes a key without mutating the dictionary    
    new_element = copy.deepcopy(elem)
    del new_element[key]
    return new_element


def type_and_key_parser(element):
    '''parses tag type from element k'''
    LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
    PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
    default_tag_type = 'regular'
    
    if assertion_try(element,'k'):
        if (re.match(LOWER_COLON, element.attrib['k']) != None):
            strg = str(element.attrib['k'])
            tag_type = strg[: strg.find(':')]
            tag_key = strg[strg.find(':') + 1 :]
            
        elif (re.match(PROBLEMCHARS, element.attrib['k']) != None):
            tag_key = [] # ignored for me means not included
            
        else:
            tag_type = default_tag_type
            tag_key = element.attrib['k']
            
    return tag_type, tag_key


def element_attrib_check(element, key):
    '''asserts for the existence of the key'''
    if assertion_try_dict(element.attrib, key):
        attribute_key_value = element.attrib[key]
    else:
        attribute_key_value = []
        
    return attribute_key_value


def float_tester_converter(element, key):
    '''asserts key existence and convert to float'''
    if assertion_try(element, key):            
        if is_float_try(element, key):
            attribute_key_value = float(element.attrib[key])
        else:
            attribute_key_value = []
    else:
        attribute_key_value = []
        
    return attribute_key_value


def digit_tester_converter(element, key):
    '''asserts key existence and converts to int'''
    if assertion_try_dict(element.attrib, key):
        if str(element.attrib[key]).isdigit():
            attribute_key_value = int(element.attrib[key])
        else:
            attribute_key_value = []
    else:
        attribute_key_value = []

    return attribute_key_value


def single_element_processor(element):
    '''returns an array of array of an element attributes'''    
    if element.tag == 'node':
        major_id = digit_tester_converter(element, 'id')            
        major_uid = digit_tester_converter(element, 'uid')            
        major_changeset = digit_tester_converter(element, 'changeset')              
        major_timestamp = element_attrib_check(element, 'timestamp')
        major_version = element_attrib_check(element, 'version')
        major_user = element_attrib_check(element, 'user')            
        node_lat = float_tester_converter(element, 'lat')
        node_lon = float_tester_converter(element, 'lon')
        return {'el_tag': element.tag, 'id': major_id, 'lat': node_lat, 'lon': node_lon,
                'user': major_user, 'uid': major_uid, 'version': major_version,
                'changeset': major_changeset, 'timestamp': major_timestamp}
        
    elif element.tag == 'way':
        major_id = digit_tester_converter(element, 'id')            
        major_uid = digit_tester_converter(element, 'uid')            
        major_changeset = digit_tester_converter(element, 'changeset')              
        major_timestamp = element_attrib_check(element, 'timestamp')
        major_version = element_attrib_check(element, 'version')
        major_user = element_attrib_check(element, 'user')            
        return {'el_tag': element.tag, 'id': major_id, 'user': major_user,
                'uid': major_uid, 'version': major_version,
                'changeset': major_changeset, 'timestamp': major_timestamp}
    
    elif element.tag == 'relation':
        major_id = digit_tester_converter(element, 'id') 
        return {'el_tag': element.tag, 'id': major_id}
        
    elif element.tag == 'nd':
        nd_ref = element_attrib_check(element, 'ref')
        return {'el_tag': element.tag, 'id': 'way_id',
                'node_id': nd_ref, 'position': 'add_position'}

    elif element.tag == 'tag':
        tag_value = element_attrib_check(element, 'v')
        tag_type, tag_key = type_and_key_parser(element)
        return {'el_tag': element.tag, 'id': 'node_way_rel_id', 'key': tag_key,
                'value': tag_value, 'type': tag_type}
            


def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'start' and elem.tag in tags:
            yield elem
            root.clear()




def pathway_builder(osm_file):
    # returns an array of arrays with id for tag and nd elements
    path_way = []
    tags = ['node', 'way', 'relation', 'nd', 'tag']
    for element in get_element(osm_file, tags):
        elmt = single_element_processor(element)
        path_way.append([elmt])
        #return path_way        

    with open("path_way_base.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(path_way)
                
    print "Now run osm2csv_step1.py from the same directory"

if __name__ == '__main__':
    pathway_builder(OSM_PATH)

