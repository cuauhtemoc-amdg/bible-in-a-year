# -------------------------------------------------------------------
# BIY Data File Access
# -------------------------------------------------------------------

from pathlib import Path

import numpy as np
import pandas as pd

from bible_in_a_year import msg
from bible_in_a_year.biy_book import BIYBookList
from bible_in_a_year.biy_utils import bible_in_year_data_path, get_reading_list, get_start_stop_list


biy_xlsx = bible_in_year_data_path().joinpath('bible-in-year-fr-mike.xlsx')
biy_xlsx_sheet='youtube'


def load_biy_df() -> pd.DataFrame:
    msg.info(f'Loading BIY data from : {biy_xlsx}')
    df = pd.read_excel(biy_xlsx, sheet_name=biy_xlsx_sheet)

    #timed_list = ['first_reading', 'second_reading', 'third_reading', 'prayer', 'notes']
    for name in get_start_stop_list():
        start_name = f'{name}_start'
        stop_name = f'{name}_stop'
        df[start_name] = df[start_name].astype('Int64')
        df[stop_name] = df[stop_name].astype('Int64')
        df[start_name] = df[start_name].fillna(0)
        df[stop_name] = df[stop_name].fillna(0)        
    
    def get_books(book_names: str, day: int, col_name: str):
        bkl = BIYBookList(book_names=book_names,
                          day=day, col_name=col_name)
        return bkl

    for col_name in get_reading_list():
        new_col_name = f'{col_name}_books'
        df[new_col_name] = df.apply(lambda x: get_books(x[col_name], x['day'], col_name),axis=1)

    return df


def save_biy_df(df: pd.DataFrame):
    msg.info(f'Saving BIY data to : {biy_xlsx}')
    df.to_excel(biy_xlsx, sheet_name=biy_xlsx_sheet, index=False)