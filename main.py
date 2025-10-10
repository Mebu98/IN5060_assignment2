import glob
from unittest import case

import pandas as pd
import plotly.express as px
import plotly.io as pio
#from matplotlib.pyplot import legend
import plotly.graph_objects as go
from matplotlib.pyplot import figure

from color_maps import operator_color_map
from color_maps import metric_range_map

pio.renderers.default = "browser"

operators = {
    '"Op"[1]': 'OP1 (Tim)',
    '"Op"[2]': 'OP2 (Vodafone)',
    '"Op"[3]': 'OP3 (Illiad)',
    '"Op"[4]': 'OP4 (Wind)',
}
#"RSRQ", "RSRP",
metrics_4G = ['RSRQ','RSRP',"SINR"]
metrics_5G = ["SSS-RSRQ", "SSS_RSRP", "SSS-SINR"]
metric_map = {
        "RSRQ": ("RSRQ", "SSS-RSRQ"),
        "RSRP": ("RSRP", "SSS_RSRP"),
        "SINR": ("SINR", "SSS-SINR")
    }

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
                       color_discrete_map=operator_color_map, range_y=metric_range_map[metric])

        for x, op in enumerate(csv['MNC'].unique()):
            print(op)
            median = csv.groupby('MNC')[metric].median()
            minimum = csv.groupby('MNC')[metric].min()
            vp.add_annotation(x=x + .33, y=median[op], showarrow=False, text=f'median: {median[op]:.2f}',
                              font=dict(size=14))
        vp.show()


def one_OP_Compare_Location():
    loaction_numb=[]
    all_data=[]
    for i in range(1, 16):
        try:
            csv_files_path = f"./4G_2023_passive/location_{i}_od_*.csv"
            all_csv_files = glob.glob(csv_files_path)
            csv4G = pd.concat([pd.read_csv(file) for file in all_csv_files], ignore_index=True)
            csv4G['Location'] = str(i)
            filtered_csv4G = csv4G[csv4G['MNC'] == '"Op"[3]']

            csv_files_path = f"./5G_2023_passive/location_{i}_od_*.csv"
            all_csv_files = glob.glob(csv_files_path)

            csv5G = pd.concat([pd.read_csv(file) for file in all_csv_files], ignore_index=True)
            csv5G['Location'] = i
            # csv5G.rename(columns={"SSS_RSRP": "RSRP"}, inplace=True)
            # csv5G.rename(columns={"SSS-RSRQ": "RSRQ"}, inplace=True)
            # csv5G.rename(columns={"SSS-SINR": "SINR"}, inplace=True)
            csv5G['RSRQ'] = csv5G['SSS-RSRQ']
            csv5G['RSRP'] = csv5G['SSS_RSRP']
            csv5G['SINR'] = csv5G['SSS-SINR']
            filtered_csv5G = csv5G[csv5G['MNC'] == '"Op"[3]']


            combined = pd.concat([filtered_csv4G, filtered_csv5G], ignore_index=True)
            all_data.append(combined)

        except Exception as e:
            print(f"{i} failed")
            print(e)
        continue

    full_data = pd.concat(all_data, ignore_index=True)
    for metric in metrics_4G:
        if metric not in full_data.columns:
            print(f"Metric {metric} not found in data. Skipping.")
            continue

        vp = px.violin(full_data,
                        title=f"Operator MNC: Illian - Metric: {metric}",
                       box=True,
                       x='Location',
                       y=metric,
                       range_y=metric_range_map[metric],)
        vp.show()

