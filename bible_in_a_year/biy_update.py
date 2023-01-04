# -------------------------------------------------------------------
# BIY table updates
# -------------------------------------------------------------------
import pytube as ptb
from pytube import YouTube

from bible_in_a_year import msg
from bible_in_a_year.biy_utils import open_yt_at_time, get_start_stop_list
from bible_in_a_year.biy_datafile import load_biy_df, save_biy_df
from bible_in_a_year.show import show_day_readings


def prompt_for_val(name, st_label: str, vid_start):
        retval = msg.prompt_int(f'Enter {st_label.upper()} time', vid_start)
        if retval != vid_start:
            msg.info(f'{name} {st_label} = {retval}')
        return retval


def get_vid_start(init_val: int, empty_val: int, st_label: str, name: str) -> int:
    if init_val > 1:
        vid_start = init_val
    else:
        vid_start = empty_val
        msg.warn(f'Missing {st_label.upper()} time for "{name}", opening url at delta : {vid_start}')
    return vid_start


def update_start_stop(url: str, name: str, label: str,
                      run_time: int, start_val: int, stop_val: int, 
                      delta: int, delta_nxt: int,
                      review: bool):
    msg.separator()
    msg.info(f'{name}')
    if label:
        msg.print(f'     "{label}"')

    # process start time
    if (start_val > 1) and (not review):
        msg.print(f'     start = {start_val}')
    else:
        vid_start = get_vid_start(init_val=start_val,
                                  empty_val=(delta + run_time),
                                  st_label='start',
                                  name=name)
        open_yt_at_time(url=url, vid_start=vid_start)
        start_val = prompt_for_val(name, 'start', vid_start)

    # process stop time
    if (stop_val > 1) and (not review):
        msg.print(f'     stop = {stop_val}')
    else:
        vid_start = get_vid_start(init_val=stop_val,
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
        notes_stop = df.notes_stop[idx]
        upload = df.upload[idx]

        msg.separator()
        msg.separator()
        msg.info(f'DAY {df.day[idx]:03d}: {url}')
        msg.print(f'     title = {title}')
        msg.print(f'     upload = {upload}')
        msg.print(f'     length = {notes_stop}')
        show_day_readings(df=df, idx=idx)

        #order_list = ['first_reading', 'second_reading', 'third_reading', 'prayer', 'notes']
        order_list = get_start_stop_list()
        start_delta_list = [75, 0, 0, 0, 0]
        end_delta_list = [300, 300, 30, 30, 60]
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
                delta = start_delta_list[ord_idx]
                delta_nxt = end_delta_list[ord_idx]
                start_upd, stop_upd = update_start_stop(url, name, label,
                                                        run_time,
                                                        start, stop, 
                                                        delta, delta_nxt,
                                                        review)
                if start != start_upd:
                    msg.info(f'update: {start_name} = {start_upd}')
                    df.at[idx, start_name] = start_upd
                    updated_row = True
                if stop != stop_upd:
                    msg.info(f'update: {stop_name} = {stop_upd}')
                    df.at[idx, stop_name] = stop_upd
                    run_time = stop_upd
                    updated_row = True
                else:
                    run_time = stop
                msg.info(f'run time = {run_time}')
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
