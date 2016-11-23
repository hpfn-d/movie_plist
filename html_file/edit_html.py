import re
import getpass


class EditHtml(object):
    def __init__(self):
        self.path_html_file = '/home/' + getpass.getuser() + '/Vídeos/index.html'
        self.html_file_lines = None

    def pull_from_html(self):
        """
           get lines in the .html file
        """
        # path_html_file = '/home/' + getpass.getuser() + 'Vídeos/index.html'
        with open(self.path_html_file, 'r') as html_file:
            self.html_file_lines = html_file.readlines()

    def push_to_html(self):
        """
           put back lines in the .html file
           after self update/remove methods
        """
        f = open(self.path_html_file, 'w')
        f.writelines(self.html_file_lines)
        f.close()

    def update_m_html(self, u_movie, u_file):
        self.pull_from_html()

        mark_start = '<!-- start ' + u_movie + ' -->\n'
        count_l = self.html_file_lines.index(mark_start)
        sub_count = count_l
        for sub_line in self.html_file_lines[count_l:]:
            if sub_line.startswith('<a href'):
                get_string = re.compile('No_movie_file_yet')
                self.html_file_lines[sub_count] = get_string.sub(u_file, sub_line, count=2)
                break
            sub_count += 1

        self.push_to_html()

    def remove_m_html(self, r_movie):
        """
            :param r_movie: movie name and year
            :return: nothing
        """
        self.pull_from_html()

        mark_start = '<!-- start ' + r_movie + ' -->\n'
        mark_end = '<!-- end ' + r_movie + ' -->\n'
        start_line = self.html_file_lines.index(mark_start)
        end_line = self.html_file_lines.index(mark_end)

        print("remove from {} to {}".format(start_line, end_line))
        del self.html_file_lines[start_line:end_line + 1]

        self.push_to_html()
