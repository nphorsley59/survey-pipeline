# ============================================================================
# == Import Global Libraries == #
import os
import pandas as pd
import sys

# == Locate Root Dir == #
flare = '\\flare.py'
path = os.getcwd()
while not os.path.isfile(path + flare):
    path = os.path.dirname(path)
sys.path.append(path)

# == Import Local Functions == #
from source.modules.data.dataframe import get_columns, load_csv, \
    load_json
from source.modules.data.math import number_in_range


# ============================================================================
# == Create Class DataPointCounts == #
class PointCountData():
    
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


    def __init__(self, path):
        self.path = path
        self.df = load_csv(self.path, column_names=self.COLUMN_NAMES)
        self.columns = get_columns(self.df)
    
    
    @staticmethod
    def validation_response(df, column):
        if len(df) > 0:
            print(df[column])
            print(f"Records in column '{column}' are not valid.")
            exit()


    def validate_categories(self, columns=CAT_COLS, constants=CAT_CONSTANTS):
        for i in range(len(constants)):
            df = self.df[~self.df[columns[i]].isin(constants[i])]
            df = df.dropna(subset=[columns[i]])
            self.validation_response(df, columns[i])


    def validate_numbers(self, columns=NUM_COLS, constants=NUM_CONSTANTS):
        for i in range(len(constants)):
            min = constants[i]['min']
            max = constants[i]['max']
            df = self.df[self.df[columns[i]] \
                .apply(lambda x: not number_in_range(x, min, max))]
            df = df.dropna(subset=[columns[i]])
            self.validation_response(df, columns[i])
    
    
    def review_csv(self):
        self.validate_categories()
        self.validate_numbers()
        print(f'File "{self.path}" has been reviewed.')


# ============================================================================
# == Test Module == #
path1 = r'./data/raw/point_counts_2020-06-21.csv'
test1 = PointCountData(path1)
# test1.review_csv()


# path2 = r'./data/raw/point_counts_2021-07-02.csv'
# test2 = PointCountData(path2)
# test2.validate_constants()


# find way to universally handle NULLs
# assign data types to columns where it matters