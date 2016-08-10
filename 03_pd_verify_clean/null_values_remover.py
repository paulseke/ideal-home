# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 13:54:55 2016

@author: seke
"""
import pandas as pd

def null_values_remover(inputcsv_df, column_name):
    '''drops eventual null values from NON NULL columns'''
    return inputcsv_df[pd.notnull(inputcsv_df[column_name])]


# remove null values in Non Null columns, if any
nodes_df = null_values_remover(nodes_df, 'NodeId')
print "nodes_df is clean"
node_tags_df = null_values_remover(node_tags_df, 'NodeId')
node_tags_df = null_values_remover(node_tags_df, 'Value')
print "node_tags_df is clean"
ways_df = null_values_remover(ways_df, 'WayId')
print "ways_df is clean"
ways_tags_df = null_values_remover(ways_tags_df, 'WayId')
ways_tags_df = null_values_remover(ways_tags_df, 'Value')
print "ways_tags_df is clean"
way_nodes_df = null_values_remover(way_nodes_df, 'WayId')
way_nodes_df = null_values_remover(way_nodes_df, 'WayNodeId')
print "way_nodes_df is clean"