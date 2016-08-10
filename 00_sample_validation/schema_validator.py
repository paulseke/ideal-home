#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
After auditing is complete the next step is to prepare the data to be inserted into a SQL database.
To do so you will parse the elements in the OSM XML file, transforming them from document format to
tabular format, thus making it possible to write to .csv files.  These csv files can then easily be
imported to a SQL database as tables.

The process for this transformation is as follows:
- Use iterparse to iteratively step through each top level element in the XML
- Shape each element into several data structures using a custom function
- Utilize a schema and validation library to ensure the transformed data is in the correct format
- Write each data structure to the appropriate .csv files

We've already provided the code needed to load the data, perform iterative parsing and write the
output to csv files. Your task is to complete the shape_element function that will transform each
element into the correct format. To make this process easier we've already defined a schema (see
the schema.py file in the last code tab) for the .csv files and the eventual tables. Using the 
cerberus library we can validate the output against this schema to ensure it is correct.

## Shape Element Function
The function should take as input an iterparse Element object and return a dictionary.

### If the element top level tag is "node":
The dictionary returned should have the format {"node": .., "node_tags": ...}

The "node" field should hold a dictionary of the following top level node attributes:
- id
- user
- uid
- version
- lat
- lon
- timestamp
- changeset
All other attributes can be ignored

The "node_tags" field should hold a list of dictionaries, one per secondary tag. Secondary tags are
child tags of node which have the tag name/type: "tag". Each dictionary should have the following
fields from the secondary tag attributes:
- id: the top level node id attribute value
- key: the full tag "k" attribute value if no colon is present or the characters after the colon if one is.
- value: the tag "v" attribute value
- type: either the characters before the colon in the tag "k" value or "regular" if a colon
        is not present.

Additionally,

- if the tag "k" value contains problematic characters, the tag should be ignored
- if the tag "k" value contains a ":" the characters before the ":" should be set as the tag type
  and characters after the ":" should be set as the tag key
- if there are additional ":" in the "k" value they and they should be ignored and kept as part of
  the tag key. For example:

  <tag k="addr:street:name" v="Lincoln"/>
  should be turned into
  {'id': 12345, 'key': 'street:name', 'value': 'Lincoln', 'type': 'addr'}

- If a node has no secondary tags then the "node_tags" field should just contain an empty list.

The final return value for a "node" element should look something like:

{'node': {'id': 757860928,
          'user': 'uboot',
          'uid': 26299,
       'version': '2',
          'lat': 41.9747374,
          'lon': -87.6920102,
          'timestamp': '2010-07-22T16:16:51Z',
      'changeset': 5288876},
 'node_tags': [{'id': 757860928,
                'key': 'amenity',
                'value': 'fast_food',
                'type': 'regular'},
               {'id': 757860928,
                'key': 'cuisine',
                'value': 'sausage',
                'type': 'regular'},
               {'id': 757860928,
                'key': 'name',
                'value': "Shelly's Tasty Freeze",
                'type': 'regular'}]}

### If the element top level tag is "way":
The dictionary should have the format {"way": ..., "way_tags": ..., "way_nodes": ...}

The "way" field should hold a dictionary of the following top level way attributes:
- id
-  user
- uid
- version
- timestamp
- changeset

All other attributes can be ignored

The "way_tags" field should again hold a list of dictionaries, following the exact same rules as
for "node_tags".

Additionally, the dictionary should have a field "way_nodes". "way_nodes" should hold a list of
dictionaries, one for each nd child tag.  Each dictionary should have the fields:
- id: the top level element (way) id
- node_id: the ref attribute value of the nd tag
- position: the index starting at 0 of the nd tag i.e. what order the nd tag appears within
            the way element

The final return value for a "way" element should look something like:

