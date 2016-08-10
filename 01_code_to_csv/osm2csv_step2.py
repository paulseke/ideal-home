# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 18:25:44 2016

@author: paul
"""
##0
##NODES_PATH = "nodes.csv"
##NODE_TAGS_PATH = "nodes_tags.csv"
##1
##NODES_PATH = "durban_nodes.csv"
##NODE_TAGS_PATH = "durban_nodes_tags.csv"
##2
NODES_PATH = "fredericton_nodes.csv"
NODE_TAGS_PATH = "fredericton_nodes_tags.csv"
##3
##NODES_PATH = "halifax_nodes.csv"
##NODE_TAGS_PATH = "halifax_nodes_tags.csv"
##4
#NODES_PATH = "quebec_nodes.csv"
#NODE_TAGS_PATH = "quebec_nodes_tags.csv"
##5
##NODES_PATH = "lausanne_nodes.csv"
##NODE_TAGS_PATH = "lausanne_nodes_tags.csv"
##6
##NODES_PATH = "nairobi_nodes.csv"
##NODE_TAGS_PATH = "nairobi_nodes_tags.csv"
##7
##NODES_PATH = "saint_louis_nodes.csv"
##NODE_TAGS_PATH = "saint_louis_nodes_tags.csv"
##8
##NODES_PATH = "turin_nodes.csv"
##NODE_TAGS_PATH = "turin_nodes_tags.csv"
##9
##NODES_PATH = "verona_nodes.csv"
##NODE_TAGS_PATH = "verona_nodes_tags.csv"


inputcsv1 = "node_fields.csv"
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
    # array of tag elements associated to the key
    # return the array of tag elements associated to the key
    tags = [d for d in all_tag if d['id'] == major_attrib['id']]
    return {major_attrib['el_tag']: major_attribs, 'node_tags': tags}


# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']


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

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        
        nodes_writer.writeheader()
        node_tags_writer.writeheader()

        for el in csv_opener(inputcsv1): 
##            if assertion_try_dict(el, 'el_tag'):
##                if el['el_tag'] == 'node':
            el_attrib = get_nd_and_tags(el)
            nodes_writer.writerow(el_attrib['node'])
            node_tags_writer.writerows(el_attrib['node_tags'])
                    
        print 'All node elements created'


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    print "Let's process:", NODES_PATH
    process_map()


