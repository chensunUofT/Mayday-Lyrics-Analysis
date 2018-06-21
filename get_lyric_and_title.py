import re
import requests
from  lxml.html import fromstring

def get_lyric_by_url(url):
    re_sentence_pattern = re.compile('\[\d\d:\d\d\.\d\d\].*')
    req = requests.get(url=url)
    html_line_to_read = ''
    for html_line in req.iter_lines(1024):
        try:
            html_line = html_line.decode('utf-8')
            if 'fsZx2' in html_line:
                html_line_to_read = html_line
                break
        except:
            print('1')
    lines = html_line_to_read.split(r'<br />')
    lyric_lines = []
    for line in lines:
        re_result = re.findall(re_sentence_pattern, line)
        if re_result:
            lyric_lines.append(re_result[0].split(r']')[-1])
    lyric_lines_no_repeat = list(set(lyric_lines))
    lyric_lines_no_repeat.sort(key=lyric_lines.index)
    lyric = '\n'.join(lyric_lines_no_repeat).replace('\u2027', ' ')
    print(lyric)
    return lyric

def get_song_title_by_url(url):
    req = requests.get(url=url)
    tree = fromstring(req.content)
    title = tree.findtext('.//title').split(' 歌词')[0].replace('?', '')
    return title
