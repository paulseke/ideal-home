# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 17:43:46 2016

@author: seke
"""
### Some useful functions
import matplotlib as mpl
from collections import Counter
import numpy as np
import pandas as pd
import math

    
# Choosing amenities of interest
needed_values = ('restaurant', 'Restaurant','hospital', 'school', 'clinic', 'doctors', 
                 'kindergarten', 'fire_station', 'police', 'parking')

# Grouping amenities of interest
restaurants = ('restaurant', 'Restaurant') 
# In Durban, one case of Restaurant instead of restaurant
kids_schools = ('school', 'kindergarten','School', 'Kindergarten')
hospitals = ('hospital', 'clinic', 'doctors','Hospital', 'Clinic', 'Doctors')
police_fire_fighters = ('fire_station', 'police')



# Displays a given amenity present in the node table
def amenities_of_interest_viewer(city_node_tag, needed_values):
    cursor.execute('''SELECT  Key, Value, count(*)
    FROM {city_node_tag} WHERE Key = 'amenity' 
    AND Value in {needed_values}
    Group BY Value ORDER BY Key;'''.format(**vars()))
    #result = cursor.fetchall()
    result = pd.DataFrame(cursor.fetchall(), 
                          columns = ('key', 'value', 'count'))
    print "amenities of interest in", city_node_tag
    return result

# exports amenities in group of interest
def service_builder_list(amenity_list, city_node_tag, city_node):
    cursor.execute('''SELECT Value, Latitude, Longitude 
    FROM {city_node_tag}  
    JOIN {city_node} ON {city_node}.NodeId = {city_node_tag}.NodeId
    WHERE Key = 'amenity' AND Value in {amenity_list} 
    Group BY Latitude  ORDER BY Longitude;'''.format(**vars()))
    return pd.DataFrame(cursor.fetchall(), 
                        columns = ('key', 'latitude', 'longitude'))

# exports a given amenity                       
def service_builder_amenity(amenity, city_node_tag, city_node):
    cursor.execute('''SELECT Value, Latitude, 
    Longitude FROM {city_node_tag}  
    JOIN {city_node} ON {city_node}.NodeId = {city_node_tag}.NodeId
    WHERE Key = 'amenity' AND Value = {amenity} 
    Group BY Latitude  ORDER BY Longitude;'''.format(**vars()))
    return pd.DataFrame(cursor.fetchall(), 
                        columns = ('key', 'latitude', 'longitude'))

# collects amenities of interest in DataFrames
def amenities_df(city_node_tag, city_node):
    # collecting restaurants
    restaurants_df = service_builder_list(
        restaurants, city_node_tag, city_node)
    # collecting kids' schools
    schools_df = service_builder_list(
        kids_schools, city_node_tag, city_node)
    # collecting hospitals
    hospitals_df = service_builder_list(
        hospitals, city_node_tag, city_node)
    # collecting kids' police_fire_fighters
    police_firefighters_df = service_builder_list(
        police_fire_fighters, city_node_tag, city_node)
    # collecting parkings
    parkings_df = service_builder_amenity(
        "'parking'", city_node_tag, city_node)
    print city_node_tag, "and", city_node, "proceeded"
    return restaurants_df, schools_df, hospitals_df, police_firefighters_df, parkings_df


# plots amenities of interest
def plotter(city, city_fig_number, legend_position, x_lim, y_lim):
    # getting df of amenities of interest
    restaurants_df, schools_df, hospitals_df, police_df, parkings_df = amenities_df(
        city_node_tag, city_node
    )
    #%matplotlib inline
    #mpl.style.use('ggplot')
    #mpl.rcParams['savefig.dpi'] = 120
    #%pylab inline
    ax = restaurants_df.plot(
        kind='scatter', y ='latitude', x='longitude', 
        color='DarkOrange', label='restaurants', 
        s=80, fontsize=15, figsize=(15, 8));
    schools_df.plot(kind='scatter', y='latitude', 
                    x='longitude', color='green', 
                    label='schools', s=120, ax=ax);
    hospitals_df.plot(kind='scatter', y='latitude', 
                      x='longitude', color= 'red', 
                      label='hospitals', s=100, ax=ax);
    police_df.plot(kind='scatter', y='latitude', 
                                x='longitude', color= 'blue', 
                                label='police or fire fighters', 
                                s=70, ax=ax);
    parkings_df.plot(kind='scatter', y='latitude', 
                     x='longitude', color='black', 
                     label='parkings', s=60, ax=ax);
    ax.grid(True);
    ax.set_xlim(x_lim)
    ax.set_ylim(y_lim)
    ax.set_title('Services in {city}'.format(**vars()), 
                 fontsize=22)
    ax.set_ylabel('Latitude', fontsize=20)
    ax.set_xlabel('Longitude', fontsize=20)
    ax.legend(loc = '{legend_position}'.format(**vars()), 
              labelspacing=0.5, fontsize = 12)
    #plt.show();
    print ""
    print "FIGURE {city_fig_number}".format(**vars())


# Returns the number of elements present in a table
def element_number(element_type, city_node_or_way, Id_node_or_way):
    cursor.execute('''SELECT {Id_node_or_way}, count(*)
    FROM {city_node_or_way};'''.format(**vars()))
    result = cursor.fetchall()
    print "The number of {element_type} in".format(**vars()), city_node_or_way,"is:", result[0][1]

# number of unique users
def unique_user_number(city, city_node, city_way):
    # users in node table
    cursor.execute('''SELECT NodeId, UserId, count(*)
    FROM {city_node} GROUP BY UserId;'''.format(**vars()))
    result_node = pd.DataFrame(cursor.fetchall(), columns = ['Id','User_Id', 'count'])
    # users in way table
    cursor.execute('''SELECT WayId, UserId, count(*)
    FROM {city_way} GROUP BY UserId;'''.format(**vars()))
    result_way = pd.DataFrame(cursor.fetchall(), columns = ['Id','User_Id', 'count'])
    # counting unique users"
    users = result_node.append(result_way)
    users = users['User_Id']
    users = len(Counter(users).keys())
    print "The number of unique users in {city} tables is:".format(**vars()), users


def osm_csv_size(city):
    if city == 'Fredericton':
        a = [32.5, 11.9, 0.254, 1.2, 4.3, 2.5] 
    elif city == 'Saint Louis':
        a = [32.9, 12.5, 0.139, 1.5, 4.5, 1.6] 
    elif city == 'Nairobi':
        a = [75.6, 29.0, 2.7, 3.0, 9.7, 2.3]
    elif city == 'Lausanne':
        a = [114.1, 40.3, 2.9, 4.9, 13.9, 9.1]
    elif city == 'Turin':
        a = [130, 47.1, 3.7, 5.4, 17.2, 6.5]
    elif city == 'Durban':
        a = [73.2, 28.5, 1.4, 2.0, 9.2, 3.6]
    elif city == 'Halifax':
        a = [83.1, 32.3, 3.7, 2.1, 10.3, 3.0]
    elif city == 'Quebec City':
        a = [115.3, 39.5, 11.2, 4.7, 12.9, 6.3]
    elif city == 'Verona':
        a = [184.6, 66.1, 7.8, 5.2, 17.2, 6.4]
        
    print city,"files' size in MB:" 
    print "city.osm:",a[0], "   nodes.csv:",a[1], "   node_tag.csv:",a[2] 
    print "ways.csv:",a[3], "   way_nodes.csv",a[4], "   way_tags.csv",a[5]

    
# returns city surface area in km² and population (in persons)
def city_area_and_population(city):
    if city == 'Fredericton':
        return math.floor(130.7), 56224
    elif city == 'Saint Louis':
        return 46, 176000
    elif city == 'Nairobi':
        return 696, 47200000
    elif city == 'Lausanne':
        return math.floor(41.37), 146372
    elif city == 'Turin':
        return math.floor(130.2), 892649
    elif city == 'Durban':
        return 2292, 3500000
    elif city == 'Halifax':
        return 5490, 417800
    elif city == 'Quebec City':
        return math.floor(484.1), 806400
    elif city == 'Verona':
        return math.floor(206.6), 259069 

# Displays a given amenity present in the node table
def land_number(city_way_tag, city_way, needed_places):
    cursor.execute('''SELECT  Value, count(*) as num
    FROM {city_way_tag} WHERE Value in {needed_places}
    Group BY Value
    ORDER BY num;'''.format(**vars()))
    #result = cursor.fetchall()
    # one element is missing in Lausanne, causing the error
    # ValueError: Wrong number of items passed 4, placement implies 5
    # solution: ensuring that the arrays has 5 elements
    result = pd.DataFrame(cursor.fetchall(), columns = ('land', 'count'))
    result_out = range(len(needed_places))
    for i in range(len(needed_places)):
        if land_try(result, needed_places[i]):
            a = result[result['land'] == needed_places[i]]
            result_out[i] = a['count'][a.index[0]]
        else:
            result_out[i] = 0
    return result_out

# returns the relative counts of way elements
def lands_pd_maker(city, city_way_tag, city_way, needed_places):
    # getting lands number
    lands_np = land_number(city_way_tag, city_way, needed_places)
    # creating an array with same len as lands_np
    lands_val = np.array(range(len(needed_places)))
    # getting city area
    area_city, population_city = city_area_and_population(city)
    # number of lands per km²
    for i in range(len(needed_places)):
        lands_val[i] = lands_np[i] * 100 / area_city
    # returning the lands pd series 
    return pd.Series(lands_val, index = needed_places)

# returns False if a needed element is missing 
def land_try(result, tested_str):
    a = result[result['land'] == tested_str]
    try:
        a['count'][a.index[0]]
        return True
    except IndexError:
        return False

def pandas_plotter(pd_series, city_fig_number, title, ylabel, y_lim, fig_size):
    ax =(pd_series).plot.bar(fontsize=10,figsize=fig_size)
    ax.set_title('{title}'.format(**vars()), fontsize=13)
    ax.set_ylabel('{ylabel}'.format(**vars()), fontsize=12)
    ax.set_ylim(y_lim)
    print ""
    print "FIGURE {city_fig_number}".format(**vars())



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
    #print city_node_tag, "and", city_node, "proceeded"
    return [restaurant_density, schools_density, hospitals_density, population_density]

def print_city_file_stats(city):
    city_node_tag, city_node, city_way_tag, city_way = city_files_id(city)
    # osm file information
    osm_csv_size(city)
    print ""
    #node_number 
    element_number('nodes', city_node, 'NodeId')
    print ""
    element_number('ways', city_way, 'WayId')
    print ""
    unique_user_number(city, city_node, city_way)

        
# returns city fileID
def city_files_id(city):
    if city == 'Fredericton':
        return "fredericton_node_tag", "fredericton_node", "fredericton_way_tag", "fredericton_way"
    elif city == 'Saint Louis':
        return "st_louis_node_tag", "st_louis_node", "st_louis_way_tag", "st_louis_way"
    elif city == 'Nairobi':
        return "nairobi_node_tag", "nairobi_node", "nairobi_way_tag", "nairobi_way"
    elif city == 'Lausanne':
        return "lausanne_node_tag", "lausanne_node", "lausanne_way_tag", "lausanne_way"
    elif city == 'Turin':
        return "turin_node_tag", "turin_node", "turin_way_tag", "turin_way"
    elif city == 'Durban':
        return "durban_node_tag", "durban_node", "durban_way_tag", "durban_way"
    elif city == 'Halifax':
        return "halifax_node_tag", "halifax_node", "halifax_way_tag", "halifax_way"
    elif city == 'Quebec City':
        return "quebec_node_tag", "quebec_node", "quebec_way_tag", "quebec_way"
    elif city == 'Verona':
        return  "verona_node_tag", "verona_node", "verona_way_tag", "verona_way"

# returns some city file stats and file id
def city_files_information(city):
    print_city_file_stats(city)
    return city_files_id(city)

