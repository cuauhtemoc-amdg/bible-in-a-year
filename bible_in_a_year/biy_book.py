# -------------------------------------------------------------------
# BIY Bible book and book list
# -------------------------------------------------------------------

import re
import pandas as pd
from pathlib import Path

from slugify import slugify

from bible_in_a_year.biy_utils import bible_in_year_mp3_path, bible_in_year_mp4_path


class BIYBook:
    def __init__(self, day: int, 
                 col_name: str, book, ch1, ch2) -> None:
        self.name = col_name
        self.day = day
        self.book = book
        self.ch1 = ch1
        self.ch2 = ch2

    def __str__(self) -> str:
        if self.ch2:
            return f'{self.book} {self.ch1}-{self.ch2}'
        elif self.ch1:
            return f'{self.book} {self.ch1}'
        else:
            return f'{self.book}'

    def __repr__(self) -> str:
        day_str = f'DAY[{self.day:03d}]::'
        if self.ch2:
            return f'{day_str}::{self.book} {self.ch1}-{self.ch2}'
        elif self.ch1:
            return f'{day_str}::{self.book} {self.ch1}'
        else:
            return f'{day_str}::{self.book}'
    
    def mp3_dir(self) -> Path:
        book_slug = slugify(self.book)
        ret_dir = bible_in_year_mp3_path().joinpath(book_slug)
        if not ret_dir.exists():
            ret_dir.mkdir(parents=True, exist_ok=True)
        return ret_dir

    def mp4_dir(self) -> Path:
        book_slug = slugify(self.book)
        ret_dir = bible_in_year_mp4_path().joinpath(book_slug)
        if not ret_dir.exists():
            ret_dir.mkdir(parents=True, exist_ok=True)
        return ret_dir


class BIYBookList:
    def __init__(self, book_names: str, day: int, 
                 col_name: str) -> None:
        self.name = col_name
        self.start_name = f'{self.name}_start'
        self.stop_name = f'{self.name}_stop'
        self.day = day
        self.bk_cnt = 0

        is_esther = False
        if isinstance(book_names, str):
            if book_names.lower().startswith('esther'):
                name_list = [book_names,]
                is_esther = True
            else:
                name_list = book_names.split(',')
        else:
            name_list = []
        bk_list = []
        for book_nm in name_list:
            book = None
            ch1 = None
            ch2 = None
            pattern = r'(?P<bk>([a-zA-Z]+)|(\d\s[a-zA-Z]+))(\s(?P<ch1>\d+))?(\-(?P<ch2>\d+))?'
            if is_esther:
                if ',' in book_nm:
                    pattern = r'(?P<bk>([a-zA-Z]+)|(\d\s[a-zA-Z]+))(\s(?P<ch1>\d+))?(,\s(?P<ch2>\d+))?'
            m = re.search(pattern, book_nm)
            if m:
                mdict = m.groupdict()
                if 'bk' in mdict:
                    book = mdict['bk']
                if 'ch1' in mdict:
                    ch1  = mdict['ch1']
                if 'ch2' in mdict:
                    ch2  = mdict['ch2']
            bk = BIYBook(day=day, col_name=col_name,
                         book=book, ch1=ch1, ch2=ch2)
            bk_list.append(bk)
            self.bk_cnt +=1
        self.books = bk_list
    
    def __str__(self) -> str:
        if self.bk_cnt < 1:
            return ''
        elif self.bk_cnt < 2:
            return f'{self.books[0]}'
        else: 
            return f'{self.books[0]}, {self.books[1]}'

    def __repr__(self) -> str:
        if self.bk_cnt < 1:
            return 'No Books'
        elif self.bk_cnt < 2:
            return f'{self.books[0]}'
        else: 
            return f'{self.books[0]}, {self.books[1]}'

