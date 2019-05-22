import glob
import os
import sys
from pathlib import Path
from typing import List, NoReturn, Union

from movie_plist.conf.global_conf import CFG_FILE, MOVIE_PLIST_STAT

# Number of movies - last ten added
COUNT = -10


class InvalidPath(Exception):
    pass


def read_path() -> str:
    cfg_file_path = Path(CFG_FILE).read_text()

    if not os.path.isdir(cfg_file_path):
        raise InvalidPath('Invalid path in movie_plist.cfg file.')

    return cfg_file_path


def write_path(cfg_file_path: str) -> str:
    if not os.path.isdir(cfg_file_path):
        raise InvalidPath('Invalid path. Please try again.')

    w_path = Path(CFG_FILE)
    w_path.write_text(cfg_file_path)

    return cfg_file_path


def get_desktopf_path() -> Union[str, List[str]]:
    """
    Get path from .cfg file or ask for it
    Check if stat changed or has (new) .desktop files
    Return the result or
    Abort app
    """
    if os.path.isfile(CFG_FILE):
        path_dir_scan = read_path()
        do_scan = has_stat(path_dir_scan)
    else:
        get_dir_scan = input(" Do the scan in which directory ? ")
        do_scan = glob_desktop_file(get_dir_scan)
        path_dir_scan = write_path(get_dir_scan)

    if do_scan:
        return do_scan

    abort_movie_plist(path_dir_scan)


def has_stat(scan_dir: str) -> Union[str, List[str]]:
    """
    Checking the scan dir only. Not the movie dir
    A change in movie dir will not be noted
    """
    stat_file = Path(MOVIE_PLIST_STAT)
    if stat_file.is_file():
        last_stat = stat_file.read_text()
        current_stat = Path(scan_dir).stat().st_mtime
        if last_stat == str(current_stat):
            return 'nothingnew'

    last_ones = glob_desktop_file(scan_dir)
    return last_ones[COUNT:]


def glob_desktop_file(scan_dir: str) -> List[str]:
    desktop_files = glob.glob(os.path.join(scan_dir, '**/*.desktop'), recursive=True)
    desktop_files.sort(key=os.path.getmtime)
    return desktop_files


def abort_movie_plist(scan_dir: str) -> NoReturn:
    from PyQt5.QtWidgets import QMessageBox, QApplication  # pylint: disable-msg=E0611

    app = QApplication(['0'])  # noqa: F841

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Empty Directory")

    text = """
        The directory scanned seems empty.
        Please check the directory
         """ + scan_dir

    msg.setText(text)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

    sys.exit('1')
