# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 14:01:44 2016

@author: seke
"""
import sqlite3
from sqlalchemy import create_engine


def csv_data_appender(table_name, df):
    df.to_sql(table_name, engine, if_exists='append', index = False)
    #Session.commit()
    print "created successfully, table:", table_name


# opening database connection or creating database
engine = create_engine('sqlite:///the9cities.db', echo=False)
print "Database {db} re-opened successfully".format(**vars())

# adding tables and data to the database
csv_data_appender(NODE_TABLE, nodes_df)
csv_data_appender(NODE_TAG_TABLE, node_tags_df)
csv_data_appender(WAY_TABLE, ways_df)
csv_data_appender(WAY_NODE_TABLE, way_nodes_df)
csv_data_appender(WAY_TAG_TABLE, ways_tags_df)

# closing database connection
conn.close()
print "database {db} closed".format(**vars())
print "PLEASE GO OVER AND ADD ANOTHER CITY TO THE DATABASE"