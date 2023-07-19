import csv
import math

from scipy.stats import differential_entropy

file_names = ['002left_LFP', '002right_LFP', '003right_LFP', '004left_LFP', '004right_LFP', '005right_LFP', '006left_LFP', '006right_LFP', '007left_LFP', '007right_LFP', '008left_LFP', '009left_LFP', '010left_LFP', '010right_LFP']

complete_list = []

allPD_alpha, allPD_beta = [], []

allPD_STN_beta, allPD_STN_alpha = [], []
allPD_GPI_beta, allPD_GPI_alpha = [], []

allNonPD_alpha = []

allNonPD_STN_alpha, allNonPD_GPI_alpha = [], []

allET_alpha = []

for file_name in file_names:
    current_csv = file_name + '.csv'
    subject_n = int(current_csv[0:3])

    # read csv file and store in list
    # skip first row
    with open(current_csv, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        data = list(reader)

    frequency_band = data[0][5]

    wake, restless, light, deep, rem = [], [], [], [], []
    sleepAdd = []

    for row in data:
        if row[2] == '0':
            wake.append(row)
        elif row[2] == '1': 
            restless.append(row)
        elif row[2] == '2':
            light.append(row)
        elif row[2] == '3':
            deep.append(row)
        elif row[2] == '4':
            rem.append(row)
        elif row[2] == '5':
            sleepAdd.append(row)

    sleep = restless + light + deep + rem + sleepAdd

    wake_mean, wake_std, wake_var, wake_entropy = 'NULL', 'NULL', 'NULL', 'NULL'
    restless_mean, restless_comparison, restless_difference, restless_std, restless_var, restless_entropy = 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL'
    light_mean, light_comparison, light_difference, light_std, light_var, light_entropy = 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL'
    deep_mean, deep_comparison, deep_difference, deep_std, deep_var, deep_entropy = 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL'
    rem_mean, rem_comparison, rem_difference, rem_std, rem_var, rem_entropy = 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL'
    sleep_mean, sleep_comparison, sleep_difference, sleep_std, sleep_var, sleep_entropy = 'NULL', 'NULL', 'NULL', 'NULL', 'NULL', 'NULL'

    # calculate mean local field potential for each stage 
    try: wake_mean = sum([float(row[1]) for row in wake]) / len(wake)
    except Exception as e:
        print("mean error raised is: ", e)
    try: restless_mean = sum([float(row[1]) for row in restless]) / len(restless)
    except Exception as e:
        print("mean error raised is: ", e)
    try: light_mean = sum([float(row[1]) for row in light]) / len(light)
    except Exception as e:
        print("mean error raised is: ", e)
    try: deep_mean = sum([float(row[1]) for row in deep]) / len(deep)
    except Exception as e:
        print("mean error raised is: ", e)
    try: rem_mean = sum([float(row[1]) for row in rem]) / len(rem)
    except Exception as e:
        print("mean error raised is: ", e)
    try: sleep_mean = sum([float(row[1]) for row in sleep]) / len(sleep)
    except Exception as e:
        print("mean error raised is: ", e)

    # calculate standard deviation of local field potential for each stage 
    try: wake_std = (sum([(float(row[1]) - wake_mean)**2 for row in wake]) / len(wake))**0.5
    except Exception as e:
        print("standard deviation error raised is: ", e)
    try: restless_std = (sum([(float(row[1]) - restless_mean)**2 for row in restless]) / len(restless))**0.5
    except Exception as e:
        print("standard deviation error raised is: ", e)
    try: light_std = (sum([(float(row[1]) - light_mean)**2 for row in light]) / len(light))**0.5
    except Exception as e:
        print("standard deviation error raised is: ", e)
    try: deep_std = (sum([(float(row[1]) - deep_mean)**2 for row in deep]) / len(deep))**0.5
    except Exception as e:
        print("standard deviation error raised is: ", e)
    try: rem_std = (sum([(float(row[1]) - rem_mean)**2 for row in rem]) / len(rem))**0.5
    except Exception as e:
        print("standard deviation error raised is: ", e)
    try: sleep_std = (sum([(float(row[1]) - sleep_mean)**2 for row in sleep]) / len(sleep))**0.5
    except Exception as e:
        print("standard deviation error raised is: ", e)

    # calculate variance of local field potential for each stage 
    try: wake_var = wake_std**2
    except Exception as e:
        print("wake variance error raised is: ", e)
    try: restless_var = restless_std**2
    except Exception as e:
        print("restless variance error raised is: ", e)
        print(restless_std)
        restless_var = 'NULL'
    try: light_var = light_std**2
    except Exception as e:
        print("light variance error raised is: ", e)
    try: deep_var = deep_std**2
    except Exception as e:
        print("deep variance error raised is: ", e)
    try: rem_var = rem_std**2
    except Exception as e:
        print("rem variance error raised is: ", e)
    try: sleep_var = sleep_std**2
    except Exception as e:
        print("sleep variance error raised is: ", e)

    # go through each stage list and add for each row another column indicating the frequency of the LFP (row[1]) in the stage
    wake_lfps, restless_lfps, light_lfps, deep_lfps, rem_lfps, sleep_lfps = [], [], [], [], [], []
    for row in wake:
        wake_lfps.append(float(row[1]))
    for row in restless:
        restless_lfps.append(float(row[1]))
    for row in light:
        light_lfps.append(float(row[1]))
    for row in deep:
        deep_lfps.append(float(row[1]))
    for row in rem:
        rem_lfps.append(float(row[1]))
    for row in sleep:
        sleep_lfps.append(float(row[1]))

    # calculate differential entropy of local field potential for each stage
    try: wake_entropy = differential_entropy(wake_lfps)
    except Exception as e:
        print("wake differential entropy error raised is: ", e)
    try: restless_entropy = differential_entropy(restless_lfps)
    except Exception as e:
        print("restless differential entropy error raised is: ", e)
        restless_entropy = 'NULL'
    try: light_entropy = differential_entropy(light_lfps)
    except Exception as e:
        print("light differential entropy error raised is: ", e)
    try: deep_entropy = differential_entropy(deep_lfps)
    except Exception as e:
        print("deep differential entropy error raised is: ", e)
    try: rem_entropy = differential_entropy(rem_lfps)
    except Exception as e:
        print("rem differential entropy error raised is: ", e)
    try: sleep_entropy = differential_entropy(sleep_lfps)
    except Exception as e:
        print("sleep differential entropy error raised is: ", e)

    # calculate entropy of local field potential for each stage 
    # try: wake_entropy = -sum([(float(row[1]) / wake_mean) * math.log(float(row[1]) / wake_mean) for row in wake])
    # except Exception as e:
    #     print("error raised is: ", e)
    # try: restless_entropy = -sum([(float(row[1]) / restless_mean) * math.log(float(row[1]) / restless_mean) for row in restless])
    # except Exception as e:
    #     print("error raised is: ", e)
    # try: light_entropy = -sum([(float(row[1]) / light_mean) * math.log(float(row[1]) / light_mean) for row in light])
    # except Exception as e:
    #     print("error raised is: ", e)
    # try: deep_entropy = -sum([(float(row[1]) / deep_mean) * math.log(float(row[1]) / deep_mean) for row in deep])
    # except Exception as e:
    #     print("error raised is: ", e)
    # try: rem_entropy = -sum([(float(row[1]) / rem_mean) * math.log(float(row[1]) / rem_mean) for row in rem])
    # except Exception as e:
    #     print("error raised is: ", e)
    # try: sleep_entropy = -sum([(float(row[1]) / sleep_mean) * math.log(float(row[1]) / sleep_mean) for row in sleep])
    # except Exception as e:
    #     print("error raised is: ", e)

    # variable for each stage stating whether or not the stage mean is greater or less than the wake mean
    try:
        if (restless_mean > wake_mean):
            restless_comparison = 'greater'
        elif (restless_mean < wake_mean):
            restless_comparison = 'less'
        else:
            restless_comparison = 'equal'
    except Exception as e:
        print("error raised is: ", e)
    try:
        if (light_mean > wake_mean):
            light_comparison = 'greater'
        elif (light_mean < wake_mean):
            light_comparison = 'less'
        else:
            light_comparison = 'equal'
    except Exception as e:
        print("error raised is: ", e)
    try:
        if (deep_mean > wake_mean):
            deep_comparison = 'greater'
        elif (deep_mean < wake_mean):
            deep_comparison = 'less'
        else:
            deep_comparison = 'equal'
    except Exception as e:
        print("error raised is: ", e)
    try:
        if (rem_mean > wake_mean):
            rem_comparison = 'greater'
        elif (rem_mean < wake_mean):
            rem_comparison = 'less'
        else:
            rem_comparison = 'equal'
    except Exception as e:
        print("error raised is: ", e)
    try:
        if (sleep_mean > wake_mean):
            sleep_comparison = 'greater'
        elif (sleep_mean < wake_mean):
            sleep_comparison = 'less'
        else:
            sleep_comparison = 'equal'
    except Exception as e:
        print("error raised is: ", e)

    # variable for each stage calculating difference between stage mean and wake mean
    try: restless_difference = restless_mean - wake_mean
    except Exception as e:
        print("error raised is: ", e)
    try: light_difference = light_mean - wake_mean
    except Exception as e:
        print("error raised is: ", e)
    try: deep_difference = deep_mean - wake_mean
    except Exception as e:
        print("error raised is: ", e)
    try: rem_difference = rem_mean - wake_mean
    except Exception as e:
        print("error raised is: ", e)
    try: sleep_difference = sleep_mean - wake_mean
    except Exception as e:
        print("error raised is: ", e)

    # write results to new csv file summarizing each stage's statistics in individual rows
    with open(current_csv[0:3] + frequency_band + '_statistics.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Stage', 'Stage Number', 'Sleep or Wake', 'Mean', 'Wake Comparison', 'Wake Difference', 'Standard Deviation', 'Variance', 'Entropy'])
        writer.writerow(['Wake', 0, 0, wake_mean, 'N/A', 'N/A', wake_std, wake_var, wake_entropy])
        writer.writerow(['Restless', 1, 1, restless_mean, restless_comparison, restless_difference, restless_std, restless_var, restless_entropy])
        writer.writerow(['Light', 2, 1, light_mean, light_comparison, light_difference, light_std, light_var, light_entropy])
        writer.writerow(['Deep', 3, 1, deep_mean, deep_comparison, deep_difference, deep_std, deep_var, deep_entropy])
        writer.writerow(['REM', 4, 1, rem_mean, rem_comparison, rem_difference, rem_std, rem_var, rem_entropy])
        writer.writerow(['Sleep', 5, 1, sleep_mean, sleep_comparison, sleep_difference, sleep_std, sleep_var, sleep_entropy])

    complete_list.append([subject_n, frequency_band, 'Wake', 0, 0, wake_mean, 'N/A', 'N/A', wake_std, wake_var, wake_entropy])
    complete_list.append([subject_n, frequency_band, 'Restless', 1, 1, restless_mean, restless_comparison, restless_difference, restless_std, restless_var, restless_entropy])
    complete_list.append([subject_n, frequency_band, 'Light', 2, 1, light_mean, light_comparison, light_difference, light_std, light_var, light_entropy])
    complete_list.append([subject_n, frequency_band, 'Deep', 3, 1, deep_mean, deep_comparison, deep_difference, deep_std, deep_var, deep_entropy])
    complete_list.append([subject_n, frequency_band, 'REM', 4, 1, rem_mean, rem_comparison, rem_difference, rem_std, rem_var, rem_entropy])
    complete_list.append([subject_n, frequency_band, 'Sleep', 5, 1, sleep_mean, sleep_comparison, sleep_difference, sleep_std, sleep_var, sleep_entropy])

    # beta:
    # pd: 002left, 003right, 004left, 007right, 010right
    # non-pd: 006right (no)

    # alpha: 
    # pd: 002right, 004right, 005right, 007left, 010left
    # non-pd: 006left, 008left, 009left

    # pd: 
    # stn: 002, 003, 005, 010
    # gpi: 004, 007

    # nonpd: 
    # gpi: 006
    # vim: 008, 009 

    if frequency_band == 'alpha':
        if subject_n == 2 or subject_n == 4 or subject_n == 5 or subject_n == 7 or subject_n == 10:
            allPD_alpha.append([subject_n, frequency_band, 'Wake', 0, 0, wake_mean, 'N/A', 'N/A', wake_std, wake_var, wake_entropy])
            allPD_alpha.append([subject_n, frequency_band, 'Restless', 1, 1, restless_mean, restless_comparison, restless_difference, restless_std, restless_var, restless_entropy])
            allPD_alpha.append([subject_n, frequency_band, 'Light', 2, 1, light_mean, light_comparison, light_difference, light_std, light_var, light_entropy])
            allPD_alpha.append([subject_n, frequency_band, 'Deep', 3, 1, deep_mean, deep_comparison, deep_difference, deep_std, deep_var, deep_entropy])
            allPD_alpha.append([subject_n, frequency_band, 'REM', 4, 1, rem_mean, rem_comparison, rem_difference, rem_std, rem_var, rem_entropy])
            allPD_alpha.append([subject_n, frequency_band, 'Sleep', 5, 1, sleep_mean, sleep_comparison, sleep_difference, sleep_std, sleep_var, sleep_entropy])
            if subject_n == 2 or subject_n == 5 or subject_n == 10:
                allPD_STN_alpha.append([subject_n, frequency_band, 'Wake', 0, 0, wake_mean, 'N/A', 'N/A', wake_std, wake_var, wake_entropy])
                allPD_STN_alpha.append([subject_n, frequency_band, 'Restless', 1, 1, restless_mean, restless_comparison, restless_difference, restless_std, restless_var, restless_entropy])
                allPD_STN_alpha.append([subject_n, frequency_band, 'Light', 2, 1, light_mean, light_comparison, light_difference, light_std, light_var, light_entropy])
                allPD_STN_alpha.append([subject_n, frequency_band, 'Deep', 3, 1, deep_mean, deep_comparison, deep_difference, deep_std, deep_var, deep_entropy])
                allPD_STN_alpha.append([subject_n, frequency_band, 'REM', 4, 1, rem_mean, rem_comparison, rem_difference, rem_std, rem_var, rem_entropy])
                allPD_STN_alpha.append([subject_n, frequency_band, 'Sleep', 5, 1, sleep_mean, sleep_comparison, sleep_difference, sleep_std, sleep_var, sleep_entropy])
            elif subject_n == 4 or subject_n == 7:
                allPD_GPI_alpha.append([subject_n, frequency_band, 'Wake', 0, 0, wake_mean, 'N/A', 'N/A', wake_std, wake_var, wake_entropy])
                allPD_GPI_alpha.append([subject_n, frequency_band, 'Restless', 1, 1, restless_mean, restless_comparison, restless_difference, restless_std, restless_var, restless_entropy])
                allPD_GPI_alpha.append([subject_n, frequency_band, 'Light', 2, 1, light_mean, light_comparison, light_difference, light_std, light_var, light_entropy])
                allPD_GPI_alpha.append([subject_n, frequency_band, 'Deep', 3, 1, deep_mean, deep_comparison, deep_difference, deep_std, deep_var, deep_entropy])
                allPD_GPI_alpha.append([subject_n, frequency_band, 'REM', 4, 1, rem_mean, rem_comparison, rem_difference, rem_std, rem_var, rem_entropy])
                allPD_GPI_alpha.append([subject_n, frequency_band, 'Sleep', 5, 1, sleep_mean, sleep_comparison, sleep_difference, sleep_std, sleep_var, sleep_entropy])
        elif subject_n == 6 or subject_n == 8 or subject_n == 9:
            allNonPD_alpha.append([subject_n, frequency_band, 'Wake', 0, 0, wake_mean, 'N/A', 'N/A', wake_std, wake_var, wake_entropy])
            allNonPD_alpha.append([subject_n, frequency_band, 'Restless', 1, 1, restless_mean, restless_comparison, restless_difference, restless_std, restless_var, restless_entropy])
            allNonPD_alpha.append([subject_n, frequency_band, 'Light', 2, 1, light_mean, light_comparison, light_difference, light_std, light_var, light_entropy])
            allNonPD_alpha.append([subject_n, frequency_band, 'Deep', 3, 1, deep_mean, deep_comparison, deep_difference, deep_std, deep_var, deep_entropy])
            allNonPD_alpha.append([subject_n, frequency_band, 'REM', 4, 1, rem_mean, rem_comparison, rem_difference, rem_std, rem_var, rem_entropy])
            allNonPD_alpha.append([subject_n, frequency_band, 'Sleep', 5, 1, sleep_mean, sleep_comparison, sleep_difference, sleep_std, sleep_var, sleep_entropy])
    else:
        if subject_n == 2 or subject_n == 3 or subject_n == 4 or subject_n == 7 or subject_n == 10:
            allPD_beta.append([subject_n, frequency_band, 'Wake', 0, 0, wake_mean, 'N/A', 'N/A', wake_std, wake_var, wake_entropy])
            allPD_beta.append([subject_n, frequency_band, 'Restless', 1, 1, restless_mean, restless_comparison, restless_difference, restless_std, restless_var, restless_entropy])
            allPD_beta.append([subject_n, frequency_band, 'Light', 2, 1, light_mean, light_comparison, light_difference, light_std, light_var, light_entropy])
            allPD_beta.append([subject_n, frequency_band, 'Deep', 3, 1, deep_mean, deep_comparison, deep_difference, deep_std, deep_var, deep_entropy])
            allPD_beta.append([subject_n, frequency_band, 'REM', 4, 1, rem_mean, rem_comparison, rem_difference, rem_std, rem_var, rem_entropy])
            allPD_beta.append([subject_n, frequency_band, 'Sleep', 5, 1, sleep_mean, sleep_comparison, sleep_difference, sleep_std, sleep_var, sleep_entropy])
            if subject_n == 2 or subject_n == 3 or subject_n == 10:
                allPD_STN_beta.append([subject_n, frequency_band, 'Wake', 0, 0, wake_mean, 'N/A', 'N/A', wake_std, wake_var, wake_entropy])
                allPD_STN_beta.append([subject_n, frequency_band, 'Restless', 1, 1, restless_mean, restless_comparison, restless_difference, restless_std, restless_var, restless_entropy])
                allPD_STN_beta.append([subject_n, frequency_band, 'Light', 2, 1, light_mean, light_comparison, light_difference, light_std, light_var, light_entropy])
                allPD_STN_beta.append([subject_n, frequency_band, 'Deep', 3, 1, deep_mean, deep_comparison, deep_difference, deep_std, deep_var, deep_entropy])
                allPD_STN_beta.append([subject_n, frequency_band, 'REM', 4, 1, rem_mean, rem_comparison, rem_difference, rem_std, rem_var, rem_entropy])
                allPD_STN_beta.append([subject_n, frequency_band, 'Sleep', 5, 1, sleep_mean, sleep_comparison, sleep_difference, sleep_std, sleep_var, sleep_entropy])
            elif subject_n == 4 or subject_n == 7:
                allPD_GPI_beta.append([subject_n, frequency_band, 'Wake', 0, 0, wake_mean, 'N/A', 'N/A', wake_std, wake_var, wake_entropy])
                allPD_GPI_beta.append([subject_n, frequency_band, 'Restless', 1, 1, restless_mean, restless_comparison, restless_difference, restless_std, restless_var, restless_entropy])
                allPD_GPI_beta.append([subject_n, frequency_band, 'Light', 2, 1, light_mean, light_comparison, light_difference, light_std, light_var, light_entropy])
                allPD_GPI_beta.append([subject_n, frequency_band, 'Deep', 3, 1, deep_mean, deep_comparison, deep_difference, deep_std, deep_var, deep_entropy])
                allPD_GPI_beta.append([subject_n, frequency_band, 'REM', 4, 1, rem_mean, rem_comparison, rem_difference, rem_std, rem_var, rem_entropy])
                allPD_GPI_beta.append([subject_n, frequency_band, 'Sleep', 5, 1, sleep_mean, sleep_comparison, sleep_difference, sleep_std, sleep_var, sleep_entropy])
    
    if subject_n == 8 or subject_n == 9:
        allET_alpha.append([subject_n, frequency_band, 'Wake', 0, 0, wake_mean, 'N/A', 'N/A', wake_std, wake_var, wake_entropy])
        allET_alpha.append([subject_n, frequency_band, 'Restless', 1, 1, restless_mean, restless_comparison, restless_difference, restless_std, restless_var, restless_entropy])
        allET_alpha.append([subject_n, frequency_band, 'Light', 2, 1, light_mean, light_comparison, light_difference, light_std, light_var, light_entropy])
        allET_alpha.append([subject_n, frequency_band, 'Deep', 3, 1, deep_mean, deep_comparison, deep_difference, deep_std, deep_var, deep_entropy])
        allET_alpha.append([subject_n, frequency_band, 'REM', 4, 1, rem_mean, rem_comparison, rem_difference, rem_std, rem_var, rem_entropy])
        allET_alpha.append([subject_n, frequency_band, 'Sleep', 5, 1, sleep_mean, sleep_comparison, sleep_difference, sleep_std, sleep_var, sleep_entropy])

