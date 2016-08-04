
from bs4 import BeautifulSoup
import re


class ParseImdbData:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, "lxml")

    def rate_value_and_votes(self):
        rate_value = self.soup.find(itemprop="ratingValue")
        print("rate: {}" .format(rate_value.contents[0]))
        rate_count = self.soup.find(itemprop="ratingCount")
        print("votes: {}" .format(rate_count.contents[0]))

    def director(self):
        director = self.soup.find(itemprop="director")
        re_director = re.compile("([A-Z].*[a-z])</span></a>.*")
        result = re_director.search(str(director.contents[1]))
        print("director: {}" .format(result.group(1)))

    def creator_writers(self):
        writer_cia = self.soup.find_all(itemprop="creator", itemtype="http://schema.org/Person")
        re_writer_cia = re.compile("([A-Z].*[a-z])</span></a>.*")
        print("Writers: ", end=' ')

        for i in writer_cia:
            result = re_writer_cia.search(str(i))
            print(result.group(1), end="  ")

        print()

    def actors(self):
        actors = self.soup.find_all(itemprop="actors", itemtype="http://schema.org/Person")
        re_actors = re.compile("([A-Z].*[a-z])</span></a>.*")
        print("Actors: ", end=' ')
        for i in actors:
            result = re_actors.search(str(i))
            print(result.group(1), end="  ")

        print("|  and others")

    def synopsis(self):
        description = self.soup.find(itemprop="description")
        raw_txt = description.contents[0].strip()
        # maybe split() is better than this
        count = 0
        for i in raw_txt:
            if count < 70 or i is not ' ':
                print(i, end='')
            else:
                if i is ' ':
                    print()
                    count = 0
                    continue
            count += 1

        print()

    def movie_poster(self):
        poster = self.soup.find(itemprop="image")
        re_poster = re.compile("http.*\.jpg")
        result = re_poster.search(str(poster))
        print("link to get poster: ")
        print(result.group(0))
