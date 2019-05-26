import re
import time
from pathlib import Path
from typing import Generator, Tuple

from movie_plist.conf.global_conf import (
    MOVIE_PLIST_STAT, MOVIE_SEEN, MOVIE_UNSEEN
)

from .check_dir import get_desktopf_path, read_path


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
    # for root in _new_desktop_f():
    for title_year, desktop_path, root in _unknow_dirs():
        imdb_url = _open_right_file(desktop_path)
        yield (title_year, imdb_url, root)

    return None


def _unknow_dirs() -> Generator[Tuple[str, str, str], None, None]:
    """
    If stat changes, get the new movies
    Write the new stat
    """
    path_last_movies = get_desktopf_path()

    if path_last_movies != 'nothingnew':
        _json_movies = {**MOVIE_SEEN, **MOVIE_UNSEEN}
        for movie in path_last_movies:
            root = movie.rpartition('/')[0]
            title_year = mk_title_year(root)
            if not _json_movies.get(title_year):
                yield (title_year, movie, root)

        new_stat()

    return None


def new_stat():
    _scan_dir = read_path()
    current_stat = Path(_scan_dir).stat().st_mtime
    Path(MOVIE_PLIST_STAT).write_text(str(current_stat))


def _open_right_file(file_with_url: str) -> str:
    """ receives a Path obj and read the content of the file """
    file_lines = Path(file_with_url).read_text()

    pat = r"(URL|url)=https?://.*"
    line_with_url = re.search(pat, ''.join(file_lines))

    if line_with_url:
        return line_with_url.group(0)[4:]

    raise Exception(f'Please check {file_with_url} file. Path and content')


def mk_title_year(root_path: str) -> str:
    return root_path.rpartition('/')[-1]
