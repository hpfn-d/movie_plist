import os
from unittest.mock import patch

import pytest

from movie_plist.conf.global_conf import dump_json_movie, load_from_json
from movie_plist.data import check_dir


@pytest.fixture
def test_cfg_file():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_path_read = os.path.join(base_dir, 'tests/videos_test')
    check_dir.CFG_FILE = 'movie_plist/tests/movie_plist.cfg'
    check_dir.MOVIE_PLIST_STAT = 'movie_plist/tests/stat_file.json'
    last_stat = {'old_ones': 'test', 'stat': 0}

    with open(check_dir.CFG_FILE, 'w') as w_file:
        w_file.write(test_path_read)

    dump_json_movie(last_stat, check_dir.MOVIE_PLIST_STAT)

    yield test_path_read, check_dir.CFG_FILE
    os.system('/bin/rm -fr ' + check_dir.CFG_FILE)
    os.system('/bin/rm -fr ' + check_dir.MOVIE_PLIST_STAT)


def test_url_raises(test_cfg_file, mocker):
    mocker.patch.object(check_dir.os.path, 'isdir', return_value=False)

    with pytest.raises(check_dir.InvalidPath):
        check_dir.read_path()


def test_write_path(test_cfg_file):
    """
    call write_path to create movie_plist.cfg file
    """
    test_path = 'movie_plist/tests'
    assert os.path.isdir(test_path)
    r_path = check_dir.write_path(test_path)
    assert r_path == test_path
    assert os.path.isfile(check_dir.CFG_FILE)


def test_read_path(test_cfg_file):
    test_path_read, _ = test_cfg_file

    assert 'videos_test' in test_path_read
    assert check_dir.read_path() in test_path_read


def test_whole_success_process(test_cfg_file):
    test_path_read, _ = test_cfg_file
    desktop_file = check_dir.get_desktopf_path()
    test_path_read += '/Shawshank Redemption, the 1994/Shawshank Redemption, the 1994.desktop'

    assert test_path_read in desktop_file


def test_fail_write_path():
    with pytest.raises(check_dir.InvalidPath):
        check_dir.write_path('/tmp/XXX')


def test_fail_read_path():
    check_dir.CFG_FILE = 'movie_plist/tests/__init__.py'
    with pytest.raises(check_dir.InvalidPath):
        check_dir.read_path()


@patch('movie_plist.data.check_dir.sys.exit')
@patch('PyQt5.QtWidgets.QApplication')
@patch('PyQt5.QtWidgets.QMessageBox')
def test_fail_scan(message, app, exit):
    os.system('/bin/mkdir /tmp/XXX')
    check_dir.abort_movie_plist('/tmp/XXX')
    os.system('/bin/rm -fr /tmp/XXX')

    assert message.call_count == 1
    assert app.call_count == 1
    assert exit.call_count == 1


# @patch('movie_plist.data.check_dir.Path.stat')
def test_stat_nothingnew(test_cfg_file, mocker):
    """
    stat file exists, old stat is equal new stat
    """
    last_stat = dict(
        old_ones=list(),
        stat=0
    )

    class STAT:
        st_mtime = 0

    scan_dir = test_cfg_file[0]
    mocker.patch.object(check_dir.Path, 'is_file', return_value=True)
    mocker.patch.object(check_dir, 'load_from_json', return_value=last_stat)
    mocker.patch.object(check_dir.Path, 'stat', return_value=STAT())

    assert check_dir.has_stat(scan_dir) == 'nothingnew'


def test_stat_differ(test_cfg_file, mocker):
    """
    stat file exists, old stat differ new stat
    """
    last_stat = dict(
        old_ones=list(),
        stat=0
    )

    class STAT:
        st_mtime = 1

    scan_dir = test_cfg_file[0]
    mocker.patch.object(check_dir.Path, 'is_file', return_value=True)
    mocker.patch.object(check_dir, 'load_from_json', return_value=last_stat)
    mocker.patch.object(check_dir.Path, 'stat', return_value=STAT())
    # this will change to a set()
    # test more than is instance
    assert isinstance(check_dir.has_stat(scan_dir), set)


def test_no_stat_file(test_cfg_file, mocker):
    """
    stat file does not exists
    """
    scan_dir = test_cfg_file[0]
    mocker.patch.object(check_dir.Path, 'is_file', return_value=False)
    assert isinstance(check_dir.has_stat(scan_dir), set)


def test_return_dir_after_check(test_cfg_file):
    """
    All process
    Must return path to dir with movies
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    scan_dir = os.path.join(base_dir, 'tests/videos_test')
    scan_dir += '/Shawshank Redemption, the 1994/Shawshank Redemption, the 1994.desktop'
    desktop_file = check_dir.get_desktopf_path()

    assert scan_dir in desktop_file


def test_json(test_cfg_file):
    g = load_from_json(check_dir.MOVIE_PLIST_STAT)
    assert 'old_ones' in g.keys()
    assert 'stat' in g.keys()