with open('statistics.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Subject Number', 'Frequency Band', 'Stage', 'Stage Number', 'Sleep or Wake', 'Mean', 'Wake Comparison', 'Wake Difference', 'Standard Deviation', 'Variance', 'Entropy'])
    writer.writerows(complete_list)

with open('allPD_alpha.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Subject Number', 'Frequency Band', 'Stage', 'Stage Number', 'Sleep or Wake', 'Mean', 'Wake Comparison', 'Wake Difference', 'Standard Deviation', 'Variance', 'Entropy'])
    writer.writerows(allPD_alpha)

with open('allPD_beta.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Subject Number', 'Frequency Band', 'Stage', 'Stage Number', 'Sleep or Wake', 'Mean', 'Wake Comparison', 'Wake Difference', 'Standard Deviation', 'Variance', 'Entropy'])
    writer.writerows(allPD_beta)

with open('allPD_STN_alpha.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Subject Number', 'Frequency Band', 'Stage', 'Stage Number', 'Sleep or Wake', 'Mean', 'Wake Comparison', 'Wake Difference', 'Standard Deviation', 'Variance', 'Entropy'])
    writer.writerows(allPD_STN_alpha)

with open('allPD_GPI_alpha.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Subject Number', 'Frequency Band', 'Stage', 'Stage Number', 'Sleep or Wake', 'Mean', 'Wake Comparison', 'Wake Difference', 'Standard Deviation', 'Variance', 'Entropy'])
    writer.writerows(allPD_GPI_alpha)

with open('allPD_STN_beta.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Subject Number', 'Frequency Band', 'Stage', 'Stage Number', 'Sleep or Wake', 'Mean', 'Wake Comparison', 'Wake Difference', 'Standard Deviation', 'Variance', 'Entropy'])
    writer.writerows(allPD_STN_beta)

with open('allPD_GPI_beta.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Subject Number', 'Frequency Band', 'Stage', 'Stage Number', 'Sleep or Wake', 'Mean', 'Wake Comparison', 'Wake Difference', 'Standard Deviation', 'Variance', 'Entropy'])
    writer.writerows(allPD_GPI_beta)

with open('allNonPD_alpha.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Subject Number', 'Frequency Band', 'Stage', 'Stage Number', 'Sleep or Wake', 'Mean', 'Wake Comparison', 'Wake Difference', 'Standard Deviation', 'Variance', 'Entropy'])
    writer.writerows(allNonPD_alpha)

with open('allET_alpha.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Subject Number', 'Frequency Band', 'Stage', 'Stage Number', 'Sleep or Wake', 'Mean', 'Wake Comparison', 'Wake Difference', 'Standard Deviation', 'Variance', 'Entropy'])
    writer.writerows(allET_alpha)
