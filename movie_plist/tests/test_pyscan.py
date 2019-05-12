import pytest

from movie_plist.data import pyscan  # noqa: E402
from movie_plist.data import check_dir

expected = [
    hasattr(pyscan, 'os'),
    hasattr(pyscan, 're'),
    hasattr(pyscan, 'time'),
    hasattr(pyscan, 'MOVIE_SEEN'),
    hasattr(pyscan, 'MOVIE_UNSEEN'),
    hasattr(pyscan, 'create_dicts'),
    hasattr(pyscan, '_new_data'),
    hasattr(pyscan, '_new_desktop_f'),
    hasattr(pyscan, '_unknow_dirs'),
    hasattr(pyscan, '_open_right_file'),
    hasattr(pyscan, 'mk_title_year'),
]


@pytest.mark.parametrize('e', expected)
def test_attrs(e):
    assert e


pyscan.MOVIE_SEEN = dict()
pyscan.MOVIE_UNSEEN = dict()


@pytest.fixture()
def test_all(mocker):
    mocker.patch.object(
        check_dir,
        'read_path',
        return_value='movie_plist/tests/videos_test/'
    )
    return pyscan.create_dicts()


def test_all_key(test_all):
    assert 'Shawshank Redemption, the 1994' in pyscan.MOVIE_UNSEEN.keys()


def test_all_url(test_all):
    url, _ = list(pyscan.MOVIE_UNSEEN.values())[0]
    assert 'https://www.imdb.com/title/tt0111161/' == url


def test_all_path_to(test_all):
    _, path_to = list(pyscan.MOVIE_UNSEEN.values())[0]

    return_path = 'movie_plist/tests/'
    return_path += 'videos_test/Shawshank Redemption, the 1994'
    assert return_path == path_to


def test_all_movie_seen_len(test_all):
    assert len(pyscan.MOVIE_SEEN) == 0
