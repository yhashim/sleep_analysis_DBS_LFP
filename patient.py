from asyncio.windows_events import NULL
from contextlib import nullcontext
import imp

patients = []

class Patient:
    def __init__(self, first_name, last_name, gender, diagnosis, implant_date):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.diagnosis = diagnosis
        self.implant_date = implant_date
        
        self.left_diagnostic_data = []
        self.right_diagnostic_data = []
        self.graphs = []

        self.starttimes_endtimes = []
        self.stage_starttimes_endtimes = []

        self.analysis_rows = []

        patients.append(self)

    def __repr__(self):
        return 'first name: %s, last name: %s, gender: %s, diagnosis: %s, implant date: %s' % (self.first_name, self.last_name, self.gender, self.diagnosis, self.implant_date)

class Stages:
    def __init__(self, start_time, end_time, data, main_sleep):
        self.start_time = start_time
        self.end_time = end_time

        self.data = data

        self.main_sleep = main_sleep
    
    def __repr__(self):
        return 'start time: %s, end time: %s, main sleep: %s' % (self.start_time, self.end_time, self.main_sleep)