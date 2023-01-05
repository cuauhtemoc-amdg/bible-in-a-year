# -------------------------------------------------------------------
# General package utils
# -------------------------------------------------------------------
from pathlib import Path


def template_path() -> Path:
    return Path(__file__).parent.joinpath('templates')
