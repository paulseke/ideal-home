# -*- coding: utf-8 -*-
"""
Headers for Senegalese city Saint Louis
Created on Fri Aug  5 13:17:59 2016
@author: seke
"""
import pandas as pd

NODE_TABLE = "st_louis_node"
NODE_TAG_TABLE = "st_louis_node_tag"
WAY_TABLE = "st_louis_way"
WAY_NODE_TABLE = "st_louis_way_node"
WAY_TAG_TABLE = "st_louis_way_tag"
##7
NODES_PATH = "saint_louis_nodes.csv"
NODE_TAGS_PATH = "saint_louis_nodes_tags.csv"
WAYS_PATH = "saint_louis_ways.csv"
WAY_NODES_PATH = "saint_louis_ways_nodes.csv"
WAY_TAGS_PATH = "saint_louis_ways_tags.csv"
print "opened {NODES_PATH} and related, no other city needed at this time go to next section".format(**vars())


# open csv file as pandas dataframe with the same headers as the database tables to create
nodes_df = pd.read_csv(NODES_PATH, encoding='latin1', skiprows  = 1, 
                       names = ["NodeId", "Latitude", "Longitude", "Username", 
                                "UserId", "Version", "Changeset", "Timestamp"])
print "{NODES_PATH}, opened".format(**vars())
node_tags_df = pd.read_csv(NODE_TAGS_PATH, encoding='latin1', skiprows  = 1, 
                           names = ["NodeId", "Key", "Value", "Type"])
print "{NODE_TAGS_PATH}, opened".format(**vars())
ways_df = pd.read_csv(WAYS_PATH, encoding='latin1', skiprows  = 1, 
                      names = ["WayId", "Username", "UserId", "Version", 
                               "Changeset", "Timestamp"])
print "{WAYS_PATH}, opened".format(**vars())
ways_tags_df = pd.read_csv(WAY_TAGS_PATH, encoding='latin1', skiprows  = 1, 
                           names = ["WayId", "Key", "Value", "Type"])
print "{WAY_TAGS_PATH}, opened".format(**vars())
way_nodes_df = pd.read_csv(WAY_NODES_PATH, encoding='latin1', skiprows  = 1, 
                           names = ["WayId", "WayNodeId", "Position"])
print "{WAY_NODES_PATH}, opened".format(**vars())



