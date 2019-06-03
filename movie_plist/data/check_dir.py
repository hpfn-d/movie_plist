import glob
import os
import sys
from pathlib import Path
from typing import List, NoReturn, Set, Union

from movie_plist.conf.global_conf import (
    CFG_FILE, MOVIE_PLIST_STAT, dump_json_movie, load_from_json
)


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


def get_desktopf_path() -> Union[str, Set[str], List[str]]:
    """
    Get path from .cfg file or ask for it
    Check if stat changed or has (new) .desktop files
    Return the result or
    Abort app
    """
    if os.path.isfile(CFG_FILE):
        path_dir_scan = read_path()
        do_scan: Union[str, Set[str], List[str]] = has_stat(path_dir_scan)
    else:
        get_dir_scan = input(" Do the scan in which directory ? ")
        path_dir_scan = write_path(get_dir_scan)
        do_scan = glob_desktop_file(get_dir_scan)

    if do_scan:
        return do_scan

    abort_movie_plist(path_dir_scan)


def has_stat(scan_dir: str) -> Union[str, Set[str]]:
    """
    If last stat exists compare with new one. If differ
    call for new desktop files
    """
    last_scan_dir_state = load_from_json(MOVIE_PLIST_STAT)
    old_stat = last_scan_dir_state.get('stat')
    current_stat = Path(scan_dir).stat().st_mtime

    if old_stat == current_stat:
        return 'nothingnew'

    last_scan_dir_state['stat'] = current_stat
    return new_desktop_files(scan_dir, last_scan_dir_state)


def new_desktop_files(scan_dir: str, last_scan_dir_state: dict) -> Set[str]:
    """
    Build a new list of desktop files and check old list and stat
    save new data and return new values
    """
    dfile_list = glob_desktop_file(scan_dir)
    new_ones = set(dfile_list) - set(last_scan_dir_state.get('old_ones', list()))
    # refresh old_ones
    last_scan_dir_state['old_ones'] = dfile_list
    dump_json_movie(last_scan_dir_state, MOVIE_PLIST_STAT)

    return new_ones


def glob_desktop_file(scan_dir: str) -> List[str]:
    return glob.glob(os.path.join(scan_dir, '**/*.desktop'), recursive=True)


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
