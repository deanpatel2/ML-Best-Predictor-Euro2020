# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 15:16:02 2021

@author: deanp

Program to load Euro 2020 data and plot scatter plots with best fit line on
a single figure. Includes statistical analysis for r and p values of regression.
"""

#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager
import matplotlib as mpl
from scipy import stats as sp
#%%
#Load data
df = pd.read_excel("C:/Users/deanp/OneDrive/Desktop/Football Analytics/Data/Uefa Euro Data/Euro 2020 Match and Goal Data.xlsx",
                   sheet_name=3)

#%%

# Slice df, setup into home and away columns
home_gd = df["Home GD"]
away_gd = df["Away GD"]
match_GD = home_gd.append(away_gd)

home_columns = df.iloc[:, range(6, 31)]
away_columns = df.iloc[:, range(31, len(df.columns))]


#%%
from pprint import pprint
#Statistical analysis to get r and p values

column_names = list(away_columns.columns)
r_values = {}
p_values = {}
for col in range(0, len(column_names)):
    home_col = home_columns.iloc[:, col]
    away_col = away_columns.iloc[:, col]
    predictor = home_col.append(away_col, ignore_index=True)
    result = sp.linregress(predictor, match_GD)
    r_values[column_names[col]] = result.rvalue
    p_values[column_names[col]] = result.pvalue
    
sorted_r_values = sorted(r_values.items(), key=lambda x:x[1])
for i in range(0, 25):
    stat_name = sorted_r_values[i][0]
    r_value = round(sorted_r_values[i][1], 3)
    p_value = round(p_values.get(stat_name), 3)
    pprint("|" + stat_name + "|" + str(r_value) + "|" + str(p_value) + "|")
#%%
#Plotting the scatter plot matrix

#Setup
text_color = 'white'
mpl.rcParams['font.family'] = "Arial"
fig, ax = plt.subplots(5, 5, figsize=(12, 12))
fig.set_facecolor('#313332')
row = -1
column = 0

#Loop to produce matrix of scatter plots
for col in range(0, len(column_names)):
    if ((col % 5) == 0): # logic to increment row and column correctly
        row += 1
        column = 0
    home_col = home_columns.iloc[:, col]
    away_col = away_columns.iloc[:, col]
    predictor = home_col.append(away_col, ignore_index=True)
    m, b = np.polyfit(predictor, match_GD, 1)
    ax[row, column].scatter(x=predictor, y=match_GD, color='#89CFF0', alpha=0.35)
    bounds = ax[row, column].get_xbound()
    x = np.arange(bounds[0], bounds[1], step=(bounds[1] - bounds[0])/8)
    y = b+m*x
    ax[row, column].plot(x, y, color='red')
    ax[row, column].set_xlabel(column_names[col], fontsize=14, color=text_color)
    if (column == 0):
        ax[row, column].set_ylabel('Match GD', fontsize=14, color=text_color)
    ax[row, column].patch.set_facecolor('#313332')
    ax[row, column].spines["top"].set_visible(False)
    ax[row, column].spines["right"].set_visible(False)
    ax[row, column].spines["bottom"].set_color(text_color)
    ax[row, column].spines["left"].set_color(text_color)
    ax[row, column].tick_params(axis='x', colors=text_color)
    ax[row, column].tick_params(axis='y', colors=text_color)
    column += 1

fig.text(
    x=0.05,
    y=0,
    s="Created by Dean Patel. Data provided by Fotmob.",
    fontsize=9,
    fontstyle="italic",
    color=text_color,
    )
    
fig.tight_layout(pad=3.0)
fig.savefig('C:/Users/deanp/OneDrive/Desktop/Football Analytics/Output/predictor_plots/' +
                'scatterMatrix.png', dpi=300, bbox_inches='tight')
