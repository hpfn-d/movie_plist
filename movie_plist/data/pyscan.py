import os
import re
import time
from sys import exit
from typing import Generator, List, Tuple

from movie_plist.conf.global_conf import CFG_FILE, MOVIE_SEEN, MOVIE_UNSEEN


def create_dicts() -> None:
    """
    # get seen movies from json file
    # get unseen movies from on json file
    # check for new moview
    # if no unseen movies ask if continue
    # return seen and unseen movies
    """

    start = time.time()

    movie_unseen_to_add = {dir_name: (url, path) for dir_name, url, path in _new_data()}
    MOVIE_UNSEEN.update(movie_unseen_to_add)

    end = time.time()
    print(end - start)

    return None


def _new_data() -> Generator[Tuple[str, str, str], None, None]:
    """ return title_year, imdb_url and path to movie """

    for root, file_n in _new_desktop_f():
        file_with_url = os.path.join(root, file_n)
        imdb_url = _open_right_file(file_with_url)
        title_year = mk_title_year(root)

        yield (title_year, imdb_url, root)

    return None


def _new_desktop_f() -> Generator[Tuple[str, str], None, None]:
    """ search for a .desktop file in a directory """
    for root, filename in _unknow_dirs():
        for file_n in filename:
            if file_n.endswith('.desktop'):
                yield (root, file_n)

    return None


def _unknow_dirs() -> Generator[Tuple[str, List[str]], None, None]:
    """ root (path) that are not in json files """

    _scan_dir = get_dir_path()
    scan_dir_has_movies(_scan_dir)

    _json_movies = {**MOVIE_SEEN, **MOVIE_UNSEEN}

    for root, _, filename in os.walk(_scan_dir):
        title_year = _json_movies.get(mk_title_year(root), 0)
        if not title_year:
            yield (root, filename)

    return None


def _open_right_file(file_with_url: str) -> str:
    """ open the right file and get the url"""
    # IO error out of try/except
    try:
        with open(file_with_url, 'r') as check_content:
            file_lines = check_content.readlines()
    except IOError:
        raise Exception('Error while opening %s'.format(file_with_url))

    line_with_url = re.search(r"(URL|url)=https?://.*", ' '.join(file_lines))

    if line_with_url:
        return line_with_url.group(0)[4:]

    raise Exception('There is no url in %s' % file_with_url)


def mk_title_year(root_path: str) -> str:
    return root_path.rpartition('/')[-1]


class InvalidPath(Exception):
    pass


def read_path() -> str:
    with open(CFG_FILE, 'r') as movie_plist_cfg:
        cfg_path = movie_plist_cfg.readline()

    if not os.path.isdir(cfg_path):
        raise InvalidPath('Invalid path in movie_plist.cfg file.')

    return cfg_path


def write_path(cfg_path: str) -> str:
    if not os.path.isdir(cfg_path):
        raise InvalidPath('Invalid path. Please try again.')

    with open(CFG_FILE, 'w') as cfg_write:
        cfg_write.write(cfg_path)

    return cfg_path


def get_dir_path() -> str:
    if os.path.isfile(CFG_FILE):
        path_dir_scan = read_path()
    else:
        get_dir_scan = input(" Do the scan in which directory ? ")
        path_dir_scan = write_path(get_dir_scan)

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

    exit('1')