{'way': {'id': 209809850,
         'user': 'chicago-buildings',
         'uid': 674454,
         'version': '1',
         'timestamp': '2013-03-13T15:58:04Z',
         'changeset': 15353317},
 'way_nodes': [{'id': 209809850, 'node_id': 2199822281, 'position': 0},
               {'id': 209809850, 'node_id': 2199822390, 'position': 1},
               {'id': 209809850, 'node_id': 2199822392, 'position': 2},
               {'id': 209809850, 'node_id': 2199822369, 'position': 3},
               {'id': 209809850, 'node_id': 2199822370, 'position': 4},
               {'id': 209809850, 'node_id': 2199822284, 'position': 5},
               {'id': 209809850, 'node_id': 2199822281, 'position': 6}],
 'way_tags': [{'id': 209809850,
               'key': 'housenumber',
               'type': 'addr',
               'value': '1412'},
              {'id': 209809850,
               'key': 'street',
               'type': 'addr',
               'value': 'West Lexington St.'},
              {'id': 209809850,
               'key': 'street:name',
               'type': 'addr',
               'value': 'Lexington'},
              {'id': '209809850',
               'key': 'street:prefix',
               'type': 'addr',
               'value': 'West'},
              {'id': 209809850,
               'key': 'street:type',
               'type': 'addr',
               'value': 'Street'},
              {'id': 209809850,
               'key': 'building',
               'type': 'regular',
               'value': 'yes'},
              {'id': 209809850,
               'key': 'levels',
               'type': 'building',
               'value': '1'},
              {'id': 209809850,
               'key': 'building_id',
               'type': 'chicago',
               'value': '366409'}]}
