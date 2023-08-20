import time

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from streamlit_folium import folium_static

st.set_page_config(layout="wide")

import pandas as pd
import folium

# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import pandas as pd
import folium
file = (r'C:\Users\Daniil\Downloads\Telegram Desktop\case1.xlsx')
df1 = pd.read_excel(file,skiprows = 1, header = 0)
df1['Latitude'] = 55.539306
df1['Longitude'] = 51.856451
df1['point'] = 'A'
df1 = df1[df1.index > 1]
file = (r'C:\Users\Daniil\Downloads\Telegram Desktop\case2.xlsx')
df2 = pd.read_excel(file,skiprows = 1, header = 0)
df2['Latitude'] = 55.654578
df2['Longitude'] = 51.800072
df2['point'] = 'B'
df2 = df2[df2.index > 1]
file = (r'C:\Users\Daniil\Downloads\Telegram Desktop\case3.xlsx')
df3 = pd.read_excel(file,skiprows = 1, header = 0)
df3['Latitude'] = 55.613193
df3['Longitude'] = 51.784821
df3['point'] = 'C'
df3 = df3[df3.index > 1]
file = (r'C:\Users\Daniil\Downloads\Telegram Desktop\case4.xlsx')
df4 = pd.read_excel(file,skiprows = 1, header = 0)
df4['Latitude'] = 55.598983
df4['Longitude'] = 51.771936
df4['point'] = 'D'
df4 = df4[df4.index > 1]
file = (r'C:\Users\Daniil\Downloads\Telegram Desktop\case5.xlsx')
df5 = pd.read_excel(file,skiprows = 1, header = 0)
df5['Latitude'] = 55.650091
df5['Longitude'] = 51.852687
df5['point'] = 'E'
df5 = df5[df5.index > 1]
file = (r'C:\Users\Daniil\Downloads\Telegram Desktop\case6.xlsx')
df6 = pd.read_excel(file,skiprows = 1, header = 0)
df6['Latitude'] = 55.622944
df6['Longitude'] = 51.82557
df6['point'] = 'F'
df6 = df6[df6.index > 1]
result = pd.concat([df1, df2,df3, df4,df5, df6], ignore_index=True)
result.head()

#result.to_excel(r'my_data2.xlsx', encoding_override='latin1', index= False)

# +
initial_latitude = 55.539306
initial_longitude = 51.856451

date_string = "13.06.2023 00:00"
date_format = "%d.%m.%Y %H:%M"

# Создание карты

result['D ветра, °'] = result['D ветра, °'].str.replace(r'\D', '', regex=True)
result['D ветра, °']= pd.to_numeric(result['D ветра, °'], errors='coerce')
# result['V ветра, м/с']= pd.to_numeric(result['V ветра, м/с'], errors='coerce')
result['Latitude'] = pd.to_numeric(result['Latitude'], errors='coerce')
result['Longitude'] = pd.to_numeric(result['Longitude'], errors='coerce')
result['V ветра, м/с'] = result['V ветра, м/с'].str.extract(r'\((.*?)\)')[0].fillna(result['V ветра, м/с'].str.extract(r'\((.*?)\)|([^()]+)')[1])
result['V ветра, м/с'] = result['V ветра, м/с'].str.replace(',', '.')
result['V ветра, м/с'] = pd.to_numeric(result['V ветра, м/с'], errors='coerce')
result['CO, мг/м³'] = result['CO, мг/м³'].str.replace(',', '.')
result['CO, мг/м³'] = pd.to_numeric(result['CO, мг/м³'], errors='coerce')
result['NO, мг/м³'] = result['NO, мг/м³'].str.replace(',', '.')
result['NO, мг/м³'] = pd.to_numeric(result['NO, мг/м³'], errors='coerce')
result['NO2, мг/м³'] = result['NO2, мг/м³'].str.replace(',', '.')
result['NO2, мг/м³'] = pd.to_numeric(result['NO2, мг/м³'], errors='coerce')
result['NH3, мг/м³'] = result['NH3, мг/м³'].str.replace(',', '.')
result['NH3, мг/м³'] = pd.to_numeric(result['NH3, мг/м³'], errors='coerce')
result['SO2, мг/м³'] = result['SO2, мг/м³'].str.replace(',', '.')
result['SO2, мг/м³'] = pd.to_numeric(result['SO2, мг/м³'], errors='coerce')
result['H2S, мг/м³'] = result['H2S, мг/м³'].str.replace(',', '.')
result['H2S, мг/м³'] = pd.to_numeric(result['H2S, мг/м³'], errors='coerce')
given_period = result[result['Unnamed: 0'] == '01.06.2023 02:00']
given_period = given_period.fillna(0)
given_period
import folium
import math
from folium.vector_layers import PolyLine
from folium.plugins import TimeSliderChoropleth
initial_coords = (55.539306, 51.856451)
color2 = 'blue'
m = folium.Map(location=initial_coords, zoom_start=11)

