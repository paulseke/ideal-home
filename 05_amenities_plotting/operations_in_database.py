# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 17:40:22 2016

@author: seke
"""

# opening database connection
import sqlite3

db = 'the9cities.db'
conn = sqlite3.connect(db)
cursor = conn.cursor()
print "Database {db} opened successfully".format(**vars())


city = 'Fredericton'
city_node_tag = "fredericton_node_tag"
city_node = "fredericton_node"
city_way_tag = "fredericton_way_tag"
city_way = "fredericton_way"

# Amenities present in the node table
print_full(amenities_viewer(city_node_tag))


# Choosing amenities of interest
import pandas as pd
needed_values = ('restaurant', 'Restaurant','hospital', 
                 'school', 'clinic', 'doctors', 'kindergarten', 
                 'fire_station', 'police', 'parking')

# Grouping amenities of interest
restaurants = ('restaurant', 'Restaurant') 
# In Durban, one case of Restaurant instead of restaurant
kids_schools = ('school', 'kindergarten','School', 'Kindergarten',)
hospitals = ('hospital', 'clinic', 
             'doctors','Hospital', 'Clinic', 'Doctors')
police_fire_fighters = ('fire_station', 'police')


# Amenities of interest and number in the node table
amenities_of_interest_viewer(city_node_tag, needed_values)


# creating df of amenities of interest
restaurants_df, schools_df, hospitals_df, police_firefighters_df, parkings_df = amenities_df(city_node_tag, city_node)

#plotting the amenities of interest
city_fig_number = 1
legend_position =  'lower left'
x_lim = [-66.755, -66.556]
y_lim = [45.92, 46]
plotter(city, city_fig_number, legend_position, x_lim, y_lim)

# Let's list the way tags
leisure_land_viewer(city_way_tag)

# parks and related array
needed_places = ('dog_park', 'recreation_ground', 'playground', 'sports_centre', 'garden')
# creating the data pd series
pd_series = lands_pd_maker(city, city_way_tag, city_way, needed_places)
# plotting them
city_fig_number = city_fig_number + 1
title = 'Park and related grounds'
ylabel = 'number per km2'
y_lim = [0, 10]
fig_size = [4, 3]
pandas_plotter(pd_series, city_fig_number, title, ylabel, y_lim, fig_size)


# closing the database
conn.close()
print "{db} is closed".format(**vars())

