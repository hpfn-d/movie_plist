from movie_plist.conf.global_conf import MOVIE_PLIST_CACHE

from .fetch_data import MOVIE_SEEN, MOVIE_UNSEEN, FetchImdbData

# from movie_plist.data.pyscan import MOVIE_SEEN, MOVIE_UNSEEN


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
