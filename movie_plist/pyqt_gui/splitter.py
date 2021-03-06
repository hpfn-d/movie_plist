"""
most from zetcode tutorial
"""

from subprocess import call

from PyQt5.QtCore import Qt  # pylint: disable-msg=E0611
from PyQt5.QtWidgets import (  # pylint: disable-msg=E0611
    QFileSystemModel, QHBoxLayout, QLabel, QListWidget, QSplitter, QTabWidget,
    QTreeView, QVBoxLayout, QWidget
)

from movie_plist.data.create_dict import MOVIE_SEEN, MOVIE_UNSEEN
from movie_plist.html_file.htmltags import HtmlTags
from movie_plist.pyqt_gui.right_click_menu import RightClickMenu


class TwoLines(QWidget):
    def __init__(self):
        super().__init__()
        self.top = QListWidget()
        if MOVIE_UNSEEN:
            self.current_dict = MOVIE_UNSEEN
            self.current_list = MOVIE_UNSEEN.keys()
        else:
            self.current_dict = MOVIE_SEEN
            self.current_list = MOVIE_SEEN.keys()

        self.tabs = QTabWidget()
        self.bottom = QLabel()
        self.tree = QTreeView()

        self.init_ui()

    def init_ui(self):
        hbox = QHBoxLayout(self)

        self.top.addItems(self.current_list)
        self.top.setCurrentRow(0)
        self.top.setContextMenuPolicy(Qt.CustomContextMenu)

        # TAB movie info
        self.data_to_show()
        # TAB ls dir
        self.ls_current_dir()
        # TABS
        self.set_tabs()

        # must be here because of QBasicTimer red msg
        # QBasicTimer can only be used with threads started with QThread
        def changed_item():
            if self.top.currentItem():
                self.data_to_show()
                self.ls_current_dir()

        self.top.currentItemChanged.connect(changed_item)
        self.top.customContextMenuRequested.connect(self.right_click)
        self.tree.doubleClicked.connect(self.clicked_movie)

        # to choose a browser
        # self.labelOnlineHelp.linkActivated.connect(self.link_handler)
        self.bottom.setOpenExternalLinks(True)

        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(self.top)
        splitter1.addWidget(self.tabs)

        hbox.addWidget(splitter1)
        self.setLayout(hbox)

    def set_tabs(self):
        """
        movie info on one tab
        ls dir on the other tab
        """
        # movie info
        tab_synopsys = QWidget()

        # layout
        synopsys_vbox = QVBoxLayout()

        # ls dir
        tab_ls_dir = QWidget()

        lsdir_vbox = QVBoxLayout()

        # tab one
        synopsys_vbox.addWidget(self.bottom)
        tab_synopsys.setLayout(synopsys_vbox)
        self.tabs.addTab(tab_synopsys, "Movie Info")
        # tab two
        lsdir_vbox.addWidget(self.tree)
        tab_ls_dir.setLayout(lsdir_vbox)
        self.tabs.addTab(tab_ls_dir, "ls dir")

    def data_to_show(self):
        """
        call HtmlTags to build html with a poster and a synopsis
        and put the result on self.bottom
        """
        title = self.top.currentItem().text()
        url = self.current_dict[title][0]
        context = HtmlTags(url, title)
        self.bottom.setText(context.context)

    def ls_current_dir(self):
        path_to_dir = self.current_dict[self.top.currentItem().text()][-1]
        # ls content of the current dirQt.CustomContextMenu
        lsdir = QFileSystemModel()
        lsdir.setRootPath(path_to_dir)
        self.tree.setModel(lsdir)
        self.tree.setRootIndex(lsdir.index(path_to_dir))
        self.tree.setColumnWidth(0, 450)

    def right_click(self):
        RightClickMenu(self.current_dict, self.top)

    def clicked_movie(self):
        item = self.tree.selectedIndexes()[0]
        file_to_play = item.model().filePath(item)
        if file_to_play.endswith(('.avi', 'mp4', '.mkv')):
            call(['/usr/bin/mpv', file_to_play])

    def on_changed(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()
