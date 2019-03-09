import os
from unittest.mock import patch

import pytest

from movie_plist.data import pimdbdata
from movie_plist.data.pimdbdata import (
    AddImdbData, FetchImdbData, ParseImdbData
)

expected = [

    hasattr(pimdbdata, 'BeautifulSoup'),
    hasattr(pimdbdata, 'MOVIE_SEEN'),
    hasattr(pimdbdata, 'MOVIE_UNSEEN'),
    hasattr(pimdbdata, 'MOVIE_PLIST_CACHE'),

    # ParseOmdbData methods
    hasattr(pimdbdata.ParseImdbData, 'synopsis_exists'),
    hasattr(pimdbdata.ParseImdbData, 'make_poster_name'),

    # FetchImdbData methods
    hasattr(pimdbdata.FetchImdbData, 'fetch'),
    hasattr(pimdbdata.FetchImdbData, '_do_poster_png_file'),
    hasattr(pimdbdata.FetchImdbData, '_poster_url'),
    hasattr(pimdbdata.FetchImdbData, '_poster_file'),

]


@pytest.mark.parametrize('e', expected)
def test_init_mocked_attrs(e):
    assert e


@pytest.fixture()
def init_mocked(mocker):
    """
    For whatever reason BS$ fails
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pimdbdata.MOVIE_PLIST_CACHE = os.path.join(base_dir, 'home/.cache/movie_plist')
    mocker.patch.object(pimdbdata, 'urlopen')
    mocker.patch.object(pimdbdata, 'BeautifulSoup', return_value=None)

    return ParseImdbData('url', 'title 1999')


def test_synopsis(init_mocked):
    assert 'Maybe something is wrong' in init_mocked.synopsis


def test_poster_url(init_mocked):
    assert pimdbdata.MOVIE_PLIST_CACHE + '/skrull.jpg' == init_mocked.cache_poster


def test_synopsis_exists():
    """
    Synopsis exists. Do nothing.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pimdbdata.MOVIE_PLIST_CACHE = os.path.join(base_dir, 'tests/.cache')
    pimdbdata.MOVIE_UNSEEN = dict(
        title=('/root', 'synopsis', 'any_path')
    )

    obj = ParseImdbData('url', 'title')
    assert obj.synopsis == 'synopsis'
    assert obj.cache_poster.endswith('movie_plist/tests/.cache/title.png')


@pytest.fixture
def run_init():
    """
    new movie scanned
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, 'tests/Shawshank_Redemption-1994.html')
    title = 'Shawshank Redemption 1994'
    return ParseImdbData('file://' + html_path, title)


def test_init_synopsys(run_init):
    synopsys = 'Directed by Frank Darabont.  With Tim Robbins, Morgan Freeman, '
    synopsys += 'Bob Gunton, William Sadler. Two imprisoned men bond over a number '
    synopsys += 'of years, finding solace and eventual redemption through acts of '
    synopsys += 'common decency.'

    assert synopsys == run_init.synopsis


def test_poster_name(run_init):
    file_name = run_init.cache_poster.rpartition('/')
    assert file_name[-1] == 'Shawshank_Redemption_1994.png'


def test_choice_no_made(run_init):
    """
    json data does not have a record of the new movie
    no choice can be made
    the method works for old records
    """

    assert run_init.title not in pimdbdata.MOVIE_UNSEEN


def test_choice_unseen(run_init):
    """
    A record exists and it goes to an unseen movie dict
    """
    pimdbdata.MOVIE_UNSEEN[run_init.title] = ('root/',)
    AddImdbData(run_init.title, 'Directed')
    assert 'Directed' in pimdbdata.MOVIE_UNSEEN[run_init.title][1]
    del pimdbdata.MOVIE_UNSEEN[run_init.title]


def test_choice_seen(run_init):
    """
    A record exists and it goes to a seen movie dict
    """
    pimdbdata.MOVIE_SEEN[run_init.title] = ('root/',)
    AddImdbData(run_init.title, 'Directed')
    assert 'Directed' in pimdbdata.MOVIE_SEEN[run_init.title][1]
    del pimdbdata.MOVIE_SEEN[run_init.title]


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
    """
    mocker.patch.object(ParseImdbData, 'synopsis_exists', return_value=False)
    ParseImdbData('url', 'title')
    assert add.call_count == 1


@patch('movie_plist.data.pimdbdata.BeautifulSoup')
def test_description_content(poster_png, mocker):
    """
    What happens when synopsis does not exists
    """
    mocker.patch.object(pimdbdata, 'QImage')
    mocker.patch.object(FetchImdbData, '_poster_url')
    mocker.patch.object(FetchImdbData, '_poster_file')
    mocker.patch.object(ParseImdbData, 'synopsis_exists', return_value=False)
    ParseImdbData('url', 'title')
    assert poster_png.call_count == 1


@patch('movie_plist.data.pimdbdata.QImage')
def test_no_poster_steps(save_img, run_fetch, mocker):
    """
    A poster exists. Do nothing.
    """
    mocker.patch.object(os.path, 'isfile', return_value=True)
    run_fetch._do_poster_png_file()
    assert save_img.call_count == 0


@patch('movie_plist.data.pimdbdata.QImage')
def test_do_poster_steps(save_img, run_fetch, mocker):
    """
    There is no poster yet. Create one and save it
    """
    mocker.patch.object(os.path, 'isfile', return_value=False)
    run_fetch._do_poster_png_file()
    assert save_img.call_count == 1
