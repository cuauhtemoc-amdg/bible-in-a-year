# -------------------------------------------------------------------
# BIY table updates
# -------------------------------------------------------------------
import pytube as ptb
import math
import pandas as pd
from pytube import YouTube
from prettytable import PrettyTable, FRAME, HEADER, ALL, NONE

from bible_in_a_year import msg
from bible_in_a_year.biy_utils import open_yt_at_time, get_start_stop_list
from bible_in_a_year.biy_datafile import load_biy_df, save_biy_df
from bible_in_a_year.show import show_day_readings

import datetime


def vid_time_convert(time_val:int):
    tv_int = int(time_val)
    dt_val_str = str(datetime.timedelta(seconds=tv_int))
    return f'{dt_val_str} ({time_val})'


def prompt_for_val(name, st_label: str, vid_start):
        msg.print(f'     est {st_label} = {vid_time_convert(vid_start)}')
        retval = msg.prompt_int(f'Enter {st_label.upper()} time', vid_start)
        if retval != vid_start:
            msg.info(f'{name} {st_label} = {retval}')
        return retval


def get_vid_start(run_time: int, init_val: int, empty_val: int, st_label: str, name: str) -> int:
    if init_val > 1:
        vid_start = init_val
    else:
        vid_start = empty_val
        msg.warn(f'Missing {st_label.upper()} time for "{name}"')
        msg.print(f'   Run Time = {vid_time_convert(run_time)}')
        msg.print(f'   Opening url at time = {vid_time_convert(vid_start)}')
    return vid_start


def stop_stats(row_lbl:str, stat1, stat2, start_val, rec_tot_time) -> list:
    if 'std' not in row_lbl.lower():
        eor_vid_pos = rec_tot_time - stat2
        eor_dur = eor_vid_pos - start_val
        return [row_lbl,
                stat1, vid_time_convert(stat1 + start_val),
                eor_dur, vid_time_convert(eor_vid_pos)]
    else:
        return [row_lbl,
                stat1, 'N/A',
                stat2, 'N/A']


def update_start_stop(df_timed: pd.DataFrame,
                      url: str, name: str, label: str,
                      run_time: int, start_val: int, stop_val: int,
                      delta: int, delta_nxt: int,
                      review: bool, rec_tot_time: int):
    msg.separator()
    msg.info(f'{name}')
    if label:
        msg.print(f'     "{label}"')

    # process start time
    if (start_val > 1) and (not review):
        msg.print(f'     start = {start_val}')
    else:
        vid_start = get_vid_start(run_time=run_time,
                                  init_val=start_val,
                                  empty_val=(delta + run_time),
                                  st_label='start',
                                  name=name)
        open_yt_at_time(url=url, vid_start=vid_start)
        start_val = prompt_for_val(name, 'start', vid_start)

    # process stop time
    if (stop_val > 1) and (not review):
        msg.print(f'     stop = {stop_val}')
    else:
        # stop stats
        stop_table = PrettyTable()
        stop_table.field_names = ['stat', 'reading', 'reading vid', 'to_eor', 'to_eor vid']
        stop_table.hrules = ALL
        stop_table.vrules = ALL
        stop_table.add_row(
            stop_stats('mean',
                       math.ceil(df_timed[f'{name}_duration'].mean()),
                       math.ceil(df_timed[f'{name}_to_eor'].mean()),
                       start_val, rec_tot_time))
        stop_table.add_row(
            stop_stats('50%',
                       math.ceil(df_timed[f'{name}_duration'].median()),
                       math.ceil(df_timed[f'{name}_to_eor'].median()),
                       start_val, rec_tot_time))
        stop_table.add_row(
            stop_stats('std',
                       math.ceil(df_timed[f'{name}_duration'].std()),
                       math.ceil(df_timed[f'{name}_to_eor'].std()),
                       start_val, rec_tot_time))
        print(stop_table)

        vid_start = get_vid_start(run_time=run_time,
                                  init_val=stop_val,
                                  empty_val=(delta_nxt + start_val),
                                  st_label='stop',
                                  name=name)
        open_yt_at_time(url=url, vid_start=vid_start)
        stop_val = prompt_for_val(name, 'stop', vid_start)
    
    return start_val, stop_val


