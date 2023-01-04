# -------------------------------------------------------------------
# General package utils
# -------------------------------------------------------------------
from pathlib import Path

import numpy as np
import pandas as pd


def template_path() -> Path:
    return Path(__file__).parent.joinpath('templates')


def proj_path() -> Path:
    return Path(__file__).parent.parent