for index, row in given_period.iterrows():
    for i in range(3):
        for j in range(3):
            if row['D ветра, °'] > 0:
                start_point = (row['Latitude'] + i/100 - j/100, row['Longitude'] - i/100 - j/100)
                angle_degrees = row['D ветра, °']
#                 angle_degrees = 45
                angle_degrees1 = angle_degrees + 30 + 180
                angle_degrees2 = angle_degrees + 180 - 30
                angle_radians = math.radians(angle_degrees)
                angle_radians1 = math.radians(angle_degrees1)
                angle_radians2 = math.radians(angle_degrees2)
                vector_length = max(0.003,row['V ветра, м/с'] * 0.008)
                end_lat = start_point[0] + vector_length * math.cos(angle_radians)
                end_lon = start_point[1] + vector_length * math.sin(angle_radians)
                end_point = (end_lat, end_lon)
                end_1at_1 = end_point[0] + vector_length * 0.5 * math.cos(angle_radians1)
                end_1on_1 = end_point[1] + vector_length * 0.5 * math.sin(angle_radians1)
                end_1at_2 = end_point[0] + vector_length * 0.5 * math.cos(angle_radians2)
                end_1on_2 = end_point[1] + vector_length * 0.5 * math.sin(angle_radians2)
                end_1 = (end_1at_1,end_1on_1)
                end_2 = (end_1at_2,end_1on_2)
                if row['V ветра, м/с'] <= 1.2:
                    color1 = 'blue'
                elif row['V ветра, м/с'] <= 1.9:
                    color1 = 'orange'
                elif row['V ветра, м/с'] <= 3.0:
                    color1 = 'red'
                elif row['V ветра, м/с'] <= 3.5:
                    color = 'dark red'
                else:
                    color1 = 'black'
                vector_line = PolyLine(locations=[start_point, end_point], color=color1, weight=2)
                vector_line1 = PolyLine(locations=[end_point, end_1], color=color1, weight=2)
                vector_line2 = PolyLine(locations=[end_point, end_2], color=color1, weight=2)
                if row['CO, мг/м³'] >= result['CO, мг/м³'].quantile(0.9):
                    color1 = 'red'
                    tag = 'CO'
                elif row['NO, мг/м³'] >= result['NO, мг/м³'].quantile(0.9):
                    color2 = 'red'
                    tag = 'NO'
                elif row['NO2, мг/м³'] >= result['NO2, мг/м³'].quantile(0.9):
                    color2 = 'red'
                    tag = 'NO2'
                elif row['NH3, мг/м³'] >= result['NH3, мг/м³'].quantile(0.9):
                    color1 = 'red'
                    tag = 'NH3'
                elif row['SO2, мг/м³'] >= result['SO2, мг/м³'].quantile(0.9):
                    color2 = 'red'
                    tag = 'SO2'
                elif row['H2S, мг/м³'] >= result['H2S, мг/м³'].quantile(0.9):
                    color2 = 'red'
                    tag = 'H2S'
                if color2 == 'red':
                    circle_center = (row['Latitude'], row['Longitude'])
                    radius_meters = 500  # Радиус 1 км
                    circle = folium.Circle(
                        location=circle_center,
                        radius=radius_meters,
                        color=color2,  # Цвет обводки круга
                        fill=True,     # Заполнить круг цветом
                        fill_color=color2,  # Цвет заполнения круга
                        fill_opacity=0.4    # Прозрачность заполнения
                    )
                    circle.add_to(m)
                vector_line.add_to(m)
                vector_line1.add_to(m)
                vector_line2.add_to(m)

folium_static(m)