def cli_update_times(start_day: int, stop_day: int, review: bool):
    df = load_biy_df()

    # filter the dates
    df_filt = df[ (df['day']>=start_day) & (df['day']<=stop_day) ]

    for idx in df_filt.index:
        url = df.day_yt_url[idx]
        title = df.title[idx]
        rec_tot_time = df.notes_stop[idx]
        upload = df.upload[idx]

        msg.separator()
        msg.separator()
        msg.info(f'DAY {df.day[idx]:03d}: {url}')
        msg.print(f'     title = {title}')
        msg.print(f'     upload = {upload}')
        msg.print(f'     length = {rec_tot_time}')
        show_day_readings(df=df, idx=idx)

        order_list = get_start_stop_list()
        start_delta_list = [69, 2, 2, 2, 1]
        end_delta_list = [392, 421, 30, 30, 60]
        fixed_list = ['prayer', 'notes']
        ord_idx = 0
        run_time = 0
        updated_row = False
        for name in order_list:
            # check for label and set has start/stop based on whether there is text in the column
            label = None
            has_start_stop = True
            if name not in fixed_list:
                label = df[name][idx]
                if isinstance(label, str):
                    if len(label.strip()) < 2:
                        has_start_stop = False
                else:
                    has_start_stop = False

            # process all with start/stop 
            if has_start_stop:
                start_name = f'{name}_start'
                stop_name = f'{name}_stop'
                start = df[start_name][idx]
                stop = df[stop_name][idx]
                df_timed = df[df[f'{name}_duration'] > 0].copy()
                df_timed[f'{name}_to_eor'] = df_timed['notes_stop'] - df_timed[f'{name}_stop']
                delta = start_delta_list[ord_idx]
                delta_nxt = end_delta_list[ord_idx]
                start_upd, stop_upd = update_start_stop(df_timed,
                                                        url, name, label,
                                                        run_time,
                                                        start, stop, 
                                                        delta, delta_nxt,
                                                        review, rec_tot_time)
                if start != start_upd:
                    msg.info(f'update: {start_name} = {vid_time_convert(start_upd)}')
                    df.at[idx, start_name] = start_upd
                    updated_row = True
                if stop != stop_upd:
                    msg.info(f'update: {stop_name} = {vid_time_convert(stop_upd)}')
                    df.at[idx, stop_name] = stop_upd
                    run_time = stop_upd
                    updated_row = True
                else:
                    run_time = stop
                msg.info(f'run time = {vid_time_convert(run_time)}')
            else:
                msg.info(f'No start/stop for {name}')
            
            ord_idx += 1
        if updated_row:
            save_biy_df(df=df)


def cli_update_titles(start_day: int, stop_day: int):
    # read xlsx file
    df = load_biy_df()

    # filter the dates
    df_filt = df[ (df['day']>=start_day) & (df['day']<=stop_day) ]

    for idx in df_filt.index:
        url = df.day_yt_url[idx]

        # get video info from pytube.YouTube object
        yt = YouTube(url)
        title = yt.title
        notes_stop = yt.length
        upload = yt.publish_date.strftime('%Y-%m-%d')

        msg.separator()
        msg.info(f'DAY {df.day[idx]:03d}: {url}')
        msg.print(f'     title = {title}')
        msg.print(f'     upload = {upload}')
        msg.print(f'     length = {notes_stop}')

        df.at[idx, 'title'] = title
        df.at[idx, 'notes_stop'] = notes_stop
        df.at[idx, 'upload'] = upload

    save_biy_df(df=df)
