import glob
import pandas as pd
import csv
import plotly.express as px
import plotly.io as pio
from plotly.graph_objs import Figure
from pygments.lexers import go

from color_maps import operator_color_map

pio.renderers.default = "browser"



with open('4G_2023_passive/location_4_od_capacity_iw_tti_0.csv', newline='') as csvfile:
    csv = pd.read_csv(csvfile)

csv.sort_values(by=['MNC'], inplace=True)

# fig = px.scatter_map(csv, lat="Latitude", lon="Longitude", size='Speed', hover_name="RSRP", color='RSRP', zoom=15)
# fig.update_layout(map_style="open-street-map")
# fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
# fig.show()

operators = csv['MNC'].unique()
operator_csvs = [csv[csv['MNC'] == op] for op in operators]

# for operator_csv in operator_csvs:
bp = px.box(csv, x=csv['MNC'], y='RSRP', color="MNC", color_discrete_map=operator_color_map)
bp.show()



# csv_files_path = "./4G_2023_passive/*.csv"
# all_csv_files = glob.glob(csv_files_path)
#
# for file_path in all_csv_files:
#     print(f"Processing file: {file_path}")
#

# Create a boxplot grouped by ID and Category (extra column)
# fig = px.box(df, x="ID", y="Value", color="Category", points="all")
#
# fig.update_layout(title="Boxplot of Value by ID and Category")
# fig.show()