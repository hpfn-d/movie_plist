import os
from unittest.mock import patch

import pytest

from movie_plist.data import pimdbdata
from movie_plist.data.pimdbdata import (
    AddImdbData, ParseImdbData, RetrieveImdbData
)

expected = [

    hasattr(pimdbdata, 'BeautifulSoup'),
    hasattr(pimdbdata, 'MOVIE_SEEN'),
    hasattr(pimdbdata, 'MOVIE_UNSEEN'),
    hasattr(pimdbdata, 'MOVIE_PLIST_CACHE'),

    # ParseOmdbData methods
    hasattr(pimdbdata.ParseImdbData, 'synopsis_exists'),
    hasattr(pimdbdata.ParseImdbData, 'make_poster_name'),

    # RetrieveImdbData methods
    hasattr(pimdbdata.RetrieveImdbData, 'bs4_synopsis'),
    hasattr(pimdbdata.RetrieveImdbData, '_do_poster_png_file'),
    hasattr(pimdbdata.RetrieveImdbData, '_save_poster_file'),
    hasattr(pimdbdata.RetrieveImdbData, '_poster_url'),
    hasattr(pimdbdata.RetrieveImdbData, '_poster_file'),

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
    mocker.patch.object(pimdbdata.urllib, 'request')
    mocker.patch.object(pimdbdata, 'BeautifulSoup', return_value=None)

    return ParseImdbData('url', 'title 1999')


def test_synopsis(init_mocked):
    assert 'Maybe something is wrong' in init_mocked.synopsis


def test_poster_url(init_mocked):
    assert pimdbdata.MOVIE_PLIST_CACHE + '/skrull.jpg' == init_mocked.cache_poster


@pytest.fixture
def run_init():
    """
    new movie scanned
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, 'tests/Shawshank_Redemption-1994.html')
    title = 'Shawshank Redemption 1994'
    return ParseImdbData('file://' + html_path, title)


# def test_init_title_year(run_init):
#    assert 'Um Sonho de Liberdade (1994)' == run_init.title_year()


def test_init_synopsys(run_init):
    synopsys = 'Directed by Frank Darabont.  With Tim Robbins, Morgan Freeman, '
    synopsys += 'Bob Gunton, William Sadler. Two imprisoned men bond over a number '
    synopsys += 'of years, finding solace and eventual redemption through acts of '
    synopsys += 'common decency.'

    assert synopsys == run_init.synopsis


def test_poster_name(run_init):
    file_name = run_init.cache_poster.rpartition('/')
    assert file_name[-1] == 'Shawshank_Redemption_1994.png'


@pytest.fixture
def run_retrieve(mocker):
    mocker.patch.object(RetrieveImdbData, '_poster_file',
                        return_value=b'tests/Shawshank_Redemption_1994.png')
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, 'tests/Shawshank_Redemption-1994.html')
    title = 'Shawshank Redemption 1994'
    cache_poster = 'cache_poster'
    return RetrieveImdbData('file://' + html_path, title, cache_poster)


def test_init_poster_url(run_retrieve):
    poster_url = 'https://m.media-amazon.com/images/'
    poster_url += 'M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFm'
    poster_url += 'NTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU'
    poster_url += '@._V1_UX182_CR0,0,182,268_AL_.jpg'
    assert poster_url == run_retrieve._poster_url()


def test_choice_no_made(run_init):
    """
    json data does not have a record of the new movie
    no choice can be made
    the method works for old records
    """

    assert run_init.title not in pimdbdata.MOVIE_UNSEEN


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


# RetrieveImdbData tests
@patch('movie_plist.data.pimdbdata.RetrieveImdbData')
def test_add_synopsis_attr(add, mocker):
    """
    When synopsis does not exists call RetrieveImdbData
    """
    mocker.patch.object(ParseImdbData, 'synopsis_exists', return_value=False)
    ParseImdbData('url', 'title')
    assert add.call_count == 1


@patch('movie_plist.data.pimdbdata.RetrieveImdbData.bs4_synopsis')
def test_description_content(bs4_synopsis, mocker):
    """
    What happens when synopsis does not exists
    """
    mocker.patch.object(pimdbdata, 'BeautifulSoup', return_value=str())
    mocker.patch.object(ParseImdbData, 'synopsis_exists', return_value=False)
    ParseImdbData('url', 'title')
    assert bs4_synopsis.call_count == 1


@patch('movie_plist.data.pimdbdata.RetrieveImdbData._save_poster_file')
def test_do_save_poster_call(save_file, run_retrieve, mocker):
    """
    There is no poster yet. Create one and save it
    What is done when _save_poster_file is called
    """
    mocker.patch.object(os.path, 'isfile', return_value=False)
    run_retrieve._do_poster_png_file()
    assert save_file.call_count == 1


@patch('movie_plist.data.pimdbdata.QImage')
def test_do_save_poster_steps(img_mock, run_retrieve):
    """
    There is no poster yet. Create one and save it
    What is done when _save_poster_file is called
    """
    run_retrieve._save_poster_file()
    assert img_mock.call_count == 1
    img_mock.assert_has_calls(img_mock.loadFromData)
    img_mock.assert_has_calls(img_mock.save)


@patch('movie_plist.data.pimdbdata.RetrieveImdbData._save_poster_file')
def test_do_not_save_poster_steps(save_file, run_retrieve, mocker):
    """
    A poster exists. Do nothing.
    """
    mocker.patch.object(os.path, 'isfile', return_value=True)
    run_retrieve._do_poster_png_file()
    assert save_file.call_count == 0
