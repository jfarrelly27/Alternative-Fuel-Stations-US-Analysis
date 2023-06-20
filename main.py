#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 22:49:19 2023

@author: jimmyfarrelly
"""

import pandas as pd
import utilities as p

def main():
    df = pd.read_csv("alt_fuel_stations (Jul 29 2021).csv")
    
    p.plot_fuel_type_distribution(df)
    
    p.stations_by_fuel_type_and_state(df)
    
    p.plot_access_type_distribution(df)
    
    p.stations_n_states(df, n=64)
    
    p.plot_stations_n_states(df, n=64)
    
    p.plot_upcoming_stations(df)
    
    p.stations_opened_per_year(df)
    
    p.plot_public_ev_stations(df)
    
    p.plot_top_cities(df, 10)
    
    p.plot_ev_charging_stations_in_iowa(df)
    
    p.find_stations_in_city(df)
    
    
    
    
if __name__ == "__main__":
    main()