import glob
from unittest import case

import pandas as pd
import plotly.express as px
import plotly.io as pio
#from matplotlib.pyplot import legend
import plotly.graph_objects as go
from matplotlib.pyplot import figure

from color_maps import operator_color_map

pio.renderers.default = "browser"

operators = {
    '"Op"[1]': 'OP1 (Tim)',
    '"Op"[2]': 'OP2 (Vodafone)',
    '"Op"[3]': 'OP3 (Illiad)',
    '"Op"[4]': 'OP4 (Wind)',
}
#"RSRQ", "RSRP",
metrics_4G = ["SINR"]
metrics_5G = ["SSS-RSRQ", "SSS_RSRP", "SSS-SINR"]

def plot_graphs(signal, csv):
    metrics = None
    match signal:
        case "4G": metrics = metrics_4G
        case "5G": metrics = metrics_5G
    name= f"location: {i} , using {signal}"
    for metric in metrics:
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


        vp = px.violin(csv, title=name + f", metric: {metric}", box=True, x=csv['MNC'], y=metric, color="MNC",
                       color_discrete_map=operator_color_map)

        for x, op in enumerate(csv['MNC'].unique()):
            print(op)
            median = csv.groupby('MNC')[metric].median()
            minimum = csv.groupby('MNC')[metric].min()
            vp.add_annotation(x=x + .33, y=median[op], showarrow=False, text=f'median: {median[op]:.2f}',
                              font=dict(size=14))
        vp.show()

for i in range(4,5):
    try:
        csv_files_path = f"./4G_2023_passive/location_{i}_od_capacity_*.csv"
        all_csv_files = glob.glob(csv_files_path)

        csv4G = pd.concat([pd.read_csv(file) for file in all_csv_files], ignore_index=True)
        csv4G.sort_values(by=['MNC'], inplace=True)
        csv4G.replace({'MNC': operators}, inplace=True)
        print(csv4G['MNC'].unique())

        csv_files_path = f"./5G_2023_passive/location_{i}_od_capacity_*.csv"
        all_csv_files = glob.glob(csv_files_path)

        csv5G = pd.concat([pd.read_csv(file) for file in all_csv_files], ignore_index=True)
        csv5G.sort_values(by=['MNC'], inplace=True)
        csv5G.replace({'MNC': operators}, inplace=True)

        plot_graphs(signal="4G", csv=csv4G)
        # plot_graphs(signal="5G", csv=csv5G)


    except Exception as e:
        print(f"{i} failed")
        print(e)
        continue