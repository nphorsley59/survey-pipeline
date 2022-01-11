

# IN: raw point count data, OUT: cleaned point count data


import os
import pandas as pd
import pandera as pa
from config import Config
from app.utils import yes_no_input


# from _depricated.dataframe import get_columns, load_csv, \
#     load_json
# from source.modules.data_processing.prompts import yes_no
# from source.modules.data_processing.math import number_in_range


point_counts_schema = pa.DataFrameSchema({
    'observer_id': pa.Column(str, pa.Check.isin(Config.OBSERVERS)),
    'year': pa.Column(int, pa.Check.in_range(2019, 2022)),
    'month': pa.Column(int, pa.Check.in_range(1, 12)),
    'day': pa.Column(int, pa.Check.in_range(1, 31)),
    'site_id': pa.Column(str, pa.Check.isin(Config.SITES)),
    'start_time': pa.Column(str),
    'point': pa.Column(int, pa.Check.in_range(Config.POINTS_RANGE['min'], Config.POINTS_RANGE['max'])),
    'minute': pa.Column(int, pa.Check.in_range(Config.MINUTES_RANGE['min'], Config.MINUTES_RANGE['max'])),
    'distance': pa.Column(int, pa.Check.in_range(Config.DISTANCE_RANGE['min'], Config.DISTANCE_RANGE['max'])),
    'how': pa.Column(str, pa.Check.isin(Config.HOW)),
    'visual': pa.Column(bool),
    'sex': pa.Column(str, pa.Check.isin(Config.SEX)),
    'migrating': pa.Column(bool),
    'cluster_size': pa.Column(int, pa.Check.in_range(Config.CLUSTER_SIZE['min'], Config.CLUSTER_SIZE['max'])),
    'cluster_code': pa.Column(str),
    'notes': pa.Column(str)
})


class PointCounts:
    """Docstring"""
    # SPECIES_CODE_PATH = './data/cleaned/species_codes.json'
    # SPECIES_CODES = list(pd.DataFrame \
    #         .from_dict(load_json(SPECIES_CODE_PATH), orient='index') \
    #         .reset_index()['index'].unique())
    # CAT_CONSTANTS = [OBSERVERS, SITES, SPECIES_CODES, HOW, BOOL, SEX, BOOL]
    # NUM_CONSTANTS = [POINTS_RANGE, MINUTES_RANGE, DISTANCE_RANGE,
    #                  CLUSTER_SIZE]
    def __init__(self, path):
        """Docstring"""
        self.path = path
        print(f'File: {self.path}\n')
        self.df = pd.read_csv(path)
        self.columns = list(self.df.columns)
        print('LOG:')

    def fill_nulls(self, fill: dict = None):
        """Docstring"""
        for column, value in fill.items():
            self.df[column] = self.df[column].fillna(value, axis=0)
            print(f'Auto-filled nulls in column "{column}" with "{value}".')

    def drop_incomplete_rows(self, required_columns: list[str] = None):
        """Docstring"""
        null_records = self.df[self.df[required_columns].isnull().any(axis='columns')]
        null_records_count = len(null_records)
        if null_records_count > 0:
            print(f'>> WARNING: null values found in required columns for {null_records_count} records.')
            if yes_no_input('Drop records and continue?'):
                self.df = self.df.dropna(subset=required_columns)
                print(f'({null_records_count} records removed)')
            else:
                print('Cannot proceed with NULL values in required columns.')
                exit()

    def clean(self):
        print(f'Cleaning {self.path} ...')
        self.fill_nulls(fill={'cluster_size': 1, 'start_time': '00:00'})
        self.drop_incomplete_rows(required_columns=Config.REQUIRED_COLS)
        return self.df


def factory():
    path = os.path.join(Config.PROJECT_DIR, r'data\raw\test_df.csv')
    pc = PointCounts(path).clean()
    print(pc.head(5))


if __name__ == '__main__':
    factory()

#     # instance method
#     def manual_fill_na(self):
#         self.df['cluster_size'] = self.df['cluster_size'].fillna(1, axis=0)
#         self.df['start_time'] = self.df['start_time'].fillna('00:00', axis=0)
#
#
#     # instance method
#     def drop_incomplete_rows(self):
#         null_records = self.df[self.df[self.REQUIRED_COLS] \
#             .isnull() \
#             .any(axis='columns')]
#         if len(null_records) > 0:
#             print(f"A NULL value was found in a required column for each of "
#                 f"the following records:\n\n{null_records}\n")
#             if yes_no("Remove records?"):
#                 self.df = self.df.dropna(subset=self.REQUIRED_COLS)
#                 print("(records removed)")
#             else:
#                 print("Cannot proceed with NULL values in required columns.\n"
#                     "\n--- == REVIEW TERMINATED == ---")
#                 exit()
#
#
#     # TASK METHOD []
#     def treat_null_values(self):
#         print("Treating null values...")
#         self.manual_fill_na()
#         self.drop_incomplete_rows()
#         print("Treating null values complete!")
#
#
#     @staticmethod
#     def validation_response(df, column):
#         if len(df) > 0:
#             print(df[column])
#             print(f"Records in column '{column}' are not valid.")
#             exit()
#
#
#     # instance method
#     def validate_categories(self, columns=CAT_COLS, constants=CAT_CONSTANTS):
#         for i in range(len(constants)):
#             df = self.df[~self.df[columns[i]].isin(constants[i])]
#             df = df.dropna(subset=[columns[i]])
#             self.validation_response(df, columns[i])
#
#
#     # instance method
#     def validate_numbers(self, columns=NUM_COLS, constants=NUM_CONSTANTS):
#         for i in range(len(constants)):
#             min = constants[i]['min']
#             max = constants[i]['max']
#             df = self.df[self.df[columns[i]] \
#                 .apply(lambda x: not number_in_range(x, min, max))]
#             df = df.dropna(subset=[columns[i]])
#             self.validation_response(df, columns[i])
#
#
#     # TASK METHOD []
#     def validate_records(self):
#         print("\nValidating records...")
#         self.validate_categories()
#         self.validate_numbers()
#         print("Validating records complete!")
#
#
#     # instance method
#     def merge_date(self):
#         self.df['date'] = pd.to_datetime(self.df[['year', 'month', 'day']])
#
#
#     # instance method
#     def time_to_int(self):
#         date_obj = dt(1900, 1, 1)
#         self.df['seconds'] = self.df['start_time'] \
#             .apply(lambda x: (dt.strptime(x, "%H:%M") - date_obj) \
#                 .total_seconds())
#
#
#     # TASK METHOD []
#     def convert_values(self):
#         print("\nConverting values...")
#         self.merge_date()
#         self.time_to_int()
#         print("Converting values complete!")
#         print("\n--- == REVIEW COMPLETE == ---\n")
#
#
# # ============================================================================
# # == Test Module == #
# path1 = r'./data/raw/test_df.csv'
# test1 = PointCounts(path1)
# test1.treat_null_values()
# test1.validate_records()
# test1.convert_values()
# print(test1.df.sample(20))
#
#
# # visual to bool
# # replace codes with full names