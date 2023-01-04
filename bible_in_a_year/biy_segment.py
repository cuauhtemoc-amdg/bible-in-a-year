
import pandas as pd
from slugify import slugify

from bible_in_a_year.biy_utils import get_fixed_start_stop_list, has_start_stop, yt_url_at_time, get_yt_url
from bible_in_a_year.biy_utils import bible_in_year_mp3_path, bible_in_year_mp4_path


class BIYSegment:
    def __init__(self, df: pd.DataFrame, idx: int, name: str) -> None:
        self.name = name
        self.idx = idx
        self.reading = None
        self.start = None
        self.start_name = None
        self.stop = None
        self.stop_name = None
        self.is_reading = False
        self.slug = None
        self.start_url = None
        self.stop_url = None
        self.mp3_path = None
        self.mp4_path = None

        if has_start_stop(df=df, idx=idx, name=name):
            if name in get_fixed_start_stop_list():
                self.slug = slugify(self.name)
            else:
                self.reading = df[name][idx]
                self.is_reading = True
                self.slug = slugify(self.reading)

            # get start/stop values
            self.start_name = f'{name}_start'
            self.stop_name = f'{name}_stop'
            self.start = df[self.start_name][idx]
            self.stop = df[self.stop_name][idx]

            # setup url link
            url = get_yt_url(df=df, idx=idx)
            self.start_url = yt_url_at_time(url=url, vid_start=self.start)
            self.stop_url = yt_url_at_time(url=url, vid_start=self.stop)

            # paths
            self.name_books = f'{name}_books'
            self.bkl = df[self.name_books][idx]
            bk_0 = self.bkl.books[0]
            self.mp3_path = bk_0.mp3_dir().joinpath(f'{self.slug}.mp3')
            self.mp4_path = bk_0.mp4_dir().joinpath(f'{self.slug}.mp4')
