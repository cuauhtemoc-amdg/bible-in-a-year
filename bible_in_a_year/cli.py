# -------------------------------------------------------------------
# BIY CLI
# -------------------------------------------------------------------
from pathlib import Path
import click

import bible_in_a_year.msg as msg

from bible_in_a_year.biy_update import cli_update_titles, cli_update_times
from bible_in_a_year.biy_mp3 import cli_mp3
from bible_in_a_year.biy_utils_book import cli_books, cli_days


@click.group()
def cli():
    pass


@cli.command()
@click.option('--start', prompt='Start day', type=int)
@click.option('--stop', default=0, type=int)
@click.option('--review', is_flag=True)
def update_times(start, stop, review):

    if stop == 0 and start>0:
        stop = start
    msg.info(f'Start Day: : {start}')
    msg.info(f'Stop Day: : {stop}')
    cli_update_times(start_day=start,
                     stop_day=stop,
                     review=review)

@cli.command()
@click.option('--start', default=1, type=int)
@click.option('--stop', default=365, type=int)
def update_titles(start, stop):

    msg.info(f'Start Day: : {start}')
    msg.info(f'Stop Day: : {stop}')
    cli_update_titles(start_day=start,
                      stop_day=stop)


@cli.command()
@click.option('--start', prompt='Start day', type=int)
@click.option('--stop', prompt='Stop (end) day', type=int)
def mp3_bible(start, stop):

    msg.info(f'Start Day: : {start}')
    msg.info(f'Stop Day: : {stop}')
    cli_mp3(start_day=start,
            stop_day=stop)


@cli.command()
@click.option('--start', prompt='Start day', type=int)
@click.option('--stop', prompt='Stop (end) day', type=int)
def mp3_day(start, stop):

    msg.info(f'Start Day: : {start}')
    msg.info(f'Stop Day: : {stop}')
    cli_mp3(start_day=start,
            stop_day=stop)


@cli.command()
@click.option('--start', default=1, type=int)
@click.option('--stop', default=365, type=int)
def books(start, stop):
    msg.info(f'Start Day: : {start}')
    msg.info(f'Stop Day: : {stop}')
    cli_books(start_day=start,
              stop_day=stop)


@cli.command()
@click.argument('books', nargs=-1)
def days(books):
    msg.info(f'Books: : {books}')
    cli_days(books=books)


if __name__ == '__main__':
    cli()
