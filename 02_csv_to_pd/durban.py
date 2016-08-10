# -*- coding: utf-8 -*-
"""
Headers for South African city Durban
Created on Fri Aug  5 13:17:59 2016
@author: seke
"""
import pandas as pd

NODE_TABLE = "durban_node"
NODE_TAG_TABLE = "durban_node_tag"
WAY_TABLE = "durban_way"
WAY_NODE_TABLE = "durban_way_node"
WAY_TAG_TABLE = "durban_way_tag"
##1
NODES_PATH = "durban_nodes.csv"
NODE_TAGS_PATH = "durban_nodes_tags.csv"
WAYS_PATH = "durban_ways.csv"
WAY_NODES_PATH = "durban_ways_nodes.csv"
WAY_TAGS_PATH = "durban_ways_tags.csv"



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

