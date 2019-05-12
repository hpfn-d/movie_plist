import os
import sys
from pathlib import Path

from movie_plist.conf.global_conf import CFG_FILE


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


def get_dir_path() -> str:
    if os.path.isfile(CFG_FILE):
        path_dir_scan = read_path()
    else:
        get_dir_scan = input(" Do the scan in which directory ? ")
        path_dir_scan = write_path(get_dir_scan)

    scan_dir_has_movies(path_dir_scan)

    return path_dir_scan


def scan_dir_has_movies(scan_dir: str):
    # tem que fazer uma checagem melhor
    for _, _, filename in os.walk(scan_dir):
        for file in filename:
            if file.endswith('.desktop'):
                return True

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
