import os
from unittest.mock import patch

import pytest

from movie_plist.data import fetch_data
from movie_plist.data.fetch_data import FetchImdbData
from movie_plist.data.pimdbdata import ParseImdbData

expected = [

    hasattr(fetch_data, 'BeautifulSoup'),
    hasattr(fetch_data, 'MOVIE_SEEN'),
    hasattr(fetch_data, 'MOVIE_UNSEEN'),
    hasattr(fetch_data, 'MOVIE_PLIST_CACHE'),
    hasattr(fetch_data, 'add_synopsis'),
    hasattr(fetch_data, 'dict_movie_choice'),

    # FetchImdbData methods
    hasattr(fetch_data.FetchImdbData, 'fetch'),
    hasattr(fetch_data.FetchImdbData, '_do_poster_png_file'),
    hasattr(fetch_data.FetchImdbData, '_poster_url'),
    hasattr(fetch_data.FetchImdbData, '_poster_file'),
]


@pytest.mark.parametrize('e', expected)
def test_init_mocked_attrs(e):
    assert e


# FetchImdbData tests
@pytest.fixture
def run_fetch(mocker):
    mocker.patch.object(FetchImdbData, '_poster_file',
                        return_value=b'tests/Shawshank_Redemption_1994.png')
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, 'tests/Shawshank_Redemption-1994.html')
    title = 'Shawshank Redemption 1994'
    cache_poster = 'cache_poster'
    return FetchImdbData('file://' + html_path, title, cache_poster)


def test_init_poster_url(run_fetch):
    poster_url = 'https://m.media-amazon.com/images/'
    poster_url += 'M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFm'
    poster_url += 'NTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU'
    poster_url += '@._V1_UX182_CR0,0,182,268_AL_.jpg'
    assert poster_url == run_fetch._poster_url()


@patch('movie_plist.data.pimdbdata.FetchImdbData')
def test_add_synopsis_attr(add, mocker):
    """
    When synopsis does not exists call FetchImdbData
    It is a kind of integration test
    """
    mocker.patch.object(ParseImdbData, 'synopsis_exists', return_value=False)
    ParseImdbData('url', 'title')
    assert add.call_count == 1


@patch('movie_plist.data.fetch_data.BeautifulSoup')
def test_description_content(poster_png, mocker):
    """
    What happens when synopsis does not exists
    It is a kind of integration test
    """
    mocker.patch.object(fetch_data, 'QImage')
    mocker.patch.object(FetchImdbData, '_poster_url')
    mocker.patch.object(FetchImdbData, '_poster_file')
    mocker.patch.object(ParseImdbData, 'synopsis_exists', return_value=False)
    ParseImdbData('url', 'title')
    assert poster_png.call_count == 1


@patch('movie_plist.data.fetch_data.QImage')
def test_no_poster_steps(save_img, run_fetch, mocker):
    """
    A poster exists. Do nothing.
    """
    mocker.patch.object(os.path, 'isfile', return_value=True)
    run_fetch._do_poster_png_file()
    assert save_img.call_count == 0


@patch('movie_plist.data.fetch_data.QImage')
def test_do_poster_steps(save_img, run_fetch, mocker):
    """
    There is no poster yet. Create one and save it
    """
    mocker.patch.object(os.path, 'isfile', return_value=False)
    run_fetch._do_poster_png_file()
    assert save_img.call_count == 1
