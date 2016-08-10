# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 13:02:34 2016

@author: seke
"""


# Creating a df of cities' summary for plotting
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