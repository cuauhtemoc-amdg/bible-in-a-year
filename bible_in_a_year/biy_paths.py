# -------------------------------------------------------------------
# BIY Paths
# -------------------------------------------------------------------
from pathlib import Path


def proj_path() -> Path:
    return Path(__file__).parent.parent


def bible_in_year_data_path() -> Path:
    return proj_path().joinpath('data')


class BIYExportDataPath:
    def __init__(self):
        self.__exp_path = proj_path().joinpath('bible-in-a-year')

    @property
    def export_path(self) -> Path:
        return self.__exp_path

    @export_path.setter
    def export_path(self, val: Path):
        self.__exp_path = val


BIY_EXPORT_DATA = BIYExportDataPath()


def bible_in_year_path() -> Path:
    return BIY_EXPORT_DATA.export_path


def bible_in_year_temp_path() -> Path:
    return bible_in_year_path().joinpath('yt-temp')


def biy_mp4_path() -> Path:
    return bible_in_year_path().joinpath('mp4')


def biy_mp4_bible_path() -> Path:
    return biy_mp4_path().joinpath('bible')


def biy_mp3_path() -> Path:
    return bible_in_year_path().joinpath('mp3')


def biy_mp3_bible_path() -> Path:
    return biy_mp3_path().joinpath('bible')

