# -------------------------------------------------------------------
# BIY Data File Access
# -------------------------------------------------------------------

import textwrap
import difflib
from prettytable import PrettyTable, FRAME, HEADER, ALL, NONE 

import bible_in_a_year.msg as msg
from bible_in_a_year.biy_datafile import load_biy_df
from bible_in_a_year.biy_utils import get_reading_list


def cli_days(books: list):
    df = load_biy_df()
    book_days, book_names = get_book_details(df, 1, 365)
    bk_names = []
    for nm in books:
        bk_nm = nm.capitalize()
        if bk_nm not in book_names:
            nm_list = difflib.get_close_matches(bk_nm, book_names, n=3, cutoff=0.6)
            if len(nm_list) == 0:
                msg.warn(f'No book with name "{nm}" found - skipping.')
                continue
            elif len(nm_list) == 1:
                bk_nm = nm_list[0]
            else:
                nm_list = sorted(nm_list)
                msg.warn(f'Found multiple books with similar name "{nm}".')
                opt_str = [textwrap.indent(f'[{idx}] : {nm_list[idx]}', '     ') for idx in range(len(nm_list))]
                msg.print('\n'.join(opt_str))
                sel = msg.prompt_int('Select which to use ', 0)
                bk_nm = nm_list[sel]
        bk_names.append(bk_nm)
    print_book_table(book_days, bk_names)


def cli_books(start_day: int, stop_day: int):
    df = load_biy_df()
    book_days, book_names = get_book_details(df, start_day, stop_day)
    print_book_table(book_days, book_names)


def print_book_table(book_days, book_names):
    bible_table = PrettyTable()
    bible_table.field_names = ['Book', 'Day']
    bible_table.hrules = ALL
    bible_table.vrules = ALL
    wrapper = textwrap.TextWrapper(width=40)
    for bk_nm in sorted(book_names):
        try:
            days_list = book_days[bk_nm]
            # days_str_list = [f'{x:03d}' for x in days_list]
            days_str_str = ', '.join(days_list)
            days_tw_list = wrapper.wrap(text=days_str_str)
            days_str = '\n'.join(days_tw_list)
            # msg.print(f'     {bk_nm} : days = {days_str}')
            bible_table.add_row([bk_nm, days_str])
        except KeyError:
            continue
    bible_table.sortby = 'Book'
    print(bible_table)


def get_book_details(df, start_day, stop_day):
    # filter the dates
    df_filt = df[(df['day'] >= start_day) & (df['day'] <= stop_day)]
    book_names = set()
    book_days = {}
    for idx in df_filt.index:
        day = df.day[idx]
        for col in get_reading_list():
            books_col = f'{col}_books'
            bkl = df[books_col][idx]
            # day_str will end with * if a start or stop time is missing
            bk_start = df[bkl.start_name][idx]
            bk_stop = df[bkl.stop_name][idx]
            day_str = f'{day:03d}'
            if bk_start < 1 or bk_stop < 1:
                day_str = f'{day_str}*'
            for bkl_idx in range(bkl.bk_cnt):
                book = bkl.books[bkl_idx].book
                # get book days
                if book in book_days:
                    book_list = book_days[book]
                    book_list.append(day_str)
                else:
                    book_list = [day_str]
                book_days[book] = book_list
                book_names.add(book)
    return book_days, book_names