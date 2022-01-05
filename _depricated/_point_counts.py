# ============================================================================
# == Import Global Libraries == #
import os
import pandas as pd
import sys

from datetime import datetime as dt

# == Locate Root Dir == #
flare = '\\flare.py'
path = os.getcwd()
while not os.path.isfile(path + flare):
    path = os.path.dirname(path)
sys.path.append(path)

# == Import Local Functions == #
from _depricated.dataframe import get_columns, load_csv, \
    load_json
from source.modules.data_processing.prompts import yes_no
from source.modules.data_processing.math import number_in_range


# ============================================================================
# == Create Class DataPointCounts == #
class PointCountData():
    
    # class attributes
    COLUMN_NAMES = ['observer_id', 'year', 'month', 'day', 'site_id', 
        'start_time', 'point', 'minute', 'species_code', 'distance', 
        'how', 'visual', 'sex', 'migrating', 'cluster_size', 
        'cluster_code', 'notes']
    OBSERVERS = ['CKD']
    SITES = ['CC', 'CT', 'RW', 'JW', 'DQ']
    HOW = ['V', 'S', 'C', 'O']
    BOOL = ['X']
    SEX = ['M', 'F', 'J']
    SPECIES_CODE_PATH = './data/cleaned/species_codes.json'
    SPECIES_CODES = list(pd.DataFrame \
            .from_dict(load_json(SPECIES_CODE_PATH), orient='index') \
            .reset_index()['index'].unique())
    CAT_CONSTANTS = [OBSERVERS, SITES, SPECIES_CODES, HOW, BOOL, SEX, BOOL]
    CAT_COLS = ['observer_id', 'site_id', 'species_code', 'how', 'visual', 
        'sex', 'migrating']
    POINTS_RANGE = {'min': 1, 'max': 88}
    MINUTES_RANGE = {'min': 1, 'max': 6}
    DISTANCE_RANGE = {'min': 0, 'max': 1000}
    CLUSTER_SIZE = {'min': 1, 'max': 1000}
    NUM_CONSTANTS = [POINTS_RANGE, MINUTES_RANGE, DISTANCE_RANGE, 
        CLUSTER_SIZE]
    NUM_COLS = ['point', 'minute', 'distance', 'cluster_size']
    REQUIRED_COLS = ['year', 'month', 'day', 'site_id', 'point', 
        'species_code']


    # initialization method
    def __init__(self, path):
        print("--- == REVIEW INITIATED == ---\n")
        self.path = path
        self.df = load_csv(self.path, column_names=self.COLUMN_NAMES)
        self.columns = get_columns(self.df)
    
    
    # instance method
    def manual_fill_na(self):
        self.df['cluster_size'] = self.df['cluster_size'].fillna(1, axis=0)
        self.df['start_time'] = self.df['start_time'].fillna('00:00', axis=0)
    
    
    # instance method
    def drop_incomplete_rows(self):
        null_records = self.df[self.df[self.REQUIRED_COLS] \
            .isnull() \
            .any(axis='columns')]
        if len(null_records) > 0:
            print(f"A NULL value was found in a required column for each of "
                f"the following records:\n\n{null_records}\n")
            if yes_no("Remove records?"):
                self.df = self.df.dropna(subset=self.REQUIRED_COLS)
                print("(records removed)")
            else:
                print("Cannot proceed with NULL values in required columns.\n"
                    "\n--- == REVIEW TERMINATED == ---")
                exit()
            
    
    # TASK METHOD []
    def treat_null_values(self):
        print("Treating null values...")
        self.manual_fill_na()
        self.drop_incomplete_rows()
        print("Treating null values complete!")
    
    
    @staticmethod
    def validation_response(df, column):
        if len(df) > 0:
            print(df[column])
            print(f"Records in column '{column}' are not valid.")
            exit()


    # instance method
    def validate_categories(self, columns=CAT_COLS, constants=CAT_CONSTANTS):
        for i in range(len(constants)):
            df = self.df[~self.df[columns[i]].isin(constants[i])]
            df = df.dropna(subset=[columns[i]])
            self.validation_response(df, columns[i])


    # instance method
    def validate_numbers(self, columns=NUM_COLS, constants=NUM_CONSTANTS):
        for i in range(len(constants)):
            min = constants[i]['min']
            max = constants[i]['max']
            df = self.df[self.df[columns[i]] \
                .apply(lambda x: not number_in_range(x, min, max))]
            df = df.dropna(subset=[columns[i]])
            self.validation_response(df, columns[i])

    
    # TASK METHOD []
    def validate_records(self):
        print("\nValidating records...")
        self.validate_categories()
        self.validate_numbers()
        print("Validating records complete!")
    
    
    # instance method
    def merge_date(self):
        self.df['date'] = pd.to_datetime(self.df[['year', 'month', 'day']])
    
    
    # instance method
    def time_to_int(self):
        date_obj = dt(1900, 1, 1)
        self.df['seconds'] = self.df['start_time'] \
            .apply(lambda x: (dt.strptime(x, "%H:%M") - date_obj) \
                .total_seconds())
    
    
    # TASK METHOD []
    def convert_values(self):
        print("\nConverting values...")
        self.merge_date()
        self.time_to_int()
        print("Converting values complete!")
        print("\n--- == REVIEW COMPLETE == ---\n")


# ============================================================================
# == Test Module == #
path1 = r'./data/raw/test_df.csv'
test1 = PointCountData(path1)
test1.treat_null_values()
test1.validate_records()
test1.convert_values()
print(test1.df.sample(20))


# visual to bool
# replace codes with full names