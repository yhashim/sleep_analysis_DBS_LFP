from difflib import restore
from distutils.command.install_egg_info import safe_name
from inspect import walktree
from sndhdr import whathdr
import matplotlib as mpl
import matplotlib.pyplot as plt

from matplotlib.dates import DateFormatter

import math, statistics

import numpy as np
import pandas as pd

from datetime import datetime, timedelta
import time

# handle date time conversions between pandas and matplotlib
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from patient import *

def graph(p): 
    hemisphere_frequencies = [[[],[]], [['beta'],['alpha']], [[],['beta']], [['beta'],['alpha']], [[],['alpha']], [['alpha'],['beta']], [['alpha'],['beta']], [['alpha'],[]], [['alpha'],[]], [['beta'],['alpha']]]

    if (len(p.left_diagnostic_data) != 0):
        # preprocessing
        remove_outliers(p, p.left_diagnostic_data, 'left')
        normalize(p, p.left_diagnostic_data, 'left')
        # graphing
        graph_hemisphere(p, p.left_diagnostic_data, str(hemisphere_frequencies[int(p.first_name)-1][0][0]))

    if (len(p.right_diagnostic_data) != 0):
        # preprocessing
        remove_outliers(p, p.right_diagnostic_data, 'right')
        normalize(p, p.right_diagnostic_data, 'right')
        # graphing
        graph_hemisphere(p, p.right_diagnostic_data, str(hemisphere_frequencies[int(p.first_name)-1][1][0]))

def remove_outliers (p, diagnostic_data, hemisphere):
    # remove outliers
    # finds the mean and standard deviation of the data

    # find the mean and standard deviation of the data while retaining 4 dimensional data
    mean = statistics.mean(diagnostic_data, key=lambda diagnostic_data: diagnostic_data[1])
    std = statistics.stdev(diagnostic_data, key=lambda diagnostic_data: diagnostic_data[1])
    
    # removes data points that are more than 3 standard deviations away from the mean
    for i in range(len(diagnostic_data)):
        if (diagnostic_data[i][0] > mean + 3*std or diagnostic_data[i][0] < mean - 3*std):
            diagnostic_data.remove(diagnostic_data[i])
    
    if (hemisphere == 'left'):
        p.left_diagnostic_data = diagnostic_data
    else:
        p.right_diagnostic_data = diagnostic_data

def normalize (p, diagnostic_data, hemisphere):
    # find max local field potential of the data
    max_lfp = max(diagnostic_data, key=lambda diagnostic_data: diagnostic_data[1])
    
    # normalize the data
    for i in range(len(diagnostic_data)):
        diagnostic_data[i][0] = (diagnostic_data[i][0]/max_lfp)*100
    
    if (hemisphere == 'left'):
        p.left_diagnostic_data = diagnostic_data
    else:
        p.right_diagnostic_data = diagnostic_data

