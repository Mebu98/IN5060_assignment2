
import csv

with open('./4G_2023_passive/location_1_is_capacity_dl+ul_5gnr_tti_1.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
       print(', '.join(row))