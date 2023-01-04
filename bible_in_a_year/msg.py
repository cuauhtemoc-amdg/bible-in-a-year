# -------------------------------------------------------------------
# message package
# -------------------------------------------------------------------
import click


def msg_init():
    pass


def separator():
    click.echo('-'*80)


def print(msg):
    click.echo(msg)


def info(msg):
    click.echo(f'INFO: {msg}')


def warn(msg):
    click.secho(f'WARN: {msg}', fg='yellow')


def error(msg):
    click.secho(f'ERROR: {msg}', fg='red', bold=True, err=True)


def yn_question(question):
    yn_ans=click.prompt(f'{question} [y/N]:', type=bool)
    return yn_ans

def prompt_int(msg, default = 0):
    retval=click.prompt(f'{msg} :', default=default, type=int)
    return retval
