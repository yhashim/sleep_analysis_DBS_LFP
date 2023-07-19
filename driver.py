import json, csv

import matplotlib as mpl
import matplotlib.pyplot as plt

from parser import parse, patients

from analysis import *

from grapher import graph
from figures import figure

with open('file_names.txt') as fn:
    file_names = fn.readlines()

for fn in file_names:
    parse(fn.split('\n')[0])

for p in patients:
    graph(p)

# new_file = 'stages.csv'
new_file = 'wake.csv'
fields = ['Number', 'Frequency Range', 'Stage', 'Relative mean local field potential', 'Increase or decrease in sleep', 'Relative depth %', 'Relative standard deviation %']

with open(new_file, 'w') as csvfile2: 
    csvwriter2 = csv.writer(csvfile2) 
    csvwriter2.writerow(fields)
    for p in patients:
    
    # mean_file = 'mean.csv'
    # new_file = p.first_name + 'analysis.csv'

    # restless, light, deep, rem = [[0, 0, 0, 0, 'restless'], [0, 0, 0, 0, 'restless']], [[0, 0, 0, 0, 'light'], [0, 0, 0, 0, 'light']], [[0, 0, 0, 0, 'deep'], [0, 0, 0, 0, 'deep']], [[0, 0, 0, 0, 'rem'], [0, 0, 0, 0, 'rem']]

    # with open(mean_file, 'w') as csvfile1:
        # csvwriter1 = csv.writer(csvfile1) 
        # csvwriter1.writerow(['Number', 'Hemisphere', 'Increase or decrease in sleep', 'Relative depth %', 'Relative standard deviation %'])
    
        # epoch = 1
        for r in p.analysis_rows:
            row = [p.first_name, r[0], r[1], r[2], r[3], r[4], r[5]]
            csvwriter2.writerow(r)
            # epoch += 1
                
            #     hemisphere, stage, difference, relative_depth, relative_standard_deviation = r[0], r[1], r[2], r[3], r[4]
            #     if hemisphere == 'left':
            #         mean(0, stage, restless, light, deep, rem, difference, relative_depth, relative_standard_deviation)      
            #     else:
            #         mean(1, stage, restless, light, deep, rem, difference, relative_depth, relative_standard_deviation)   
            
            # stages = [restless, light, deep, rem]
            # for stage in stages:
            #     for hemisphere in stage:
            #         if hemisphere[2] > 0:
            #             hemisphere[1] = 'decrease'
            #         elif hemisphere[2] == 0:
            #             hemisphere[1] = 'none'
            #         else:
            #             hemisphere[1] = 'increase'
            #         try: 
            #             hemisphere[2], hemisphere[3] = str(hemisphere[2]/hemisphere[0]) + '%', str(hemisphere[3]/hemisphere[0]) + '%'
            #         except Exception as e:
            #             print('error raised: ', e)
            #         new_row = [p.first_name, hemisphere[4], hemisphere[1], hemisphere[2], hemisphere[3]]
            #         csvwriter1.writerow(new_row)
        # csvwriter2.writerow(['Epoch count: ' + str(epoch), '', '', ''])

# figure()

plt.show()