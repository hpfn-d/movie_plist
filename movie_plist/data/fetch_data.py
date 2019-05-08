import re
from socket import timeout
from typing import Union
from urllib.error import URLError
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from PyQt5.QtGui import QImage  # pylint: disable-msg=E0611

from movie_plist.conf.global_conf import MOVIE_PLIST_CACHE

from .pyscan import MOVIE_SEEN, MOVIE_UNSEEN


class FetchImdbData:
    def __init__(self, url: str, title: str, cache_poster: str):
        self._url = url
        self.title = title
        self.bs4_poster = ''
        self.cache_poster = MOVIE_PLIST_CACHE + '/skrull.jpg'

        self.synopsis = """Maybe something is wrong with
        internet connection, url problem, the imdb .css file.
        A skrull and this text. Please try again."""

        self.fetch(cache_poster)

    def fetch(self, cache_poster: str) -> None:

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

    def _do_poster_png_file(self) -> None:
        """

        """
        poster_to_save = self._poster_file()
        if poster_to_save:
            img = QImage()  # (8,10,4)
            img.loadFromData(poster_to_save)
            img.save(self.cache_poster)
            add_synopsis(self.title, self.synopsis)
        else:
            print('QImage - Unexpected type for a poster. Please try again.')

    def _poster_file(self) -> Union[bytes]:
        poster_file = urlopen(self._poster_url(), timeout=3).read()

        if isinstance(poster_file, bytes):
            return poster_file

        return None

    def _poster_url(self) -> Union[str, Request]:
        find_url = re.search(r'\bhttp\S+jpg\b', str(self.bs4_poster))
        if find_url:
            return find_url.group(0)

        print(f'Did not find a url for {self.title}')
        print("Maybe the (poster) url does not exists in the .html file")

        return ''

    def _get_html(self) -> Union[bytes, str]:
        """

        """
        try:
            return urlopen(self._url, timeout=3).read()
        except (URLError, timeout, ValueError) as e:
            text = "Internet or {}.desktop file problem".format(self.title)
            print(e)
            print(text)

        return ''


# helper func
def add_synopsis(title: str, synopsis: str) -> None:
    d_movie = MOVIE_UNSEEN if MOVIE_UNSEEN.get(title) else MOVIE_SEEN

    movie_info = list(d_movie[title])
    movie_info.insert(1, synopsis)
    d_movie[title] = tuple(movie_info)
