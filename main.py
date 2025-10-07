import glob
import pandas as pd
import csv

csv_files_path = "./4G_2023_passive/*.csv"
all_csv_files = glob.glob(csv_files_path)

for file_path in all_csv_files:
    print(f"Processing file: {file_path}")

# with open('./4G_2023_passive/location_1_is_capacity_dl+ul_5gnr_tti_1.csv', newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#     for row in spamreader:
#        print(', '.join(row))