import json
import os
# user
from pathlib import Path

HOME_USER = os.environ['HOME']
# first, main path
MOVIE_PLIST_CACHE = os.path.join(HOME_USER, '.cache/movie_plist')
MOVIE_PLIST_STUFF = os.path.join(HOME_USER, '.config/movie_plist')
MOVIE_PLIST_STAT = os.path.join(MOVIE_PLIST_STUFF, 'stat_file.json')
CFG_FILE = os.path.join(MOVIE_PLIST_STUFF, 'movie_plist.cfg')
SEEN_JSON_FILE = os.path.join(MOVIE_PLIST_STUFF, 'seen_movies.json')
UNSEEN_JSON_FILE = os.path.join(MOVIE_PLIST_STUFF, 'unseen_movies.json')


def check_movie_plist_dirs():
    if not os.path.isdir(MOVIE_PLIST_CACHE):
        os.system('/bin/mkdir -p ' + MOVIE_PLIST_CACHE)

    if not os.path.isdir(MOVIE_PLIST_STUFF):
        os.system('/bin/mkdir -p ' + MOVIE_PLIST_STUFF)


def load_from_json(json_file):
    if os.path.isfile(json_file):
        with open(json_file) as json_data:
            return json.load(json_data)

    return dict()


MOVIE_SEEN = load_from_json(SEEN_JSON_FILE)
MOVIE_UNSEEN = load_from_json(UNSEEN_JSON_FILE)


def dump_json_movie(movie_dic, json_file):
    with open(json_file, 'w') as outfile:
        json.dump(movie_dic, outfile, sort_keys=True, allow_nan=False)


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
