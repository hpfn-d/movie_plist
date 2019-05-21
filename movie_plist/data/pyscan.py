import os
import re
import time
from pathlib import Path
from typing import Generator, Tuple

from movie_plist.conf.global_conf import (
    MOVIE_PLIST_STAT, MOVIE_SEEN, MOVIE_UNSEEN
)

from .check_dir import get_dir_path


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
    """
    return title_year, imdb_url and path to movie
    Path obj is converted to str
    """
    for root in _new_desktop_f():
        imdb_url = _open_right_file(root)
        path = str(root.parent)
        title_year = mk_title_year(path)

        yield (title_year, imdb_url, path)

    return None


def _new_desktop_f() -> Generator[Path, None, None]:
    """ search for a .desktop file in a directory """
    for d in _unknow_dirs():
        teste = list(d.glob("*.desktop"))
        if teste:
            yield teste[0]

    return None


def _unknow_dirs() -> Generator[Path, None, None]:
    """ root (path) that are not in json files

    # see this later - stat info
    directory = Path(_scan_dir)
    ((f.stat().st_mtime, f) for f in directory.iterdir())
    """
    _scan_dir = get_dir_path()

    if _scan_dir == 'nothingnew':
        return None

    _json_movies = {**MOVIE_SEEN, **MOVIE_UNSEEN}

    for root, _, _ in os.walk(_scan_dir):
        title_year = mk_title_year(root)
        if not _json_movies.get(title_year):
            yield Path(root)

    current_stat = Path(_scan_dir).stat().st_mtime
    last_stat = Path(MOVIE_PLIST_STAT)
    last_stat.write_text(str(current_stat))

    # current_stat = os.stat(_scan_dir)
    # with open(current_file, 'w') as current:
    #    current.write(str(current_stat.st_mtime))

    return None


def _open_right_file(file_with_url: Path) -> str:
    """ receives a Path obj and read the content of the file """
    file_lines = file_with_url.read_text()

    pat = r"(URL|url)=https?://.*"
    line_with_url = re.search(pat, ''.join(file_lines))

    if line_with_url:
        return line_with_url.group(0)[4:]

    desktop_file = str(file_with_url.name)

    raise Exception(f'Please check {desktop_file} file. Path and content')


def mk_title_year(root_path: str) -> str:
    return root_path.rpartition('/')[-1]
