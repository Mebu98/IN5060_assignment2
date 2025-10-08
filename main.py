import glob
import pandas as pd
import plotly.express as px
import plotly.io as pio
from matplotlib.pyplot import legend
import plotly.graph_objects as go

from color_maps import operator_color_map

pio.renderers.default = "browser"

metrics = ["RSRQ", "RSRP", "SINR"]

for i in range(4,5):
    try:
        csv_files_path = f"./4G_2023_passive/location_{i}_od_capacity_*.csv"
        all_csv_files = glob.glob(csv_files_path)

        csv = pd.concat([pd.read_csv(file) for file in all_csv_files], ignore_index=True)
        csv.sort_values(by=['MNC'], inplace=True)

        # operators = csv['MNC'].unique()
        # operator_csvs = [csv[csv['MNC'] == op] for op in operators]
        #
        # for op_csv in operator_csvs:
        #     print(op_csv.size)
        #
        #     fig = px.scatter_map(op_csv, title=f'location {i} {op_csv['MNC'].unique()[0]}', labels='MNC', lat="Latitude", lon="Longitude", hover_name=metric, color=metric, zoom=15)
        #     fig.update_layout(map_style="open-street-map")
        #     fig.update_layout(margin={"r": 50, "t": 50, "l": 50, "b": 50})
        #     fig.show()

        for metric in metrics:
            vp = px.violin(csv, title=i, box=True, x=csv['MNC'], y=metric, color="MNC",
                           color_discrete_map=operator_color_map)
            vp.show()


    except Exception as e:
        print(f"{i} failed")
        print(e)
        continue