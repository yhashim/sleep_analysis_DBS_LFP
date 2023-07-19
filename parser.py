from asyncio.windows_events import NULL
import json, csv

from datetime import datetime, timedelta
from logging import NullHandler

from patient import *

patients = []

def convert(t):
    if t[-2:] == 'AM' and t[:2] == '12':
        return '00' + t[2:-2] 
    elif t[-2:] == 'AM':
        if len(t) == 7:
            return t[:-2]
        else: 
            return '0' + t[:-2]
    elif t[-2:] == 'PM' and t[:2] == '12':
        return t[:-2]   
    else:
        if len(t) == 7:
            return str(int(t[:2]) + 12) + t[2:5]
        else:
            return str(int(t[:1]) + 12) + ':' + t[2:4]

def parse(fn):
    subjectFile = fn + '\\' + fn + 'subject.json'
    
    sleepFile = fn + '\\' + fn + 'sleep.csv'
    stageFile = fn + '\\' + fn + 'stages.json'

    starttimes_endtimes = []
    stage_starttimes_endtimes = []

    with open(subjectFile) as suf:
        subjectFile = json.load(suf)

    with open(sleepFile, mode ='r') as slf:
        sleepFile = csv.reader(slf)
        for i in sleepFile:
            if not i:
                pass
            elif i[0] == 'Sleep' or i[0] == 'Start Time':
                pass
            else:
                start_time = (datetime.strptime(i[0].split(' ')[0] + ' ' + convert(i[0].split(' ')[1]), '%Y-%m-%d %H:%M') + timedelta(hours=0)).timestamp()
                end_time = (datetime.strptime(i[1].split(' ')[0] + ' ' + convert(i[1].split(' ')[1]), '%Y-%m-%d %H:%M') + timedelta(hours=0)).timestamp()
                starttimes_endtimes.append([start_time, end_time])

    with open(stageFile) as stf:
        stageFile = json.load(stf)
        
    for i in stageFile:
        # exclude not main sleep
        # if (i['mainSleep'] == True):
            start_time = datetime.strptime(i['startTime'].replace('T', ' ').replace('Z', '').split('.')[0], '%Y-%m-%d %H:%M:%S').timestamp()
            end_time = datetime.strptime(i['endTime'].replace('T', ' ').replace('Z', '').split('.')[0], '%Y-%m-%d %H:%M:%S').timestamp()
            stage = Stages(start_time, end_time, i['levels']['data'], i['mainSleep'])
            stage_starttimes_endtimes.append(stage)

    for i in subjectFile:
        if i == 'PatientInformation':
            # from PatientInformation: name/surname, gender, diagnosis, implant_date
            # from LeadConfiguration: hemisphere, lead_location
            v = subjectFile[i]['Initial']
            patient = Patient(v['PatientFirstName'], v['PatientLastName'], v['PatientGender'], v['Diagnosis'], NULL)
        elif i == 'DeviceInformation':   
            v = subjectFile[i]['Initial']
            patient.implant_date = v['ImplantDate']
        elif i == 'EventSummary':
            # from EventSummary: start/end date, hemisphere
            hemisphere_1, hemisphere_2 = None, None
            left, right = None, None
            try: 
                hemisphere_1 =  subjectFile[i]['LfpAndAmplitudeSummary'][0]['Hemisphere'] 
                if ('Left' in hemisphere_1):
                    left = hemisphere_1
                elif ('Right' in hemisphere_1):
                    right = hemisphere_1
            except IndexError:
                print('No hemisphere sensing')
            try:
                hemisphere_2 =  subjectFile[i]['LfpAndAmplitudeSummary'][1]['Hemisphere']
                if ('Left' in hemisphere_2):
                    left = hemisphere_2
                elif ('Right' in hemisphere_2):
                    right = hemisphere_2
            except IndexError:
                print('No hemisphere sensing')
        elif i == 'DiagnosticData':
            # from DiagnosticData: (LFPTrendLogs: hemisphere): date/time, local_field_potential, amplitude
            if (left != None):
                v = subjectFile[i]['LFPTrendLogs'][left] # this needs to go one level deeper and iterate
                for v1 in v:
                    for v2 in range(0,len(v[v1])): 
                        date_time = datetime.strptime(v[v1][v2]['DateTime'].replace('T', ' ').replace('Z', ''), '%Y-%m-%d %H:%M:%S')
                        left_diagnostic_data = [date_time.timestamp(), v[v1][v2]['LFP'], False, date_time]
                        patient.left_diagnostic_data.append(left_diagnostic_data)
                patient.left_diagnostic_data = sorted(patient.left_diagnostic_data, key=lambda diagnostic_data: diagnostic_data[0])
            if (right != None):
                v = subjectFile[i]['LFPTrendLogs'][right] # this needs to go one level deeper and iterate
                for v1 in v:
                    for v2 in range(0,len(v[v1])):
                        date_time = datetime.strptime(v[v1][v2]['DateTime'].replace('T', ' ').replace('Z', ''), '%Y-%m-%d %H:%M:%S')
                        right_diagnostic_data = [date_time.timestamp(), v[v1][v2]['LFP'], False, date_time]
                        patient.right_diagnostic_data.append(right_diagnostic_data)
                patient.right_diagnostic_data = sorted(patient.right_diagnostic_data, key=lambda diagnostic_data: diagnostic_data[0])
            patient.starttimes_endtimes = starttimes_endtimes
            patient.stage_starttimes_endtimes = stage_starttimes_endtimes
            patient.first_name = str(int(fn))
            patient.last_name = ''
            patients.append(patient)