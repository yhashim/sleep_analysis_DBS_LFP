import matplotlib as mpl
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

import math, statistics

import numpy as np
import pandas as pd

def figure(): 
    fig, ax = plt.subplots()
    set_ax(ax) 

    ax = plt.figure().gca(projection='3d')
    set_ax(ax)
    
    scores = [[121,1,12], [(82+112)/2,(5+7)/2,10], [(110+120)/2,(3+4)/2,2], [88,6,10], [96,2,10], [131,1,2], [64,3,2], [125,2,12], [124,2,9]]
    
    alpha_statistics = [[18.96,19.21,121,1,12], [9.21,29.84,(110+120)/2,(3+4)/2,2], [20.88,93.94,88,6,10], [39.73,38.58,96,2,10], [54.91,262.77,131,1,2], [-19.99,59.00,64,3,2], [-4.53,50.33,125,2,12], [5.92,140.79,124,2,9]]
    beta_statistics = [[9.56,15.85,121,1,12], [8.61,10.31,(82+112)/2,(5+7)/2,10], [-5.44,39.75,(110+120)/2,(3+4)/2,2], [24.72,160.83,96,2,10], [12.60,444.12,131,1,2], [-0.02,40.03,124,2,9]]

    ax.set_title('')
    for s in scores:
        # ax.scatter3D(s[n], s[n], s[n], linestyle='-', marker='.')
        ax.plot(s[n], s[n], linestyle='-', marker='.', c='blue')

    ax.set_title('')
    for statistic in _statistics:
        ax.plot(statistic[n],statistic[n], linestyle='-', marker='.', c='blue')

    subject002a = [[38.91,22.97,5], [18.74,26.42,5], [34.82,18.14,5], [8.16,12.45,5], [30.28,22.95,5], [5.16,18.81,5], [11.51,17.05,5]]
    subject002b = [[11.97,15.83,5], [2.72,14.55,5], [19.62,18.91,5], [-0.11,15.75,5], [21.35,20.11,5], [-4.70,21.10,5], [11.74,12.15,5]]

    subject003b = [[3.65,6.89,3], [-0.81,8.84,4], [23.92,8.31,4]]

    subject004a = [[-0.77,32.63,1], [2.68,28.50,4], [-11.24,44.56,4], [3.00,26.62,5], [43.60,12.11,2], [22.99,49.85,4], [10.46,17.88,3]]
    subject004b = [[22.90,29.55,1], [-8.64,29.78,4], [7.28,19.56,4], [-9.43,15.08,5], [-20.85,14.36,2], [-10.24,18.53,4], [-14.50,17.06,3]]

    subject005a = [[19.91,86.84,3], [43.51,52.47,3], [53.50,109.79,3], [-12.37,179.91,3], [26.10,107.56,3], [125.57,82.23,3]]

    subject006a = [[-3.94,24.94,3], [-23.23,18.42,2], [75.06,50.82,2]]
    subject006b = [[-10.83,17.70,3], [-38.73,15.43,2], [2.96,11.92,2]]

    subject007a = [[112.01,456.99,3], [-77.31,746.91,3]]
    subject007b = [[7.56,499.59,3], [-76.96,747.29,3]]

    subject008a = [[-24.07,57.84,3], [-52.38,61.59,3], [-42.81,48.47,3], [-43.81,48.47,3], [-74.77, 45.54,3]]
    
    subject009a = [[-27.05,50.05,4],[-31.93,70.35,4], [19.67,54.21,3], [32.36,48.77,4], [5.76,39.52,2]]

    subject010a = [[-12.47,192.35,3], [76.37,162.54,3], [-53.49,124.66,4], [-36.06,196.69,3], [-4.13,30.62,2], [-46.37,227.08,4]]
    subject010b = [[7.78,42.96,3], [17.16,37.74,3], [-12.88,42.24,4], [-43.89,66.55,3], [0.90,55.13,2], [-0.28,11.03,4]]

    alpha = [subject002a, subject004a, subject005a, subject006a, subject007a, subject008a, subject009a, subject010a]
    beta = [subject002b, subject003b, subject004b, subject006b, subject007b, subject010b]
    
    ratio = [[subject002a,subject002b], [subject004a,subject004b], [subject006a,subject006b], [subject007a, subject007b], [subject010a, subject010b]]

    ax.set_title('Alpha/beta:alpha/beta variable1 to variable2 (n = )')
    for subject in ratio:
        for i in range(len(subject[0])):
            score = subject[0][i][2]

            a_rd = subject[0][i][0]
            b_rd = subject[1][i][0]

            a_rsd = subject[0][i][1]
            b_rsd = subject[1][i][1]

            sum_rd = a_rd + b_rd
            a_to_b_rd = a_rd/b_rd
            b_to_a_rd = b_rd/a_rd    

            sum_rsd = a_rsd + b_rsd
            a_to_b_rsd = a_rsd/b_rsd
            b_to_a_rsd = b_rsd/a_rsd  

            ax.scatter(sum_rd, score, linestyle='-', marker='.', c='blue') 
            #ax.scatter(sum_rsd, score, linestyle='-', marker='.', c='blue')

            #ax.scatter(a_to_b_rd, score, linestyle='-', marker='.', c='blue')
            #ax.scatter(a_to_b_rsd, score, linestyle='-', marker='.', c='blue')

            #ax.scatter(b_to_a_rd, score, linestyle='-', marker='.', c='blue')
            #ax.scatter(b_to_a_rsd, score, linestyle='-', marker='.', c='blue')

    # ax.set_title('Alpha/beta variable1 to variable2 (n = )')   
    # for subject in alpha:
    # for subject in beta:
    #     for cycle in subject:
    #         ax.scatter(cycle[1],cycle[2], linestyle='-', marker='.', c='blue')

def set_ax(ax):
    # plt.rcParams['text.usetex'] = True
    
    # ax.set_xlabel('Parkinson\'s disease sleep scale')
    # ax.set_xlabel('Restless leg syndrome screening questionnaire')
    # ax.set_ylabel('Epworth sleepiness scale')
    
    #ax.set_xlabel('Relative depth %')
    #ax.set_xlabel('Relative standard deviation %')
    #ax.set_ylabel('Recorded sleep score (0-5)')
