import glob
import pandas as pd
import csv
import plotly.express as px


with open('4G_2023_passive/location_4_od_capacity_iw_tti_0.csv', newline='') as csvfile:
    csv = pd.read_csv(csvfile)


fig = px.scatter_map(csv, lat="Latitude", lon="Longitude", hover_name="RSRP", color='RSRP', zoom=15)
fig.update_layout(map_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()

# csv_files_path = "./4G_2023_passive/*.csv"
# all_csv_files = glob.glob(csv_files_path)
#
# for file_path in all_csv_files:
#     print(f"Processing file: {file_path}")
#

