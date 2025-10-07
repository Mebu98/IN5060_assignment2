import glob
import pandas as pd
import plotly.express as px
import plotly.io as pio
from pygments.lexers import go

from color_maps import operator_color_map

pio.renderers.default = "browser"

for i in range(1,2):
    try:
        csv_files_path = f"./4G_2023_passive/location_{i}_*.csv"
        all_csv_files = glob.glob(csv_files_path)

        csv = pd.concat([pd.read_csv(file) for file in all_csv_files], ignore_index=True)
        print(csv)
        csv.sort_values(by=['MNC'], inplace=True)

        fig = px.scatter_map(csv, title=i, lat="Latitude", lon="Longitude", hover_name="RSRP", color='RSRP', zoom=15)
        fig.update_layout(map_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.show()

        operators = csv['MNC'].unique()
        operator_csvs = [csv[csv['MNC'] == op] for op in operators]

        vp = px.violin(csv, title=i, box=True, x=csv['MNC'], y='RSRP', color="MNC", color_discrete_map=operator_color_map)
        vp.show()
    except Exception:
        print(f"{i} failed")
        continue