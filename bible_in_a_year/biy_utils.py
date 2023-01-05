# -------------------------------------------------------------------
# BIY table updates
# -------------------------------------------------------------------

import pandas as pd
import webbrowser

from bible_in_a_year import msg


# -------------------------------------------------------------------
# Field Lists
# -------------------------------------------------------------------
def get_reading_list() -> list:
    order_list = ['first_reading', 'second_reading', 'third_reading']
    return order_list


def get_fixed_start_stop_list() -> list:
    fixed_list = ['prayer', 'notes']
    return fixed_list


def get_start_stop_list() -> list:
    order_list = get_reading_list() + get_fixed_start_stop_list()
    return order_list


# -------------------------------------------------------------------
# Utils
# -------------------------------------------------------------------
def get_yt_url(df: pd.DataFrame, idx: int) -> str:
    return df.day_yt_url[idx]


def biy_video_ext() -> str:
    return 'mp4'


def yt_url_at_time(url: str, vid_start=0) -> str:
    retval = f'{url}?t={vid_start:d}'
    return retval


def open_yt_at_time(url, vid_start=0):
    url_start = yt_url_at_time(url=url, vid_start=vid_start)
    msg.info(f'Opening Video: {url_start}')
    webbrowser.open_new_tab(url_start)


def has_start_stop(df, idx, name):
    retval = False
    if name in get_start_stop_list():
        retval = True

        # check for label and set retval based on whether there is text in the column
        label = None
        if name not in get_fixed_start_stop_list():
            label = df[name][idx]
            if isinstance(label, str):
                if len(label.strip()) < 2:
                    retval = False
            else:
                retval = False

    return retval

