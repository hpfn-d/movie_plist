import os

from PyQt5.QtGui import QCursor  # pylint: disable-msg=E0611
from PyQt5.QtWidgets import (  # pylint: disable-msg=E0611
    QAction, QMenu, QMessageBox
)

from movie_plist.conf.global_conf import MOVIE_PLIST_CACHE
from movie_plist.data.pyscan import MOVIE_SEEN, MOVIE_UNSEEN


class RightClickMenu:
    def __init__(self, current_dict, qt_list):
        self.current_dict = current_dict
        self.qt_list = qt_list

        self.right_click()

    def right_click(self):
        menu = QMenu()
        m_seen_action = QAction('Mark as Seen', menu)
        # unseenAction.setShortcut()
        m_seen_action.setStatusTip('Mark as Seen')
        m_seen_action.triggered.connect(self.m_seen_movies)

        m_rm_action = QAction('Remove from movie_plist', menu)
        # unseenAction.setShortcut()
        m_rm_action.setStatusTip('Remove from movie_plist')
        m_rm_action.triggered.connect(self.m_rm_from_dict)

        menu.addAction(m_seen_action)
        menu.addAction(m_rm_action)

        menu.exec_(QCursor.pos())

    def m_seen_movies(self):
        """
        mark a movie as seen.
        check unseen list and seen list
        check on db if it is already a seen movie
        """
        title_year = self.qt_list.currentItem().text()
        mark_as_seen = MOVIE_UNSEEN.get(title_year, 0)

        if mark_as_seen:
            self.qt_list.takeItem(self.qt_list.currentRow())
            MOVIE_SEEN[title_year] = mark_as_seen
            del MOVIE_UNSEEN[title_year]

    def m_rm_from_dict(self):
        """
        remove from current list and from db
        the user remove from HD
        """

        title_year = self.qt_list.currentItem().text()
        self.qt_list.takeItem(self.qt_list.currentRow())
        del self.current_dict[title_year]

        count_spaces = title_year.count(' ')
        name = title_year.replace(' ', '_', count_spaces)
        poster = MOVIE_PLIST_CACHE + '/' + name + '.png'

        if os.path.isfile(poster):
            os.system('/bin/rm -f ' + poster)

        msg = QMessageBox()
        msg.setText(title_year + " removed from movie_plist.\n\n"
                                 "Remove from HD yourself.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
