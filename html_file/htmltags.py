"""
   only parse_data_to_inside_table
   receive data from outside to deal
   with it and put in the .html file
"""

import urllib.request

from data import pimdbdata


class HtmlTags:
    def __init__(self, path, mode, data_to_insert=None):
        # the path is checked before calling main()
        self.file_name = path + '/pymovieinfo.html'
        if mode is 'w':
            # create a new .html file
            self.open_file = open(self.file_name, mode)
        elif mode is 'inplace':
            # insert a new movie in the .html file
            self.open_file = None
            import fileinput

            for line in fileinput.input(self.file_name, inplace=1):
                print(line, end='')
                if line.startswith('<table border'):
                    print(self.parse_data_to_inside_table(data_to_insert), end='')

    def top_header(self):
        """ from <html> tag until <table> tag """
        head = ("<html>\n<head>\n"
                "<meta http-equiv=\"Content-Type\" content=\"text/html_file; charset=utf-8\">\n"
                "<title>Py Movie Info</title>\n"
                "</head>\n<body>\n"
                "<table border=\"1\" width=\"100%\" cellpadding=\"4\" cellspacing=\"0\">\n")
        print(head, file=self.open_file)

    def inside_table(self, poster_jpg, movie_data, link, file=None):
        """
        one table cell (tr) at a time:
            poster_jpg: jpg file
            movie_data: list() with title titleYear, rate/votes, director, writers, actors, synopsis
            link: link to the directory where the movie is stored

            print everything in the .html file
        """
        print("\n<!-- start {} -->" .format(movie_data[0]), file=self.open_file)
        print("<tr valign=\"top\">", file=self.open_file)
        print("<td>\n<img src=\"{}\" width=\"226\" height=\"300\"><br></td><td>\n<p>".format(poster_jpg),
              file=self.open_file)

        fields = ['title:', 'rate/votes:', 'director:', 'writer:', 'actors:', 'synopsis:']
        for f, m_d in zip(fields, movie_data):
            print("{} {}<br>".format(f, m_d), file=self.open_file)
        print("<a href=\"{}\">{}</a>".format(link + '/' + file, file), file=self.open_file)  # last arg
        # last lines

        last_lines = ("</p></td></tr><tr>\n"
                      "<td colspan=\"2\" style=\"border-top: none; border-bottom: none; border-left: none; \
                      border-right: none; padding-top: 0.5cm; padding-bottom: 0.5cm; \
                      padding-left: 0.1cm; padding-right: 0.1cm\" valign=\"top\" width=\"100%\">\n"
                      "<center>-------------------------------------------------------</center>\n"
                      "</td></tr>")
        print(last_lines, file=self.open_file)

        print("<!-- end {} -->\n" .format(movie_data[0]), file=self.open_file)

    def bottom_tags(self):
        """ from </table> to </html> """
        bottom = "</table></body>\n</html>"
        print(bottom, file=self.open_file)
        self.open_file.close()

    def parse_data_to_inside_table(self, m_data):
        """
            all data is split and call inside_table one movie
            at a time
        """
        for db_info in m_data:
            db_info_list = list(db_info)
            html = urllib.request.urlopen(db_info_list[0]).read()
            movie = pimdbdata.ParseImdbData(html)
            m_poster = movie.movie_poster()
            rate_votes = movie.rate_value_and_votes()
            db_info_list.insert(2, rate_votes)
            self.inside_table(m_poster, db_info_list[1:-3], db_info_list[-3], db_info_list[-2])
