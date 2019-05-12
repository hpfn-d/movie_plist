import os
from unittest.mock import patch

import pytest

from movie_plist.data import check_dir


def test_url_raises(mocker):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_path_read = os.path.join(base_dir, 'tests/videos_test')
    check_dir.CFG_FILE = 'movie_plist/tests/movie_plist.cfg'
    with open(check_dir.CFG_FILE, 'w') as w_file:
        w_file.write(test_path_read)

    mocker.patch.object(
        check_dir.os.path,
        'isdir',
        return_value=False
    )
    with pytest.raises(check_dir.InvalidPath):
        check_dir.read_path()
    os.system('/bin/rm -fr ' + check_dir.CFG_FILE)


@pytest.fixture
def test_cfg_file():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_path_read = os.path.join(base_dir, 'tests/videos_test')
    check_dir.CFG_FILE = 'movie_plist/tests/movie_plist.cfg'
    with open(check_dir.CFG_FILE, 'w') as w_file:
        w_file.write(test_path_read)
    yield test_path_read, check_dir.CFG_FILE
    os.system('/bin/rm -fr ' + check_dir.CFG_FILE)


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
    check_dir.scan_dir_has_movies('/tmp/XXX')
    assert message.call_count == 1
    assert app.call_count == 1
    assert exit.call_count == 1


def test_scan_dir_has_movies():
    """
     It is called from read_path, but testing alone
     Must return True to not call PyQt stuff
    """
    assert check_dir.scan_dir_has_movies('movie_plist/tests/videos_test')
