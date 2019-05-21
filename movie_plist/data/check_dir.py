import glob
import os
import sys
from pathlib import Path
from typing import List, NoReturn, Optional, Union

from movie_plist.conf.global_conf import CFG_FILE, MOVIE_PLIST_STAT

# Number of movies - last ten added
COUNT = -10


class InvalidPath(Exception):
    pass


def read_path() -> str:
    content = Path(CFG_FILE)
    cfg_file_path = content.read_text()

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
    else:
        get_dir_scan = input(" Do the scan in which directory ? ")
        path_dir_scan = write_path(get_dir_scan)

    do_scan = nothing_new(path_dir_scan) or has_desktop_file(path_dir_scan)

    if do_scan:
        return do_scan

    abort_movie_plist(path_dir_scan)


def nothing_new(scan_dir: str) -> Optional[str]:
    """
    Checking the scan dir only. Not the movie dir
    A change in movie dir will not be noted
    """
    current_file = Path(MOVIE_PLIST_STAT)
    if current_file.is_file():
        last_stat = current_file.read_text()
        current_stat = Path(scan_dir).stat().st_mtime
        if last_stat == str(current_stat):
            return 'nothingnew'

    return None


def has_desktop_file(scan_dir: str) -> Union[List[str], None]:
    for _, _, filename in os.walk(scan_dir):
        for file in filename:
            if file.endswith('.desktop'):
                last_ones = sorted(
                    glob.glob(os.path.join(scan_dir, '*/*.desktop')),
                    key=os.path.getmtime
                )
                return last_ones[COUNT:]

    return None


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
