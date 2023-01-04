# -------------------------------------------------------------------
# BIY Data File Access
# -------------------------------------------------------------------

import pandas as pd

import textwrap
from prettytable import PrettyTable, FRAME, HEADER, ALL, NONE

import bible_in_a_year.msg as msg
from bible_in_a_year.biy_datafile import load_biy_df
from bible_in_a_year.biy_utils import get_reading_list


def show_day_readings(df: pd.DataFrame, idx:int):
    bible_table = PrettyTable()
    bible_table.field_names = ['reading', 'book']
    bible_table.hrules = ALL
    bible_table.vrules = ALL
    for col in get_reading_list():
        books_col = f'{col}_books'
        bkl = df[books_col][idx]
        bkl_str = f'{bkl}'
        bible_table.add_row([col, bkl_str])
    print(bible_table)
