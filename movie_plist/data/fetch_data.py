import re
from _socket import timeout
from urllib.error import URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup
from PyQt5.QtGui import QImage  # pylint: disable-msg=E0611

from movie_plist.conf.global_conf import MOVIE_PLIST_CACHE

from .pyscan import MOVIE_SEEN, MOVIE_UNSEEN


class FetchImdbData:
    def __init__(self, url, title, cache_poster):
        self._url = url
        self.title = title
        self.bs4_poster = ''
        self.cache_poster = MOVIE_PLIST_CACHE + '/skrull.jpg'

        self.synopsis = """Maybe something is wrong with
        internet connection, url problem, the imdb .css file.
        A skrull and this text. Please try again."""

        self.fetch(cache_poster)

    def fetch(self, cache_poster):

        try:
            soup = BeautifulSoup(self._get_html(), 'html.parser')
            description = soup.find('meta', property="og:description")
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
            self.synopsis = description['content']
            self.cache_poster = cache_poster
            self._do_poster_png_file()

    def _do_poster_png_file(self):
        """

        """
        try:
            img = QImage()  # (8,10,4)
            img.loadFromData(self._poster_file())
            img.save(self.cache_poster)
        except TypeError:
            print('QImage - Unexpected type str. Please try again.')
        else:
            add_synopsis(self.title, self.synopsis)

    def _poster_file(self):
        try:
            return urlopen(self._poster_url(), timeout=3).read()
        except (URLError, timeout, TypeError) as e:
            print(e)
            print("Poster File method error.")

        # this is not the type expected by QImage.loadFromData
        return ''

    def _poster_url(self):
        find_url = re.search(r'\bhttp\S+jpg\b', str(self.bs4_poster))
        return find_url.group(0)

    def _get_html(self):
        """

        """
        try:
            return urlopen(self._url, timeout=3).read()
        except (URLError, timeout, ValueError) as e:
            text = "Internet or {}.desktop file problem".format(self.title)
            print(e)
            print(text)

        return None


# helper funcs
def add_synopsis(title, synopsis):
    if title in MOVIE_UNSEEN:
        dict_movie_choice(title, MOVIE_UNSEEN, synopsis)
    elif title in MOVIE_SEEN:
        dict_movie_choice(title, MOVIE_SEEN, synopsis)


def dict_movie_choice(title, d_movie, synopsis):
    movie_info = list(d_movie[title])
    movie_info.insert(1, synopsis)
    d_movie[title] = tuple(movie_info)
