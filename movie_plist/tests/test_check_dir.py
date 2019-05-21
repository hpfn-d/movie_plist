import os
from unittest.mock import patch

import pytest

from movie_plist.data import check_dir


@pytest.fixture
def test_cfg_file():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_path_read = os.path.join(base_dir, 'tests/videos_test')
    check_dir.CFG_FILE = 'movie_plist/tests/movie_plist.cfg'
    check_dir.MOVIE_PLIST_STAT = 'movie_plist/tests/stat_file.txt'

    with open(check_dir.CFG_FILE, 'w') as w_file:
        w_file.write(test_path_read)
    with open(check_dir.MOVIE_PLIST_STAT, 'w') as stat_file:
        stat_file.write('last_stat')

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
    assert check_dir.read_path() == test_path_read


def test_whole_success_process(test_cfg_file):
    test_path_read, _ = test_cfg_file
    assert test_path_read == check_dir.get_dir_path()


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
    class STAT:
        st_mtime = 'last_stat'

    scan_dir = test_cfg_file[0]
    mocker.patch.object(check_dir.Path, 'is_file', return_value=True)
    mocker.patch.object(check_dir.Path, 'read_text', return_value='last_stat')
    mocker.patch.object(check_dir.Path, 'stat', return_value=STAT())

    assert check_dir.nothing_new(scan_dir) == 'nothingnew'


def test_stat_differ(test_cfg_file, mocker):
    class STAT:
        st_mtime = 'last'

    scan_dir = test_cfg_file[0]
    mocker.patch.object(check_dir.Path, 'is_file', return_value=True)
    mocker.patch.object(check_dir.Path, 'read_text', return_value='last_stat')
    mocker.patch.object(check_dir.Path, 'stat', return_value=STAT())
    assert check_dir.nothing_new(scan_dir) is None


def test_no_stat_file(test_cfg_file, mocker):
    scan_dir = test_cfg_file[0]
    mocker.patch.object(check_dir.Path, 'is_file', return_value=False)
    assert check_dir.nothing_new(scan_dir) is None


def test_return_dir_after_check(test_cfg_file):
    """
    All process
    Must return path to dir with movies
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    scan_dir = os.path.join(base_dir, 'tests/videos_test')

    assert check_dir.get_dir_path() == scan_dir
