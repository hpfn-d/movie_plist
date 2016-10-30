#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import QApplication
from pathlib import Path
# movie_plist stuff
import html_file.create_page
from data.pyscan import PyScan
from info_in_db.movie_plist_sqlite3 import DataStorage
from pyqt_gui.main_gui import Window

def check_pushto_db(stored, url_got):
    movies_stored = stored.check_movie()
    # check if the all movie info is in movie_plist_sqlite3.db
    # if not, put it in there
    for url, path, movie_file in url_got:
        if url not in movies_stored:
            stored_data.insert_data(url, path, movie_file)

def main(d_scan):
    # scan the directory
    obtain_url = PyScan(d_scan)
    obtain_url = obtain_url.dir_to_scan()
    # check if the .html exists
    movie_file_check = d_scan + "/pymovieinfo.html"
    movie_file_check = Path(movie_file_check)
    # open connection with *sqlite3.db
    stored_data = DataStorage()

    if movie_file_check.is_file():
        html_file.create_page.generate_html(d_scan, stored_data)
    else:
        check_pushto_db(stored_data, obtain_url)
        #movies_stored = stored_data.check_movie()
        #
        ## check if the all movie info is in movie_plist_sqlite3.db
        ## if not, put it in there
        #for url, path, movie_file in obtain_url:
        #    if url not in movies_stored:
        #        stored_data.insert_data(url, path, movie_file)

        # create the page for QWebView
        html_file.create_page.generate_html(d_scan, stored_data)

    # close connection with *sqlite3.db
    stored_data.exit_from_db()

    app = QApplication(sys.argv)
    ex = Window(d_scan)
    sys.exit(app.exec_())

if __name__ == '__main__':
    if len(sys.argv) is 2:
        path_dir_scan = sys.argv[1]
    else:
        path_dir_scan = input(" Do the scan in which directory ? ")

    main(path_dir_scan)
