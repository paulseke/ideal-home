# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 13:52:08 2016

@author: seke
"""


def header_type_verifier(inputcsv_df):
    '''prints headers, data types and summary'''
    print "header:"
    print inputcsv_df[0:3]
    print ""
    print "data in a nutshell:"
    print inputcsv_df.describe()
    print ""
    print "data types:"
    print inputcsv_df.dtypes
    print ""
    print "proportion of null values:"
    null_val = (pd.isnull(inputcsv_df) == True).sum()
    print null_val / (null_val + (pd.isnull(inputcsv_df) != True).sum())


# getting a fill of the data
print "please check the following data"
print ""
print "nodes_df:"
header_type_verifier(nodes_df)
print ""
print "node_tags_df:"
header_type_verifier(node_tags_df)
print ""
print "ways_df:"
header_type_verifier(ways_df)
print ""
print "ways_tags_df:"
header_type_verifier(ways_tags_df)
print ""
print "way_nodes_df:"
header_type_verifier(way_nodes_df)