def graph_hemisphere(p, diagnostic_data, hemisphere):
    fig, ax = plt.subplots()
    set_ax(ax) 

    sum, num_data = 0, 0
    y_data = []

    # sleep_lfp_sum, nonsleep_lfp_sum = 0, 0
    # sleep_n, nonsleep_n = 0, 0   
    wake_lfp_sum, restless_lfp_sum, light_lfp_sum, deep_lfp_sum, rem_lfp_sum = 0, 0, 0, 0, 0
    wake_n, restless_n, light_n, deep_n, rem_n = 0, 0, 0, 0, 0

    # sleep_lfp = []
    wake_lfp = []
    restless_lfp = []
    light_lfp = []
    deep_lfp = []
    rem_lfp = []

    # print('Subject: ' + p.first_name + ' ' + p.last_name + ', hemisphere: ' + hemisphere)
    ax.set_title('Subject: ' + p.first_name + ' ' + p.last_name + ', hemisphere: ' + hemisphere) 
    for d in diagnostic_data:
            c = 'black'

            for stage in p.stage_starttimes_endtimes:
                for t in stage.data:
                    start = datetime.strptime(t['dateTime'].replace('T', ' ').replace('Z', '').split('.')[0], '%Y-%m-%d %H:%M:%S').timestamp()
                    end = start + t['seconds']

                    try:
                        last_stage = current_stage
                    except:
                        print('first stage')
                    current_stage = t['level']

                    wake_lfp_sum += d[1]
                    wake_n += 1
                    wake_lfp.append(d[1])

                    if current_stage != 'wake' and current_stage != 'awake' and d[0]>=start and d[0]<=end:
                        wake_lfp_sum -= d[1]
                        wake_n -= 1 
                        wake_lfp.pop()

                        # if last_stage != NULL and last_stage != current_stage:
                        #     if last_stage == 'wake' or last_stage == 'awake': 
                        #         if wake_n > 0: 
                        #             x_wake_lfp = wake_lfp_sum/wake_n
                        #             try:
                        #                 p.analysis_rows.append([p.first_name, hemisphere, 'wake', wake_lfp_sum/x_wake_lfp, 'N/A', 'N/A', str((statistics.stdev(wake_lfp)/x_wake_lfp) * 100) + '%'])
                        #             except Exception as e:
                        #                 p.analysis_rows.append([p.first_name, hemisphere, 'wake', wake_lfp_sum/x_wake_lfp, 'N/A', 'N/A', 'N/A'])
                        #                 print('error raised: ', e) 

                        #     last_wake_lfp_sum, last_wake_n = wake_lfp_sum, wake_n
                        #     x_wake_lfp, wake_lfp_sum, wake_n, wake_lfp = 0, 0, 0, []
                        #     if last_stage == 'restless':
                        #         try: 
                        #             x_wake_lfp = wake_lfp_sum/wake_n
                        #             x_restless_lfp = restless_lfp_sum/restless_n
                        #             statistical_values(p, hemisphere, x_restless_lfp, x_wake_lfp, wake_lfp_sum, restless_lfp_sum, wake_n, restless_n, restless_lfp, wake_lfp, 'restless')
                        #         except Exception as e:
                        #             # print('error raised: ', e)
                        #             pass
                        #         x_restless_lfp, x_wake_lfp, wake_lfp_sum, restless_lfp_sum, wake_n, restless_n, restless_lfp, wake_lfp = 0, 0, 0, 0, 0, 0, [], []
                        #     elif last_stage == 'light':
                        #         try: 
                        #             x_wake_lfp = wake_lfp_sum/wake_n
                        #             x_light_lfp = light_lfp_sum/light_n
                        #             statistical_values(p, hemisphere, x_light_lfp, x_wake_lfp, wake_lfp_sum, light_lfp_sum, wake_n, light_n, light_lfp, wake_lfp, 'light')
                        #         except Exception as e:
                        #             # print('error raised: ', e)    
                        #             pass
                        #         x_light_lfp, x_wake_lfp, wake_lfp_sum, light_lfp_sum, wake_n, light_n, light_lfp, wake_lfp = 0, 0, 0, 0, 0, 0, [], []
                        #     elif last_stage == 'deep':
                        #         try: 
                        #             x_wake_lfp = wake_lfp_sum/wake_n
                        #             x_deep_lfp = deep_lfp_sum/deep_n
                        #             statistical_values(p, hemisphere, x_deep_lfp, x_wake_lfp, wake_lfp_sum, deep_lfp_sum, wake_n, deep_n, deep_lfp, wake_lfp, 'deep')
                        #         except Exception as e:
                        #             print('error raised: ', e)
                        #         x_deep_lfp, x_wake_lfp, wake_lfp_sum, deep_lfp_sum, wake_n, deep_n, deep_lfp, wake_lfp = 0, 0, 0, 0, 0, 0, [], []
                        #     elif last_stage == 'rem': 
                        #         try:
                        #             x_wake_lfp = wake_lfp_sum/wake_n
                        #             x_rem_lfp = rem_lfp_sum/rem_n
                        #             statistical_values(p, hemisphere, x_rem_lfp, x_wake_lfp, wake_lfp_sum, rem_lfp_sum, wake_n, rem_n, rem_lfp, wake_lfp, 'rem')
                        #         except Exception as e:
                        #             print('error raised: ', e)
                        #         x_rem_lfp, x_wake_lfp, wake_lfp_sum, rem_lfp_sum, wake_n, rem_n, rem_lfp, wake_lfp = 0, 0, 0, 0, 0, 0, [], []
                        if current_stage == 'restless':
                            c = 'greenyellow'
                            restless_lfp_sum += d[1]
                            restless_n += 1
                            restless_lfp.append(d[1])
                        if current_stage == 'light':
                            c = 'lightblue'
                            light_lfp_sum += d[1]
                            light_n += 1
                            light_lfp.append(d[1])
                        elif current_stage == 'deep':
                            c = 'deepskyblue'
                            deep_lfp_sum += d[1]
                            deep_n += 1
                            deep_lfp.append(d[1])
                        elif current_stage == 'rem':
                            c = 'dodgerblue'
                            rem_lfp_sum += d[1]
                            rem_n += 1
                            rem_lfp.append(d[1])                            
            
            ax.plot(d[0], d[1], linestyle='-', marker='.', c=c)
            # ax.plot(d[0], d[3], linestyle='-', marker='.', c=c)

            sum += d[1]
            num_data += 1

            y_data.append(d[1])

           
    start_end = []

    # for i in range(len(labelled_diagnostic_data)-1):
    #     if labelled_diagnostic_data[i][2] == False and labelled_diagnostic_data[i+1][2] == True:
    #         # non-sleep to sleep: sleep start time
    #         print('sleep start time: ' + str(labelled_diagnostic_data[i+1][0]))
    #         start_end.append(labelled_diagnostic_data[i+1][3])
    #     elif labelled_diagnostic_data[i][2] == True and labelled_diagnostic_data[i+1][2] == False:
    #         # sleep to non-sleep: sleep end time
    #         print('sleep end time: ' + str(labelled_diagnostic_data[i][0]))
    #         start_end.append(labelled_diagnostic_data[i][3])
    #         print()

    # print()

    # x_sleep_lfp = sleep_lfp_sum/sleep_n
    # x_nonsleep_lfp = nonsleep_lfp_sum/nonsleep_n

    # statistical_values(x_sleep_lfp, x_nonsleep_lfp, nonsleep_lfp_sum, sleep_lfp_sum, nonsleep_n, sleep_n, sleep_lfp)
    
    x_lfp = (wake_lfp_sum + restless_lfp_sum + light_lfp_sum + deep_lfp_sum + rem_lfp_sum)/(wake_n + restless_n + light_n + deep_n + rem_n)
    x_wake_lfp = wake_lfp_sum/wake_n
    try:
        # divide by mean lfp
        p.analysis_rows.append([p.first_name, hemisphere, 'wake', wake_lfp_sum/x_lfp, 'N/A', 'N/A', str((statistics.stdev(wake_lfp)/x_wake_lfp) * 100) + '%'])
    except Exception as e:
        p.analysis_rows.append([p.first_name, hemisphere, 'wake', wake_lfp_sum/x_lfp, 'N/A', 'N/A', 'N/A'])
        print('error raised: ', e) 

    try: 
        x_restless_lfp = restless_lfp_sum/restless_n
        statistical_values(p, hemisphere, x_restless_lfp, x_wake_lfp, wake_lfp_sum, restless_lfp_sum, wake_n, restless_n, restless_lfp, wake_lfp, x_lfp, 'restless')
    except Exception as e:
        print('error raised: ', e)
    
    try: 
        x_light_lfp = light_lfp_sum/light_n
        statistical_values(p, hemisphere, x_light_lfp, x_wake_lfp, wake_lfp_sum, light_lfp_sum, wake_n, light_n, light_lfp, wake_lfp, x_lfp, 'light')
    except Exception as e:
        print('error raised: ', e)    
    
    try: 
        x_deep_lfp = deep_lfp_sum/deep_n
        statistical_values(p, hemisphere, x_deep_lfp, x_wake_lfp, wake_lfp_sum, deep_lfp_sum, wake_n, deep_n, deep_lfp, wake_lfp, x_lfp, 'deep')
    except Exception as e:
        print('error raised: ', e)
    
    try:
        x_rem_lfp = rem_lfp_sum/rem_n
        statistical_values(p, hemisphere, x_rem_lfp, x_wake_lfp, wake_lfp_sum, rem_lfp_sum, wake_n, rem_n, rem_lfp, wake_lfp, x_lfp, 'rem')
    except Exception as e:
        print('error raised: ', e)

    # limits(p, ax, sum, num_data, y_data)
    p.graphs.append(ax)

