"""
Tool Name: Preprocessing Corona 
Source Name: preprocessingCorona.py
Version: Python 3.7
Author: Michael Robbins, Web Mapping 2020

Taking raw corona data that is updated daily and returning the most up to date
date for states NY,NJ,RI,MA,VT,NH,CT,ME,VA,WV,MD,PA,DE,DC
"""

# Libraries
import os
import pandas as pd

# Change the baseDir variable to the location where you saved the clone.
baseDir = r'C:\coronaMapFinal'

# Locations of other data directories
origDir = os.path.join(baseDir, 'origData')
prepDir = os.path.join(baseDir, 'prepData')

os.chdir(origDir)

# Reading in US covid data by county
maindf = pd.read_csv('us-counties.csv')
df = maindf

# Selecting only New York counties
df = df[(df.state == 'New York') | 
        (df.state == 'New Jersey') | 
        (df.state == 'Rhode Island') |
        (df.state == 'Massachusetts') |
        (df.state == 'Vermont') |
        (df.state == 'New Hampshire') |
        (df.state == 'Connecticut') |
        (df.state == 'Maine') |
        (df.state == 'Virginia') |
        (df.state == 'Maryland') |
        (df.state == 'West Virginia') |
        (df.state == 'Pennsylvania') |
        (df.state == 'Delaware') |
        (df.state == 'District of Columbia')
        ]

# Since New York is technically 5 counties, and this data aggregates them to 
# one, we are assigning the New York City County as 36061 since it's NaN 
# in the data
df.fips[df.county == 'New York City'] = 36061

## Summing all cases and deaths by county. Retaining FIPS code
#df = df.groupby(['county','state', 'fips'], as_index=False).agg({'cases':'sum', 
#               'deaths':'sum'})

# Ensuring that each county selected has the most recent data
df = df[df.groupby('fips')['date'].transform('max') == df['date']]

# Dropping the unknown row
df = df.drop(df.index[df.county == 'Unknown'])

# ALter FIPS field
df = df.astype({'fips': 'str'})
df.fips = df.fips.apply(lambda x: x[:5] if len(x) == 7 else x[:4].zfill(5))

# Exporting Data
#df.to_csv('corona_counties_data.csv')

# Creating dataframe for line graph and totals
linegraph = maindf.groupby('date', as_index=False).agg({'cases':'sum',
                          'deaths':'sum'})

# Adding a month columns


# Exporting Data
#linegraph.to_json('corona_counties_linegraph_data.json')
