# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 13:58:58 2016

@author: seke
"""

import sqlite3
import sqlalchemy
# opening database connection or creating database
db = 'the9cities.db'
conn = sqlite3.connect(db)
cursor = conn.cursor()
print "Database {db} opened successfully".format(**vars())
# drop tables if they exist
cursor.execute("DROP TABLE IF EXISTS {NODE_TABLE}".format(**vars()))
cursor.execute("DROP TABLE IF EXISTS {WAY_TABLE}".format(**vars()))
cursor.execute("DROP TABLE IF EXISTS {NODE_TAG_TABLE}".format(**vars()))
cursor.execute("DROP TABLE IF EXISTS {WAY_TAG_TABLE}".format(**vars()))
cursor.execute("DROP TABLE IF EXISTS {WAY_NODE_TABLE}".format(**vars()))

# creates tables into the database
conn.execute('''CREATE TABLE {NODE_TABLE} (NodeId INTEGER PRIMARY KEY NOT NULL, Latitude REAL,
               Longitude REAL, Username TEXT, UserId INTEGER,
               Version INTEGER, Changeset TEXT, Timestamp TEXT);'''.format(**vars()))
conn.execute('''CREATE TABLE {WAY_TABLE} (WayId INTEGER PRIMARY KEY NOT NULL, Username TEXT, 
              UserId INTEGER, Version INTEGER, Changeset TEXT, Timestamp TEXT);'''.format(**vars()))

conn.commit()
print "Tables {NODE_TABLE} and {WAY_TABLE} created successfully".format(**vars())

# adding other tables

sql1 = '''CREATE TABLE {NODE_TAG_TABLE} (NodeId INTEGER NOT NULL, Key TEXT, 
        Value TEXT NOT NULL, Type TEXT,
        FOREIGN KEY (NodeId) REFERENCES {NODE_TABLE} (NodeId) 
        ON DELETE NO ACTION ON UPDATE NO ACTION);'''.format(**vars())

cursor.execute(sql1)

sql1 = ("CREATE INDEX {NODE_TAG_TABLE}_id ON {NODE_TAG_TABLE}(NodeId, Value);".format(**vars()))
cursor.execute(sql1)


sql2 = '''CREATE TABLE {WAY_TAG_TABLE} (WayId INTEGER NOT NULL, Key TEXT, 
          Value TEXT NOT NULL, Type TEXT,
          FOREIGN KEY (WayId) REFERENCES {WAY_TABLE} (WayId) 
          ON DELETE NO ACTION ON UPDATE NO ACTION);'''.format(**vars())
cursor.execute(sql2)

sql2 = ("CREATE INDEX {WAY_TAG_TABLE}_id ON {WAY_TAG_TABLE}(WayId, Value);".format(**vars()))
cursor.execute(sql2)


sql3 = '''CREATE TABLE {WAY_NODE_TABLE} (WayId INTEGER NOT NULL, 
          WayNodeId INTEGER NOT NULL, Position INTEGER,
          FOREIGN KEY (WayId) REFERENCES {WAY_TABLE} (WayId) 
          ON DELETE NO ACTION ON UPDATE NO ACTION);'''.format(**vars())
cursor.execute(sql3)

sql3 = ("CREATE INDEX {WAY_NODE_TABLE}_id ON {WAY_NODE_TABLE}(WayId, WayNodeId);".format(**vars()))
cursor.execute(sql3)

conn.commit()
print "Tables {NODE_TAG_TABLE}, {WAY_TAG_TABLE} and {WAY_NODE_TABLE} created successfully".format(**vars())

conn.close()
print "{db} closed".format(**vars())

