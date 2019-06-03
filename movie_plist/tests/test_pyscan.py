import os

import pytest

from movie_plist.data import create_dict  # noqa: E402

expected = [
    # hasattr(pyscan, 'os'),
    hasattr(create_dict, 're'),
    hasattr(create_dict, 'time'),
    # hasattr(pyscan, 'MOVIE_SEEN'),
    hasattr(create_dict, 'MOVIE_UNSEEN'),
    hasattr(create_dict, 'create_dicts'),
    hasattr(create_dict, '_new_data'),
    # hasattr(pyscan, '_new_desktop_f'),
    hasattr(create_dict, '_unknow_dirs'),
    hasattr(create_dict, '_open_right_file'),
    hasattr(create_dict, 'mk_title_year'),
]


@pytest.mark.parametrize('e', expected)
def test_attrs(e):
    assert e


create_dict.MOVIE_SEEN = dict()
create_dict.MOVIE_UNSEEN = dict()


@pytest.fixture()
def test_all(mocker):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # test_path_read = os.path.join(base_dir, 'tests/videos_test')
    # pyscan.MOVIE_PLIST_STAT = os.path.join(base_dir, 'tests/stat_file.json')
    create_dict.CFG_FILE = os.path.join(base_dir, 'tests/movie_plist.cfg')

    # with open(pyscan.CFG_FILE, 'w') as w_file:
    #    w_file.write(test_path_read)

    movie_dir = 'movie_plist/tests/videos_test/'
    movie_dir += 'Shawshank Redemption, the 1994/Shawshank Redemption, the 1994.desktop'

    desktop_file = [movie_dir]

    # mocker.patch.object(
    #     pyscan,
    #     'read_path',
    #     return_value=test_path_read
    # )
    #
    mocker.patch.object(
        create_dict,
        'get_desktopf_path',
        return_value=desktop_file
    )

    yield create_dict.create_dicts()
    # os.system('/bin/rm -fr ' + pyscan.MOVIE_PLIST_STAT)
    os.system('/bin/rm -fr ' + create_dict.CFG_FILE)


def test_all_key(test_all):
    assert 'Shawshank Redemption, the 1994' in create_dict.MOVIE_UNSEEN.keys()


def test_all_url(test_all):
    url, _ = list(create_dict.MOVIE_UNSEEN.values())[0]
    assert 'https://www.imdb.com/title/tt0111161/' == url


def test_all_path_to(test_all):
    _, path_to = list(create_dict.MOVIE_UNSEEN.values())[0]

    movie_dir = 'movie_plist/tests/videos_test/Shawshank Redemption, the 1994'

    assert movie_dir == path_to


def test_all_movie_seen_len(test_all):
    assert len(create_dict.MOVIE_SEEN) == 0

# def test_write_current_stat(test_all):
#    assert os.path.isfile('movie_plist/tests/stat_file.json')
