# -*- coding: utf-8 -*-
import os
import re
from _socket import timeout
from urllib.error import URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup
from PyQt5.QtGui import QImage  # pylint: disable-msg=E0611

from movie_plist.conf.global_conf import MOVIE_PLIST_CACHE
from movie_plist.data.pyscan import MOVIE_SEEN, MOVIE_UNSEEN


class ParseImdbData:
    def __init__(self, url, title):
        """

        """
        self._url = url
        self.title = title
        self.synopsis = ''
        self.cache_poster = self.make_poster_name()
        if not self.synopsis_exists():
            retrieve_data = FetchImdbData(url, title, self.cache_poster)
            self.synopsis = retrieve_data.synopsis
            self.cache_poster = retrieve_data.cache_poster

    def make_poster_name(self):
        """

        """
        count_spaces = self.title.count(' ')
        cache_name = self.title.replace(' ', '_', count_spaces)
        return MOVIE_PLIST_CACHE + '/' + cache_name + '.png'

    def synopsis_exists(self):
        all_movies = {**MOVIE_UNSEEN, **MOVIE_SEEN}
        if self.title in all_movies and len(all_movies[self.title]) == 3:
            self.synopsis = all_movies[self.title][1]

        return self.synopsis


class FetchImdbData:
    def __init__(self, url, title, cache_poster):
        self._url = url
        self.title = title
        self.bs4_poster = ''
        self.dflt = cache_poster
        self.cache_poster = MOVIE_PLIST_CACHE + '/skrull.jpg'

        self.synopsis = """Maybe something is wrong with
        internet connection, url problem, the imdb .css file.
        A skrull and this text. Please try again."""

        self.fetch()

    def fetch(self):

        try:
            soup = BeautifulSoup(self._get_html(), 'html.parser')
            description = soup.find('meta', property="og:description")
            self.synopsis = description['content']
            self.bs4_poster = soup.find('div', class_="poster")
        except (TypeError, AttributeError) as e:
            text = """
            For some reason bs4 says that html file is empty
            or there is a problem reading the record saved in .cache dir,
            or internet problem.
            Please, try again.
            """
            print(e)
            print(text)
            print(self.title)
        else:
            self.cache_poster = self.dflt
            self._do_poster_png_file()
            AddImdbData(self.title, self.synopsis)

    def _do_poster_png_file(self):
        """

        """
        if not os.path.isfile(self.cache_poster):
            img = QImage()  # (8,10,4)
            img.loadFromData(self._poster_file())
            img.save(self.cache_poster)

    def _poster_file(self):
        try:
            url = self._poster_url()
            read_url = urlopen(url, timeout=3).read()
        except (URLError, timeout, TypeError) as e:
            print(e)
            print("Poster File method error.")
        else:
            return read_url

        # this is not the type expected by QImage.loadFromData
        return None

    def _poster_url(self):
        """

        """
        result = re.search(r'\bhttp\S+jpg\b', str(self.bs4_poster))
        return result.group(0)

    def _get_html(self):
        """

        """
        try:
            url = urlopen(self._url, timeout=3).read()
        except (URLError, timeout, ValueError) as e:
            text = "Internet or {}.desktop file problem".format(self.title)
            print(text)
            print(e)
        else:
            return url

        return None


class AddImdbData:
    def __init__(self, title, synopsis):
        self.title = title
        self.synopsis = synopsis
        self.add_synopsis()

    def add_synopsis(self):
        if self.title in MOVIE_UNSEEN:
            self.dict_movie_choice(MOVIE_UNSEEN)
        elif self.title in MOVIE_SEEN:
            self.dict_movie_choice(MOVIE_SEEN)

    def dict_movie_choice(self, d_movie):
        movie_info = list(d_movie[self.title])
        movie_info.insert(1, self.synopsis)
        d_movie[self.title] = tuple(movie_info)
