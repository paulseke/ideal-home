# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 18:25:44 2016

@author: paul
"""
##0
##WAYS_PATH = "ways.csv"
##WAY_NODES_PATH = "ways_nodes.csv"
##WAY_TAGS_PATH = "ways_tags.csv"
##1
##WAYS_PATH = "durban_ways.csv"
##WAY_NODES_PATH = "durban_ways_nodes.csv"
##WAY_TAGS_PATH = "durban_ways_tags.csv"
##2
WAYS_PATH = "fredericton_ways.csv"
WAY_NODES_PATH = "fredericton_ways_nodes.csv"
WAY_TAGS_PATH = "fredericton_ways_tags.csv"
##3
##WAYS_PATH = "halifax_ways.csv"
##WAY_NODES_PATH = "halifax_ways_nodes.csv"
##WAY_TAGS_PATH = "halifax_ways_tags.csv"
##4
#WAYS_PATH = "quebec_ways.csv"
#WAY_NODES_PATH = "quebec_ways_nodes.csv"
#WAY_TAGS_PATH = "quebec_ways_tags.csv"
##5
##WAYS_PATH = "lausanne_ways.csv"
##WAY_NODES_PATH = "lausanne_ways_nodes.csv"
##WAY_TAGS_PATH = "lausanne_ways_tags.csv"
##6
##WAYS_PATH = "nairobi_ways.csv"
##WAY_NODES_PATH = "nairobi_ways_nodes.csv"
##WAY_TAGS_PATH = "nairobi_ways_tags.csv"
##7
##WAYS_PATH = "saint_louis_ways.csv"
##WAY_NODES_PATH = "saint_louis_ways_nodes.csv"
##WAY_TAGS_PATH = "saint_louis_ways_tags.csv"
##8
##WAYS_PATH = "turin_ways.csv"
##WAY_NODES_PATH = "turin_ways_nodes.csv"
##WAY_TAGS_PATH = "turin_ways_tags.csv"
##9
##WAYS_PATH = "verona_ways.csv"
##WAY_NODES_PATH = "verona_ways_nodes.csv"
##WAY_TAGS_PATH = "verona_ways_tags.csv"



inputcsv1 = "way_fields.csv"
inputcsv2 = "all_tag.csv"
inputcsv3 = "all_nd.csv"

import csv
import copy 
import ast
import codecs
import affinity
import multiprocessing
affinity.set_process_affinity_mask(0,8**multiprocessing.cpu_count()-1)


def assertion_try_dict(dictionary, tested_str):
    try:
        dictionary[tested_str]
        return True
    except KeyError:
        return False

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


all_tag = csv_opener(inputcsv2)
all_nd = csv_opener(inputcsv3)

def get_nd_and_tags(major_attrib):
    major_attribs = remove_dict_key(major_attrib, 'el_tag')
    tags = [d for d in all_tag if d['id'] == major_attrib['id']]
    # array of tag elements associated to the key
    tags = [d for d in all_tag if d['id'] == major_attrib['id']]
    # array of nd elements associated to the key
    way_nodes = [d for d in all_nd if d['id'] == major_attrib['id']]

    return {major_attrib['el_tag']: major_attribs, 'way_nodes': way_nodes, 'way_tags': tags}



# Make sure the fields order in the csvs matches the column order in the sql table schema
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']



class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
            


def process_map():
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)
        
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        for el in csv_opener(inputcsv1): 
##            if assertion_try_dict(el, 'el_tag'):
##                if el['el_tag'] == 'way':
            el_attrib = get_nd_and_tags(el)
            ways_writer.writerow(el_attrib['way'])
            way_nodes_writer.writerows(el_attrib['way_nodes'])
            way_tags_writer.writerows(el_attrib['way_tags'])
                                        
        print 'All way elements created'


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    print "Let's process:", WAYS_PATH
    process_map()