def OP_Compare_Location_4_5(op):
    loaction_numb=[]
    all_data_4g=[]
    all_data_5g = []
    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/violin_data.csv")
    fig = go.Figure()

    for i in range(1, 16):
        try:
            csv_files_path = f"./4G_2023_passive/location_{i}_od_*.csv"
            all_csv_files = glob.glob(csv_files_path)
            csv4G = pd.concat([pd.read_csv(file) for file in all_csv_files], ignore_index=True)
            csv4G['Location'] = str(i)
            csv4G['type'] = '4G'
            filtered_csv4G = (csv4G[csv4G['MNC'] == op])
            all_data_4g.append(filtered_csv4G)

            csv_files_path = f"./5G_2023_passive/location_{i}_od_*.csv"
            all_csv_files = glob.glob(csv_files_path)

            csv5G = pd.concat([pd.read_csv(file) for file in all_csv_files], ignore_index=True)
            csv5G['Location'] = i
            # csv5G.rename(columns={"SSS_RSRP": "RSRP"}, inplace=True)
            # csv5G.rename(columns={"SSS-RSRQ": "RSRQ"}, inplace=True)
            # csv5G.rename(columns={"SSS-SINR": "SINR"}, inplace=True)
            csv5G['RSRQ'] = csv5G['SSS-RSRQ']
            csv5G['RSRP'] = csv5G['SSS_RSRP']
            csv5G['SINR'] = csv5G['SSS-SINR']
            csv5G['type'] = '5G'
            filtered_csv5G = (csv5G[csv5G['MNC'] == op])
            all_data_5g.append(filtered_csv5G)

        except Exception as e:
            print(f"{i} failed")
            print(e)
        continue

    full_data_4g = pd.concat(all_data_4g, ignore_index=True)
    full_data_5g = pd.concat(all_data_5g, ignore_index=True)
    for metric in metrics_4G:

        fig = go.Figure()
        fig.add_trace(go.Violin(x=full_data_4g['Location'],
                                y=full_data_4g[metric],
                                legendgroup='4G', scalegroup='4G', name='4G',
                                side='negative',
                                line_color='orange')
                      )
        fig.add_trace(go.Violin(x=full_data_5g['Location'],
                                y=full_data_5g[metric],
                                legendgroup='5G', scalegroup='5G', name='5G',
                                side='positive',
                                line_color='purple')
                      )
        fig.update_traces(meanline_visible=True)
        fig.update_layout(violingap=0, violinmode='overlay')

        fig.update_layout(
            title=f" {op} - Metric: {metric}",
            xaxis_title="Location",
            yaxis_title=metric,
            font=dict(size=14),
            legend_title="Technology",
            yaxis_range=metric_range_map[metric],
            xaxis_range=[-0.5, 3.5],
        )

        fig.show()
        # vp = px.violin(full_data,
        #                 title=f"Operator MNC: Illian - Metric: {metric}",
        #                box=True,
        #                x='Location',
        #                y=metric)
        # vp.show()


#one_OP_Compare_Location()
OP_Compare_Location_4_5('"Op"[3]')
# for i in range(4,5):
#     try:
#         csv_files_path = f"./4G_2023_passive/location_{i}_od_capacity_*.csv"
#         all_csv_files = glob.glob(csv_files_path)
#
#         csv4G = pd.concat([pd.read_csv(file) for file in all_csv_files], ignore_index=True)
#         csv4G.sort_values(by=['MNC'], inplace=True)
#         csv4G.replace({'MNC': operators}, inplace=True)
#         print(csv4G['MNC'].unique())
#
#         csv_files_path = f"./5G_2023_passive/location_{i}_od_capacity_*.csv"
#         all_csv_files = glob.glob(csv_files_path)
#
#             # csv_files_path = f"./5G_2023_passive/location_{i}_od_*.csv"
#             # all_csv_files = glob.glob(csv_files_path)
#             #
#             # csv5G = pd.concat([pd.read_csv(file) for file in all_csv_files], ignore_index=True)
#             # csv5G['Location'] = i
#             # filtered_csv5G = csv5G[csv5G['MNC'] == '"Op"[3]']
#             #
#             #
#             # combined = pd.concat([filtered_csv4G, filtered_csv5G], ignore_index=True)
#             all_data.append(filtered_csv4G)
#
#         except Exception as e:
#             print(f"{i} failed")
#             print(e)
#         continue
#     full_data = pd.concat(all_data, ignore_index=True)
#     for metric in metrics_4G:
#         if metric not in full_data.columns:
#             print(f"Metric {metric} not found in data. Skipping.")
#             continue
#         vp = px.violin(full_data, title='Illiad', box=True, x='Location', y=metric, color="Location")
#         vp.show()




#one_OP_Compare_Location()
# for i in range(4,5):
#     try:
#         csv_files_path = f"./4G_2023_passive/location_{i}_od_capacity_*.csv"
#         all_csv_files = glob.glob(csv_files_path)
#
#         csv4G = pd.concat([pd.read_csv(file) for file in all_csv_files], ignore_index=True)
#         csv4G.sort_values(by=['MNC'], inplace=True)
#         csv4G.replace({'MNC': operators}, inplace=True)
#         print(csv4G['MNC'].unique())
#
#         csv_files_path = f"./5G_2023_passive/location_{i}_od_capacity_*.csv"
#         all_csv_files = glob.glob(csv_files_path)
#
#         csv5G = pd.concat([pd.read_csv(file) for file in all_csv_files], ignore_index=True)
#         csv5G.sort_values(by=['MNC'], inplace=True)
#         csv5G.replace({'MNC': operators}, inplace=True)
#
#         plot_graphs(signal="4G", csv=csv4G)
#         # plot_graphs(signal="5G", csv=csv5G)
#
#
#     except Exception as e:
#         print(f"{i} failed")
#         print(e)
#         continue