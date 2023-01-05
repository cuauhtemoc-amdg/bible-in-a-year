# -------------------------------------------------------------------
# BIY mp3 generate
# -------------------------------------------------------------------
from pathlib import Path
import datetime
import webbrowser
import html
import click

from jinja2 import Template
import numpy as np
import pandas as pd

from slugify import slugify
import pytube as ptb
from pytube import YouTube

from bible_in_a_year import msg
from bible_in_a_year.biy_datafile import load_biy_df, save_biy_df
from bible_in_a_year.biy_utils import open_yt_at_time, get_start_stop_list, get_reading_list, get_yt_url, biy_video_ext
from bible_in_a_year.biy_paths import biy_mp3_path, bible_in_year_temp_path
from bible_in_a_year.biy_segment import BIYSegment

from moviepy.editor import VideoFileClip
import contextlib
import os

@contextlib.contextmanager
def create_clip(yt_path:Path, clip_path: Path, start, end):
    """Changes working directory and returns to previous on exit."""
    prev_cwd = Path.cwd()
    os.chdir(clip_path.parent)
    try:
        vid_clip = VideoFileClip(yt_path.as_posix()).subclip(start, end)
        # https://towardsdatascience.com/extracting-audio-from-video-using-python-58856a940fd
        # my_clip.audio.write_audiofile(r"my_result.mp3")
        clip_aud_path = clip_path.parent.joinpath(f'{clip_path.stem}.mp3')
        aud_clip = vid_clip.audio.write_audiofile(clip_aud_path.as_posix())
        vid_clip.write_videofile(clip_path.as_posix())
        vid_clip.close()

    finally:
        os.chdir(prev_cwd)


def cli_mp3(start_day: int, stop_day: int):
    df = load_biy_df()

    # filter the dates
    df_filt = df[ (df['day']>=start_day) & (df['day']<=stop_day) ]

    for idx in df_filt.index:
        url = df.day_yt_url[idx]

        day = df.day[idx]
        title = df.title[idx]
        notes_stop = df.notes_stop[idx]
        upload = df.upload[idx]

        msg.separator()
        msg.separator()
        msg.info(f'DAY {day:03d}: {url}')
        msg.print(f'     title = {title}')
        msg.print(f'     upload = {upload}')
        msg.print(f'     length = {notes_stop}')

        # download youtube video
        url = get_yt_url(df=df, idx=idx)
        yt = YouTube(url)
        day_fn_ext = biy_video_ext()
        day_fn = f'biy-day-{day:03d}.{day_fn_ext}'
        yts = yt.streams.filter(file_extension = day_fn_ext).first()
        yts_fn = yts.download(output_path=bible_in_year_temp_path().as_posix(),
                              filename=day_fn)
        yts_path = Path(yts_fn)

        seg_list = get_reading_list()
        for seg_name in seg_list:
            biy_seg = BIYSegment(df=df, idx=idx, name=seg_name)
            if biy_seg.is_reading:
                msg.info(f'{seg_name} : {biy_seg.reading} : "{biy_seg.slug}"')
            else:
                msg.info(f'{seg_name} : "{biy_seg.slug}"')

            # create filename for segment
            wr_fn_path = biy_seg.mp3_path
            if wr_fn_path.exists():
                wr_fn_path.unlink()
            wr_fn_str = wr_fn_path.as_posix()


            # save youtube video segment
            vid_clip = VideoFileClip(yts_path.as_posix()).subclip(biy_seg.start, biy_seg.stop)
            aud_clip = vid_clip.audio.write_audiofile(wr_fn_path.as_posix())
            vid_clip.close()



