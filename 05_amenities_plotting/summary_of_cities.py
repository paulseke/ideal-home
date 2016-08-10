# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 18:09:17 2016

@author: seke
"""


# opening database connection
import sqlite3

db = 'the9cities.db'
conn = sqlite3.connect(db)
cursor = conn.cursor()
print "Database {db} opened successfully".format(**vars())


# Some helpful functions

# exports amenities in group of interest
def service_builder_list(amenity_list, city_node_tag, city_node):
    cursor.execute('''SELECT Value, Latitude, Longitude FROM {city_node_tag}  
    JOIN {city_node} ON {city_node}.NodeId = {city_node_tag}.NodeId
    WHERE Key = 'amenity' AND Value in {amenity_list} 
    Group BY Latitude  ORDER BY Longitude;'''.format(**vars()))
    return pd.DataFrame(cursor.fetchall(), columns = ('key', 'latitude', 'longitude'))

# collects amenities of interest in DataFrames
def amenities_df_reduced(city_node_tag, city_node):
    # collecting restaurants
    restaurants_df = service_builder_list(restaurants, city_node_tag, city_node)
    # collecting kids' schools
    schools_df = service_builder_list(kids_schools, city_node_tag, city_node)
    # collecting hospitals
    hospitals_df = service_builder_list(hospitals, city_node_tag, city_node)
    return restaurants_df, schools_df, hospitals_df

# returns the density of population and 100,000 persons per amenities 
def approx_density(city_node_tag, city_node, city_area, city_population):
    # city_population in number of persons
    # city surface area in km²
    restaurants_df, schools_df, hospitals_df = amenities_df_reduced(city_node_tag, city_node)
    restaurant_density = 100000.*restaurants_df['key'].count() / city_population
    schools_density = 100000. * schools_df['key'].count() / city_population
    hospitals_density = 100000. * hospitals_df['key'].count() / city_population
    population_density = city_population / city_area
    print city_node_tag, "and", city_node, "proceeded"
    return [restaurant_density, schools_density, hospitals_density, population_density]

# Formatting and plotting data
import numpy as np
durban = np.array(approx_density("durban_node_tag", "durban_node", 2292, 3500000))
halifax = np.array(approx_density("halifax_node_tag", "halifax_node", 5490, 417800))
quebec = np.array(approx_density("quebec_node_tag", "quebec_node", 484.1, 806400))
lausanne = np.array(approx_density("lausanne_node_tag", "lausanne_node", 41.37, 146372))
turin = np.array(approx_density("turin_node_tag", "turin_node", 130.2, 892649))
verona = np.array(approx_density("verona_node_tag", "verona_node", 206.6, 259069))

population_np =  np.array(range(5))
restaurants_np = np.array(range(5))
schools_np = np.array(range(5))
hospitals_np = np.array(range(5))
cities_np = (halifax, quebec, lausanne, turin, verona)
for i in range(len(cities_np)):
    restaurants_np[i] = cities_np[i][0]
    schools_np[i] = cities_np[i][1]
    hospitals_np[i] = cities_np[i][2]
    population_np[i] = cities_np[i][3]

restaurants_pd_series = pd.Series(restaurants_np, index = ['halifax', 'quebec', 'lausanne', 'turin', 'verona'])
schools_pd_series = pd.Series(schools_np, index = ['halifax', 'quebec', 'lausanne', 'turin', 'verona'])
hospitals_pd_series = pd.Series(hospitals_np, index = ['halifax', 'quebec', 'lausanne', 'turin', 'verona'])
population_pd_series = pd.Series(population_np, index = ['halifax', 'quebec', 'lausanne', 'turin', 'verona'])

all_cities_df = pd.concat([schools_pd_series, hospitals_pd_series], axis=1)
all_cities_df.columns = ['schools', 'hospitals']


import seaborn as sns

# Plotting the Dataframe for preliminary observations and data-based hypotheses
city_fig_number = city_fig_number + 1
title = 'Population density in cities'
ylabel = 'number per km2'
y_lim = [0, 7000]
fig_size = [4, 3]
pandas_plotter(population_pd_series, city_fig_number, title, ylabel, y_lim, fig_size)



# Plotting the relative number of schools and hospitals per city
city_fig_number = city_fig_number + 1
title = 'Schools and hospitals in cities'
ylabel = 'number per 100,000 persons'
y_lim = [0, 25]
fig_size = [6.5, 3]
pandas_plotter(all_cities_df, city_fig_number, title, ylabel, y_lim, fig_size)



# Plotting the Dataframe of restaurant number per city
city_fig_number = city_fig_number + 1
title = 'Restaurants in cities'
ylabel = 'number per 100,000 persons'
y_lim = [0, 250]
fig_size = [4, 3]
pandas_plotter(restaurants_pd_series, city_fig_number, title, ylabel, y_lim, fig_size)


# closing the database
conn.close()
print "{db} is closed".format(**vars())