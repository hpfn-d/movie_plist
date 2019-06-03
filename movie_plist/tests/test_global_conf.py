import os

import pytest

from movie_plist.conf import global_conf

params = [
    hasattr(global_conf, 'HOME_USER'),
    hasattr(global_conf, 'MOVIE_PLIST_STUFF'),
    hasattr(global_conf, 'MOVIE_PLIST_CACHE'),
    hasattr(global_conf, 'CFG_FILE'),
    hasattr(global_conf, 'SEEN_JSON_FILE'),
    hasattr(global_conf, 'UNSEEN_JSON_FILE'),
    hasattr(global_conf, 'check_movie_plist_dirs'),
    hasattr(global_conf, 'load_from_json'),
    hasattr(global_conf, 'dump_json_movie'),
    hasattr(global_conf, 'MOVIE_UNSEEN'),
    hasattr(global_conf, 'MOVIE_SEEN'),
]


@pytest.mark.parametrize('a', params)
def test_attrs(a):
    assert a


@pytest.fixture()
def mock_attrs():
    # SetUp
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    global_conf.HOME_USER = os.path.join(base_dir, 'home')

    global_conf.MOVIE_PLIST_STUFF = os.path.join(global_conf.HOME_USER, '.config/movie_plist')
    global_conf.MOVIE_PLIST_CACHE = os.path.join(global_conf.HOME_USER, '.cache/movie_plist')
    global_conf.CFG_FILE = os.path.join(global_conf.MOVIE_PLIST_STUFF, 'movie_plist.cfg')

    global_conf.SEEN_JSON_FILE = os.path.join(global_conf.MOVIE_PLIST_STUFF, 'seen_movies.json')
    global_conf.UNSEEN_JSON_FILE = os.path.join(global_conf.MOVIE_PLIST_STUFF, 'unseen_movies.json')

    global_conf.check_movie_plist_dirs()

    with open(global_conf.CFG_FILE, 'w') as w_file:
        w_file.write('movie_plist/tests/')

    for json_file in [global_conf.SEEN_JSON_FILE, global_conf.UNSEEN_JSON_FILE]:
        if not os.path.isfile(json_file):
            with open(json_file, 'w') as j_file:
                j_file.write('{}')

    yield global_conf
    # TearDown
    os.system('/bin/rm -fr ' + global_conf.HOME_USER)


def test_movie_plist_conf_files(mock_attrs):
    assert os.path.isdir(global_conf.MOVIE_PLIST_CACHE)
    assert os.path.isdir(global_conf.MOVIE_PLIST_STUFF)
    assert os.path.isfile(global_conf.SEEN_JSON_FILE)
    assert os.path.isfile(global_conf.UNSEEN_JSON_FILE)


def test_movies_attrs():
    assert isinstance(global_conf.MOVIE_SEEN, dict)
    assert isinstance(global_conf.MOVIE_UNSEEN, dict)


def test_cache_dir(mock_attrs):
    assert 'home/.cache/movie_plist' in global_conf.MOVIE_PLIST_CACHE


def test_config_dir(mock_attrs):
    assert 'home/.config/movie_plist' in global_conf.MOVIE_PLIST_STUFF


def test_invalid_path(mock_attrs, mocker):
    mocker.patch.object(global_conf.os.path, 'isdir', return_value=False)

    with pytest.raises(global_conf.InvalidPath):
        global_conf.read_path()


def test_write_path(mock_attrs):
    """
    call write_path to create movie_plist.cfg file
    """
    test_path = 'movie_plist/tests'
    cfg_file = mock_attrs.CFG_FILE
    assert os.path.isdir(test_path)
    r_path = global_conf.write_path(test_path)
    assert r_path == test_path
    assert os.path.isfile(cfg_file)

# def test_read_path(mock_attrs):
#    test_path_read = global_conf.read_path()
#
#    # assert 'videos_test' in test_path_read
#    assert global_conf.read_path() in test_path_read