def set_ax(ax):
    # plt.rcParams['text.usetex'] = True
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Local field potential')
    
    plt.rcParams['xtick.major.size'] = 5.0
    plt.rcParams['xtick.minor.size'] = 3.0

    plt.rcParams['ytick.major.size'] = 5.0
    plt.rcParams['ytick.minor.size'] = 3.0

    ax.xaxis.set_minor_locator(plt.MaxNLocator(8*5))
    ax.yaxis.set_minor_locator(plt.MaxNLocator(11*5))

    ax.xaxis.set_major_locator(plt.MaxNLocator(8))
    ax.yaxis.set_major_locator(plt.MaxNLocator(11))

# def limits(p, ax, sum, num_data, y_data):
#     # relative_threshold = sum/num_data
#     # ax.axhline(y=relative_threshold, linestyle='-', c='black')
    
#     ypbot = np.percentile(y_data, 1)
#     yptop = np.percentile(y_data, 99)
#     ypad = 0.2*(yptop - ypbot)
#     y_min = ypbot - ypad
#     y_max = yptop + ypad

#     ax.set_ylim([y_min, y_max])

# def statistical_values(x_sleep_lfp, x_nonsleep_lfp, nonsleep_lfp_sum, sleep_lfp_sum, nonsleep_n, sleep_n, sleep_lfp):
def statistical_values(p, hemisphere, x_sleep_lfp, x_nonsleep_lfp, nonsleep_lfp_sum, sleep_lfp_sum, nonsleep_n, sleep_n, sleep_lfp, nonsleep_lfp, x_lfp, stage):
    # depth
    difference = ''
    if (x_sleep_lfp < x_nonsleep_lfp):
        # print('sleep lfp lower than nonsleep lfp')
        difference = 'decrease'
        # print(stage + ' lfp lower than nonsleep lfp')
    else:
        # print('sleep lfp higher than nonsleep lfp')
        difference = 'increase'
        # print(stage + ' lfp higher than nonsleep lfp')
    # print('depth = ' + str(abs(x_nonsleep_lfp - x_sleep_lfp)))

    # print('mean sleep lfp = ' + str(x_sleep_lfp))
    relative_depth = str(abs(x_nonsleep_lfp - x_sleep_lfp)/((nonsleep_lfp_sum + sleep_lfp_sum)/(nonsleep_n + sleep_n))*100) + '%'
    # print('relative depth = ' + relative_depth)

    # max_min_difference = max(sleep_lfp) - min(sleep_lfp)
    # interquartile_range = np.percentile(np.array(sleep_lfp), 75, interpolation='midpoint') - np.percentile(np.array(sleep_lfp), 25, interpolation='midpoint')
    
    standard_deviation = statistics.stdev(sleep_lfp)
    # variance = statistics.variance(sleep_lfp)

    relative_standard_deviation = str((standard_deviation/x_sleep_lfp) * 100) + '%'

    # print('range = ' + str(max_min_difference) + ', interquartile range = ' + str(interquartile_range) + ', standard deviation = ' + str(standard_deviation) + ', variance = ' + str(variance))
    # print('relative standard deviation = ' + relative_standard_deviation)
    # print()

    if difference == 'decrease':
        p.analysis_rows.append([p.first_name, hemisphere, stage, sleep_lfp_sum/x_lfp, difference, relative_depth, relative_standard_deviation])
    else:
        p.analysis_rows.append([p.first_name, hemisphere, stage, sleep_lfp_sum/x_lfp, difference, '-' + relative_depth, relative_standard_deviation])
    # try:
    #     p.analysis_rows.append([p.first_name, hemisphere, 'wake', nonsleep_lfp_sum/x_nonsleep_lfp, 'N/A', 'N/A', str((statistics.stdev(nonsleep_lfp)/x_nonsleep_lfp) * 100) + '%'])
    # except Exception as e:
    #     p.analysis_rows.append([p.first_name, hemisphere, 'wake', nonsleep_lfp_sum/x_nonsleep_lfp, 'N/A', 'N/A', 'N/A'])
    #     print('error raised: ', e)
