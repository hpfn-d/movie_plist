import os

import pytest

from movie_plist.data import fetch_data, pimdbdata
from movie_plist.data.pimdbdata import ParseImdbData

expected = [

    hasattr(pimdbdata, 'MOVIE_SEEN'),
    hasattr(pimdbdata, 'MOVIE_UNSEEN'),
    hasattr(pimdbdata, 'MOVIE_PLIST_CACHE'),

    # ParseOmdbData methods
    hasattr(pimdbdata.ParseImdbData, 'synopsis_exists'),
    hasattr(pimdbdata.ParseImdbData, 'make_poster_name'),

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
    mocker.patch.object(fetch_data, 'urlopen')
    mocker.patch.object(fetch_data, 'BeautifulSoup', return_value=None)

    return ParseImdbData('url', 'title 1999')


def test_synopsis(init_mocked):
    assert 'Maybe something is wrong' in init_mocked.synopsis


def test_poster_url(init_mocked):
    assert fetch_data.MOVIE_PLIST_CACHE + '/skrull.jpg' == init_mocked.cache_poster


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


def test_choice_unseen():
    """
    A record exists in dicts and it goes to an unseen movie dict
    It is a kind of integration test
    """
    title = 'Shawshank Redemption 1994'
    fetch_data.MOVIE_UNSEEN[title] = ('root/',)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, 'tests/Shawshank_Redemption-1994.html')
    ParseImdbData('file://' + html_path, title)
    assert 'Directed by Frank Darabont' in fetch_data.MOVIE_UNSEEN[title][1]
    del fetch_data.MOVIE_UNSEEN[title]


def test_choice_seen():
    """
    A record exists in dicts and it goes to a seen movie dict
    It is a kind of integration test
    """
    title = 'Shawshank Redemption 1994'
    fetch_data.MOVIE_SEEN[title] = ('root/',)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, 'tests/Shawshank_Redemption-1994.html')
    ParseImdbData('file://' + html_path, title)
    assert 'Directed by Frank Darabont' in fetch_data.MOVIE_SEEN[title][1]
    del fetch_data.MOVIE_SEEN[title]


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
