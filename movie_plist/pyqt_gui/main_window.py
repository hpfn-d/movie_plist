"""
from zetcode tutorial
"""

from PyQt5.QtCore import QTimer  # pylint: disable-msg=E0611
from PyQt5.QtWidgets import QAction, QMainWindow  # pylint: disable-msg=E0611

from movie_plist.data.pyscan import MOVIE_SEEN, MOVIE_UNSEEN

from . import splitter


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.two_lines = splitter.TwoLines()
        self.timer = QTimer()

        self.init_ui()

    def init_ui(self):
        self.setCentralWidget(self.two_lines)

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        # exit_action.setStatusTip('Exit app')
        exit_action.triggered.connect(self.close)

        unseen_action = QAction('Unseen', self)
        # unseenAction.setShortcut()
        # unseen_action.setStatusTip('Unseen movies: ' + count_unseen)
        unseen_action.triggered.connect(self.unseenmovies)

        seen_action = QAction('Seen', self)
        # unseenAction.setShortcut()
        # seen_action.setStatusTip('Seen movies: ' + count_seen)
        seen_action.triggered.connect(self.seenmovies)

        # status bar
        self.timer.timeout.connect(self.update_statusbar)
        # check every second
        self.timer.start(1000 * 1)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exit_action)
        toolbar.addAction(unseen_action)
        toolbar.addAction(seen_action)

        self.setGeometry(100, 100, 800, 650)
        self.setWindowTitle('movie_plist')
        self.show()

    def unseenmovies(self):
        # botão 'unseen'
        self.two_lines.top.clear()
        self.two_lines.current_dict = MOVIE_UNSEEN
        self.two_lines.top.addItems(MOVIE_UNSEEN.keys())
        self.two_lines.top.setCurrentRow(0)

    def seenmovies(self):
        # botão 'seen'
        if MOVIE_SEEN:
            self.two_lines.top.clear()
            self.two_lines.current_dict = MOVIE_SEEN
            self.two_lines.top.addItems(MOVIE_SEEN.keys())
            self.two_lines.top.setCurrentRow(0)

    def update_statusbar(self):
        self.statusBar().showMessage(Window.unseen_status() + Window.seen_status())

    @staticmethod
    def unseen_status():
        u_quant = len(MOVIE_UNSEEN)
        return 'Unseen: ' + str(u_quant)

    @staticmethod
    def seen_status():
        s_quant = len(MOVIE_SEEN)
        return ' | Seen: ' + str(s_quant)
