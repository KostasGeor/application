import pandas as pd
import numpy as np
import re
data = pd.read_csv('autopilot_logs/uav-1-testm.csv',encoding = 'unicode_escape')



mission_id = []
flight_id = []
flight_path_id = []
for index,row in data.iterrows():
  mission_id.append(1)
  flight_id.append(1)
  flight_path_id.append(1)


data['Mission ID'] = mission_id

df1 = data[['GPS Position East (degrees)','GPS Position North (degrees)','GPS Altitude (meters)','Mission ID']]
df1['GPS Position East (degrees)'] = df1['GPS Position East (degrees)'].str.replace('W','')
df1['GPS Position North (degrees)'] = df1['GPS Position North (degrees)'].str.replace('N','')

df1['GPS Position East (degrees)'] = df1['GPS Position East (degrees)'].astype(float)
df1['GPS Position North (degrees)'] = df1['GPS Position North (degrees)'].astype(float)

df1.to_csv('data2.csv')





#
# df1 = data[['Flight Path ID','Mission ID','Current Speed (meters / s)', 'AGL (meters)','Current Roll (degrees)','Current Yaw (degrees)','GPS Speed (meters / s)','Pressure Altitude (meters)','Current Pitch (degrees)','Airborn','Time (s)',]]
#





