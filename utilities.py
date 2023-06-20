#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 21:09:13 2023

@author: jimmyfarrelly
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("alt_fuel_stations (Jul 29 2021).csv")


# Fuel Type Distribution Functions
def plot_fuel_type_distribution(df):
    """
    Plots a pie chart and line plot showing the distribution of fuel types, 
    including "ELEC", "E85", "LPG", and others.
    """
    data = df['Fuel Type Code'].value_counts()
    data['Other'] = data.loc[~data.index.isin(['ELEC', 'E85', 'LPG'])].sum()
    data = data.loc[['ELEC', 'E85', 'LPG', 'Other']]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(data.values, labels=data.index, autopct='%1.2f%%')
    ax.set_title('Fuel Type Distribution')
    
    """
    Creates a bar chart of the fuel types and the corresponding number of 
    stations and incorporates numpy
    """
    fuel_type_counts = np.array(data.values)
    fuel_types = np.array(data.index)
    total_count = fuel_type_counts.sum()  # Calculate the total count
    
    fig, ax2 = plt.subplots(figsize=(6, 6))
    ax2.bar(fuel_types, fuel_type_counts)
    ax2.set_xlabel('Fuel Type')
    ax2.set_ylabel('Number of Stations')
    ax2.set_title('Distribution of Fuel Types')
    
    # Add total count as a separate bar in orange
    ax2.bar('Total', total_count, color='orange')
    
    plt.xticks(rotation=90)
    plt.show()



def stations_by_fuel_type_and_state(df):
    """
    Creates a stacked bar chart showing states and the number of stations
    per fuel type
    """
    grouped_data = df.groupby(['State', 'Fuel Type Code'])['Station Name'].count().reset_index(name='Number of Stations')
    
    pivoted_data = grouped_data.pivot_table(index='State', columns='Fuel Type Code', values='Number of Stations', fill_value=0)
    
   
    ax = pivoted_data.plot.bar(stacked=True, figsize=(15, 6))
    ax.set_title('Number of Stations by Fuel Type and State')
    ax.set_xlabel('State')
    ax.set_ylabel('Number of Stations')
    plt.xticks(rotation=90)
    plt.legend(title='Fuel Type')
    plt.show()
    


# Access Type Distribution Functions
def plot_access_type_distribution(df):
    """
    Creates a pie chart showing the distribution of access types.
    Essentially, it shows the percentage of alternative fueling stations that
    are public and private.
    """
    data = df['Access Code'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(data.values, labels=data.index, autopct='%1.1f%%')
    ax.set_title('Access Type Distribution')
    plt.show()

def stations_n_states(df, n=64):
    """
    Returns states and territories and each number alternative fuel locations 
    """
    state_counts = df.groupby('State')['Station Name'].count().reset_index(name='Number of Stations')
    stations_n = state_counts.sort_values('Number of Stations', ascending=False).head(n)

    return stations_n


def plot_stations_n_states(df, n=64):
    """
    Creates a bar chart showing states and territories with their number of 
    alternative fuel locations.
    """
    stations_n = stations_n_states(df, n)
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.bar(stations_n['State'], stations_n['Number of Stations'])
    ax.set_title('States (and Territories) and Number of Alt Fuel Locations')
    ax.set_xlabel('State')
    ax.set_ylabel('Number of Stations')
    plt.xticks(rotation=90)
    plt.show()
    
    
def plot_upcoming_stations(df):
    """
    Plots a bar chart of the number of expected alternative fuel stations for each state, ordered from largest to smallest.
    """
    df['Expected Date'] = pd.to_datetime(df['Expected Date'], errors='coerce')
    upcoming_df = df[df['Expected Date'].notnull()].sort_values('Expected Date', ascending=True)

    if len(upcoming_df) == 0:
        print("No upcoming alternative fuel stations were found.")
    else:
        state_counts = upcoming_df.groupby('State')['Station Name'].count().reset_index(name='Number of Expected Stations')
        state_counts = state_counts.sort_values('Number of Expected Stations', ascending=False)  # Sort by number of expected stations
        fig, ax = plt.subplots(figsize=(15, 6))
        ax.bar(state_counts['State'], state_counts['Number of Expected Stations'])
        ax.set_title('Number of Expected Alt Fuel Stations by State (and Territories)')
        ax.set_xlabel('State')
        ax.set_ylabel('Number of Expected Stations')
        plt.xticks(rotation=90)
        plt.show()

    

# Stations Over Time Functions
def stations_opened_per_year(df):
    """
    Plots a line chart showing the number of alternative fueling stations 
    opened over time, displaying the years and number of stations.
    """
    df['Open Date'] = pd.to_datetime(df['Open Date'], errors='coerce')
    df['Year'] = df['Open Date'].dt.year
    year_counts = df['Year'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(year_counts.index, year_counts.values)
    ax.set_title('Number of Stations Opened Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Stations')
    plt.show()
    


# Location Specific Functions
def plot_public_ev_stations(df):
    """
    Plots a scatter chart of where there are public electric stations in the US
    """
    public_ev_df = df[(df['Fuel Type Code'] == 'ELEC') & (df['Access Code'] == 'public')]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(public_ev_df['Longitude'], public_ev_df['Latitude'], s = .5)
    ax.set_title('Public EV Charging Stations by Location')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    plt.show()



# Top Cities and States Functions
def plot_top_cities(df, n):
    """
    Plots a bar chart of the top n cities with the most alternative fueling 
    stations, displaying the city names and number of stations.
    """

    data = df.groupby('City')['Station Name'].count().reset_index(name='Number of Stations')
    data = data.sort_values('Number of Stations', ascending=False).head(n)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(data['City'], data['Number of Stations'])
    ax.set_title(f'Top {n} Cities with the Most Alt Fuel Stations')
    ax.set_xlabel('City')
    ax.set_ylabel('Number of Stations')
    plt.xticks(rotation=90)
    plt.show()


def plot_ev_charging_stations_in_iowa(df):
    """
    Plots a bar chart of the top 10 cities in Iowa with the most EV charging 
    stations, and shows the city names and number of stations.
    """
    df = df[(df["State"] == "IA") & (df["Fuel Type Code"] == "ELEC")]
    data = df.groupby('City')['Station Name'].count().reset_index(name='Number of Stations')
    data = data.sort_values('Number of Stations', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(data['City'], data['Number of Stations'])
    ax.set_title('Top 10 Cities in Iowa with the Most EV Charging Stations')
    ax.set_xlabel('City')
    ax.set_ylabel('Number of Stations')
    plt.xticks(rotation=90)
    plt.show()





def find_stations_in_city(df):
    """
    Asks a user for a city and state, and returns the number of stations of 
    each fuel type in the location. If their location does not have any stations,
    or the user incorrectly types the state or city, then a message will appear
    that no stations were found.
    """

    try:
        state = input("Enter the state abbreviation (ex: IL): ")
        city = input("Enter the city name: ")
        
        if len(state) != 2 or not state.isalpha():
            raise ValueError("Invalid state abbreviation")
        
        df_city = df[(df['State'] == state.upper()) & (df['City'] == city.title())]

        if len(df_city) == 0:
            print(f"No alternative fuel stations were found in {city.title()}, {state.upper()}.")
        else:
            fuel_type_counts = df_city['Fuel Type Code'].value_counts()
            print(f"Alternative fuel stations in {city.title()}, {state.upper()}:")
            for fuel_type, count in fuel_type_counts.items():
                print(f"{fuel_type}: {count} stations")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

