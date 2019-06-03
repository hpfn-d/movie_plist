#!/usr/bin/python3

import sys

from PyQt5.QtWidgets import QApplication

from movie_plist.conf.global_conf import (
    SEEN_JSON_FILE, UNSEEN_JSON_FILE, check_movie_plist_dirs, dump_json_movie
)
from movie_plist.data.create_dict import MOVIE_SEEN, MOVIE_UNSEEN, create_dicts
from movie_plist.pyqt_gui.main_window import Window


def main():
    create_dicts()
    app = QApplication(sys.argv)
    ex = Window()  # noqa: F841

    exit_task = [
        app.exec_(),
        dump_json_movie(MOVIE_UNSEEN, UNSEEN_JSON_FILE),
        dump_json_movie(MOVIE_SEEN, SEEN_JSON_FILE),
    ]
    sys.exit(exit_task)


if __name__ == '__main__':
    check_movie_plist_dirs()
    main()
