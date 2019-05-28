from unittest.mock import patch

import pytest

from movie_plist.data import data_manager, fetch_data
from movie_plist.data.data_manager import ImdbDataManager, os
from movie_plist.data.fetch_data import FetchImdbData

expected = [

    hasattr(fetch_data, 'BeautifulSoup'),
    hasattr(fetch_data, 'MOVIE_SEEN'),
    hasattr(fetch_data, 'MOVIE_UNSEEN'),
    hasattr(fetch_data, 'MOVIE_PLIST_CACHE'),
    hasattr(fetch_data, 'add_synopsis'),

    # FetchImdbData methods
    hasattr(fetch_data.FetchImdbData, 'fetch'),
    hasattr(fetch_data.FetchImdbData, '_save_poster_png_file'),
    hasattr(fetch_data.FetchImdbData, '_poster_url'),
    hasattr(fetch_data.FetchImdbData, '_poster_file'),
]


@pytest.mark.parametrize('e', expected)
def test_init_mocked_attrs(e):
    assert e


# FetchImdbData tests
@pytest.fixture
def run_fetch(mocker):
    # mocker.patch.object(FetchImdbData, '_poster_file',
    #                    return_value=b'tests/Shawshank_Redemption_1994.png')
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, 'tests/Shawshank_Redemption-1994.html')
    title = 'Shawshank Redemption 1994'
    cache_poster = 'cache_poster'
    fetch_data.MOVIE_UNSEEN[title] = ('root/',)
    return FetchImdbData('file://' + html_path, title, cache_poster)


def test_init_poster_url(run_fetch):
    poster_url = 'https://m.media-amazon.com/images/'
    poster_url += 'M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFm'
    poster_url += 'NTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU'
    poster_url += '@._V1_UX182_CR0,0,182,268_AL_.jpg'
    assert poster_url == run_fetch._poster_url()


def test_synopsys(run_fetch):
    synopsys = 'Directed by Frank Darabont.  With Tim Robbins, Morgan Freeman, '
    synopsys += 'Bob Gunton, William Sadler. Two imprisoned men bond over a number '
    synopsys += 'of years, finding solace and eventual redemption through acts of '
    synopsys += 'common decency.'

    assert synopsys == run_fetch.synopsis


@patch('movie_plist.data.data_manager.FetchImdbData')
def test_add_synopsis_attr(add, mocker):
    """
    When imdb data does not exists call FetchImdbData
    It is a kind of integration test
    """
    mocker.patch.object(data_manager.os.path, 'isfile', return_value=False)
    ImdbDataManager('url', 'title')
    assert add.call_count == 1


@patch('movie_plist.data.fetch_data.QImage')
# @patch('movie_plist.data.fetch_data.urlopen')
@patch('movie_plist.data.fetch_data.FetchImdbData._get_html')
@patch('movie_plist.data.fetch_data.BeautifulSoup')
def test_description_content(bs4, html, img):
    """
    What happens when imdb data does not exists
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, 'tests/Shawshank_Redemption-1994.html')
    FetchImdbData('file://' + html_path, 'title', 'cache_poster')

    assert bs4.call_count == 1
    assert html.call_count == 1
    # assert fetch.call_count == 1
    assert img.call_count == 0


@patch('movie_plist.data.fetch_data.QImage')
# @patch('movie_plist.data.fetch_data.urlopen')
@patch('movie_plist.data.fetch_data.FetchImdbData._get_html')
@patch('movie_plist.data.fetch_data.BeautifulSoup')
def test_url(bs4, html, img):
    """
    What happens bad url
    """
    FetchImdbData('url', 'title', 'cache_poster')
    assert bs4.call_count == 1
    assert html.call_count == 1
    # assert fetch.call_count == 1
    assert img.call_count == 0


@patch('movie_plist.data.fetch_data.QImage.save')
def test_do_poster_steps(save_img, run_fetch, mocker):
    """
    There is no poster yet. Create one and save it
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    poster_path = os.path.join(base_dir, 'tests/Shawshank_Redemption_1994.jpg')

    mocker.patch.object(FetchImdbData,
                        '_poster_url',
                        return_value='file://' + poster_path)

    run_fetch._poster_file()
    assert save_img.call_count == 1
