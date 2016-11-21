"""
   edit the .html file to remove a movie entry
"""

def EditHtmlRemove(movie_title):
    with open('/home/zaza/Vídeos/index.html', 'r') as html_file:
        html_file_lines = html_file.readlines()

    mark_start = '<!-- start ' + movie_title + ' -->\n'
    mark_end = '<!-- end ' + movie_title + ' -->\n'
    start_line = html_file_lines.index(mark_start)
    end_line = html_file_lines.index(mark_end)

    print("remove from {} to {}" .format(start_line, end_line))
    del html_file_lines[start_line:end_line+1]

    f = open('/home/zaza/Vídeos/index.html', 'w')
    f.writelines(html_file_lines)
    f.close()