"""
from collections import Counter # ADD THIS
#import StringIO # ADD THIS
import copy # ADD THIS

####################################################################

import csv
import codecs
import re
import xml.etree.cElementTree as ET

import cerberus

#import schema

OSM_PATH = "fredericton_sample.osm"

NODES_PATH = "fredericton_sample_nodes.csv"
NODE_TAGS_PATH = "fredericton_sample_nodes_tags.csv"
WAYS_PATH = "fredericton_sample_ways.csv"
WAY_NODES_PATH = "fredericton_sample_ways_nodes.csv"
WAY_TAGS_PATH = "fredericton_sample_ways_tags.csv"



LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

#SCHEMA = schema.Schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

# Note: The schema is stored in a .py file in order to take advantage of the
# int() and float() type coercion functions. Otherwise it could easily stored as
# as JSON or another serialized format.

SCHEMA = {
    'node': {
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'lat': {'required': True, 'type': 'float', 'coerce': float},
            'lon': {'required': True, 'type': 'float', 'coerce': float},
            'user': {'required': True, 'type': 'string'},
            'uid': {'required': True, 'type': 'integer', 'coerce': int},
            'version': {'required': True, 'type': 'string'},
            'changeset': {'required': True, 'type': 'integer', 'coerce': int},
            'timestamp': {'required': True, 'type': 'string'}
        }
    },
    'node_tags': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'required': True, 'type': 'string'},
                'value': {'required': True, 'type': 'string'},
                'type': {'required': True, 'type': 'string'}
            }
        }
    },
    'way': {
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'user': {'required': True, 'type': 'string'},
            'uid': {'required': True, 'type': 'integer', 'coerce': int},
            'version': {'required': True, 'type': 'string'},
            'changeset': {'required': True, 'type': 'integer', 'coerce': int},
            'timestamp': {'required': True, 'type': 'string'}
        }
    },
    'way_nodes': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'node_id': {'required': True, 'type': 'integer', 'coerce': int},
                'position': {'required': True, 'type': 'integer', 'coerce': int}
            }
        }
    },
    'way_tags': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'required': True, 'type': 'string'},
                'value': {'required': True, 'type': 'string'},
                'type': {'required': True, 'type': 'string', 'required': True}
            }
        }
    }
}


def shape_element(elem, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""
    print "SHAPE ELEMENT?:", elem.tag

    # single_element_maker(OSM_PATH, (get_element(OSM_PATH)).next())
    # element_maker_all(OSM_PATH)
    
    osm_file = OSM_PATH # WE MAY NEED TO CHANGE THIS 
    tag_get, path_nd, path_tag, all_id_elemts = all_tag_dict_builder(osm_file)
 
    if elem.tag == 'node':
        node_attribs = single_element_maker(osm_file, elem) 
        for each_tag in range(len(path_tag)):
            # return the array of tag elements associated to the key
            tags = [d for d in path_tag if d['id'] == (node_attribs['node'])['id']]            
            return {elem.tag: node_attribs[elem.tag], 'node_tags': tags}
            
    elif elem.tag == 'way':
        way_attribs = single_element_maker(osm_file, elem)
        for each_tag in range(len(path_tag)):
            # return the array of tag elements associated to the key
            tags = [d for d in path_tag if d['id'] == (way_attribs['way'])['id']]
        for each_node in range(len(path_nd)):
            way_nodes = [d for d in path_nd if d['id'] == (way_attribs['way'])['id']]            
            return {elem.tag: way_attribs[elem.tag], 'way_nodes': way_nodes, 'way_tags': tags}


        
            
############################# MY SUPPORT FUNCTIONS #################################

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


def tag_filter(tag_element):
    tag_dict = tag_element.attrib
    default_tag_type = 'regular'
    if assertion_try_dict(tag_dict,'type'):
        ta_ty = tag_dict['type']
        
    elif (re.match(LOWER_COLON, tag_dict['k']) != None):
        a = str(tag_dict['k'])
        ta_ty = a[0 : a.find(':')]
        ta_ke = a[a.find(':') + 1 :]
        
    elif (re.match(PROBLEMCHARS, tag_dict['k']) != None):
        ta_ke = [] # ignored for me means not included
    else:
        ta_ty = default_tag_type
        ta_ke = tag_dict['k']

    return {'id': 0, 'key': ta_ke, 'value': tag_dict['v'], 'type': ta_ty}


def single_element_maker(osm_file, major_element):
    # makes int and float and removes 'version'
    # from 'node', 'way' or 'relation
    # certify that element.tag is either node, way or relation
    if assertion_try_dict(major_element.attrib, 'id'):        
        if str(major_element.attrib['id']).isdigit():
            major_element.attrib['id'] = int(major_element.attrib['id'])
        else:
            major_element.attrib['id'] = []    
        if str(major_element.attrib['uid']).isdigit():
            major_element.attrib['uid'] = int(major_element.attrib['uid'])
        else:
            major_element.attrib['uid'] = []
        if str(major_element.attrib['changeset']).isdigit():
            major_element.attrib['changeset'] = int(major_element.attrib['changeset'])
        else:
            major_element.attrib['changeset'] = []
        # certify that it is a node
        if assertion_try(major_element,'lat'):            
            if is_float_try(major_element,'lat'):
                major_element.attrib['lat'] = float(major_element.attrib['lat'])
            else:
                major_element.attrib['lat'] = []
            if is_float_try(major_element, 'lon'):
                major_element.attrib['lon'] = float(major_element.attrib['lon'])
            else:
                major_element.attrib['lon'] = []
            # for nodes without 'visible' key
            if assertion_try(major_element,'visible'):
                return {major_element.tag:
                        remove_dict_key(major_element.attrib, 'visible'),
                        'node_tags': []}
            else:
                return {major_element.tag: major_element.attrib, 'node_tags': []}       
        else:
            # thus, if a way or a relation
            if assertion_try(major_element,'visible'):
                return {major_element.tag:
                        remove_dict_key(major_element.attrib, 'visible'),
                        'node_tags': []}
            else:
                return {major_element.tag: major_element.attrib, 'node_tags': []}


def count_tags(osm_file):
    # returns an array of arrays with id for tag and nd elements
    path_way = []
    tag_get = []
    nd_get = []
    tags = ("node", "way", "relation", "nd", "tag")
    
    for event, element in ET.iterparse(osm_file, events=("start", "end",)):
        if event == 'start':
            if element.tag in tags:                
                if assertion_try(element,'id'):
                    collector_way = (element.tag, int(element.attrib['id']))
                    path_way.append(collector_way)                
                else:
                    collector_way = [element.tag, 'OK']
                    path_way.append(collector_way)
        # Adding 'id' to tags and nd
        for i in range(len(path_way) - 1):
            if (path_way[i])[0] != (path_way[i+1])[0]:
                if (path_way[i])[0] == 'node':
                    if (path_way[i+1])[0] == 'tag':
                        (path_way[i+1])[1] = [(path_way[i])[1], 'node']
                elif (path_way[i])[0] == 'way':
                    if (path_way[i+1])[0] == 'tag':
                        (path_way[i+1])[1] = [(path_way[i])[1], 'way']
                    elif (path_way[i+1])[0] == 'nd':
                        (path_way[i+1])[1] = [(path_way[i])[1], 'way']
                elif (path_way[i])[0] == 'relation':
                    if (path_way[i+1])[0] == 'tag':
                        (path_way[i+1])[1] = [(path_way[i])[1], 'relation'] 
        for i in range(len(path_way) - 1):
            if (path_way[i])[0] == (path_way[i+1])[0]:
                if (path_way[i])[0] == 'tag':
                    (path_way[i+1])[1] = (path_way[i])[1]
                elif (path_way[i])[0] == 'nd':
                    (path_way[i+1])[1] = (path_way[i])[1]
            elif (path_way[i])[0] == 'nd' and (path_way[i+1])[0] == 'tag':
                (path_way[i+1])[1] = (path_way[i])[1]
            elif (path_way[i])[0] == 'tag' and (path_way[i+1])[0] == 'nd':
                (path_way[i+1])[1] = (path_way[i])[1]
    # extracts all tag and nd with id
    for i in range(len(path_way)):
        if (path_way[i])[0] == 'tag':
            tagg = path_way[i]
            tag_get.append(tagg)
        elif (path_way[i])[0] == 'nd':
            tagg_nd = path_way[i]
            nd_get.append(tagg_nd)
                   
    return path_way, tag_get, nd_get

        
def all_tag_dict_builder(osm_file):
    # get position counts for nd elements
    counter = 0
    nd_counts = []
    data = []
    path = []
    path_tag = []
    path_nd = []
    path_way, tag_get, nd_get = count_tags(osm_file)############### KIL THIS
    strg = str(nd_get)
    default_tag_type = 'regular'
    
    position = [m.start() for m in re.finditer("nd", strg)]
    for j in range(len(position)):
        start = strg.find("[", position[j]) + 1
        end = strg.find("'", start) - 2
        datum = strg[start: end]
        data.append(datum)        

    words = Counter(data).keys() # equals to list(set(words))    
    counts = Counter(data).values() # counts the elements' frequency

    for i in range(len(words)):
        for j in range(len(data)):
            if data[j] == words[i]:
                count_unit = (words[i], counter)
                nd_counts.append(count_unit)
                counter += 1
            else:
                counter = 0
    
    # get all upper tag id (e.g. 'node') and attribute to nd and tag elements
    # get 'type' for tag elements 
    
    for event, element in ET.iterparse(osm_file, events=("start", "end",)):
        if event == 'start':
            if element.tag == "node" or element.tag == "way" or element.tag == "relation":
                path.append(element.attrib['id'])
            if element.tag == "tag":                
                if assertion_try(element,'type'):
                    ta_ty = element.attrib['type']
                elif (re.match(PROBLEMCHARS, element.attrib['k']) != None):
                    ta_ke = [] # to be ignored, so not included
                elif (re.match(LOWER_COLON, element.attrib['k']) != None):
                    a = str(element.attrib['k'])
                    ta_ty = a[0 : a.find(':')]
                    ta_ke = a[a.find(':') + 1 :]
                else:
                    ta_ty = default_tag_type
                    ta_ke = element.attrib['k']
                collector_tag = {'id': 0, 'key': ta_ke,
                                 'value': element.attrib['v'], 'type': ta_ty}
                path_tag.append(collector_tag)
                
            if element.tag == "nd":
                if element.attrib['ref'].isdigit():
                    nD_re = int(element.attrib['ref'])
                else:
                    nD_re = []
                collector_nd = {'id': 0, 'node_id': nD_re, 'position': 0}                
                path_nd.append(collector_nd)

        for i in range(len(path_tag)):
            (path_tag[i])['id'] = ((tag_get[i])[1])[0]

        for i in range(len(path_nd)):
            (path_nd[i])['id'] = ((nd_get[i])[1])[0]

        for i in range(len(path_nd)):
            (path_nd[i])['position'] = (nd_counts[i])[1]
    print "all elements:", path
    return tag_get, path_nd, path_tag, path

           
####################################################################################



# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_strings = (
            "{0}: {1}".format(k, v if isinstance(v, str) else ", ".join(v))
            for k, v in errors.iteritems()
        )
        raise cerberus.ValidationError(
            message_string.format(field, "\n".join(error_strings))
        )
    


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
            


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        print "printing headers"
        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    print "in the loop:", element.tag
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    print "in the loop:", element.tag
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])
                    
                    
        print 'The following is over:', OSM_PATH


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    print "let's go"
    process_map(OSM_PATH, validate=True)
