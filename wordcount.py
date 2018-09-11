import jieba as jb
import re
from collections import Counter
import requests


def count(text):
    seg_list = jb.cut(text, cut_all=False)
    c = Counter(seg_list)
    print(c)


def get_all_url():
    url_list = []
    album_id_list = [1, 2, 6, 13, 18, 24, 29, 37, 54]
    for album_id in album_id_list:
        for song_id in range(1, 20):
            url = r"https://mojim.com/cny100012x" + str(album_id) + "x" + song_id + ".htm"
            url_list.append(url)
    return url_list


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
    # TODO: 用RE匹配带时间戳的行
    lines = html_line_to_read.split(r'<br />')
    lyric_lines = []
    for line in lines:
        re_result = re.findall(re_sentence_pattern, line)
        if re_result != []:
            lyric_lines.append(re_result[0].split(r']')[-1])
    lyric_lines_no_repeat = list(set(lyric_lines))
    lyric_lines_no_repeat.sort(key=lyric_lines.index)
    lyric = '\n'.join(lyric_lines_no_repeat)
    # print(lyric)
    return lyric




if __name__ == "__main__":
    # re_Chinese = re.compile(r'[\u4e00-\u9fa5]+')
    # with open(r'听不到.txt') as f:
    #     text_all = f.read().split(r'<br /><br /><br /><br />')[1]
    #     text_Chinese = ''.join(re.findall(re_Chinese, text_all))
    #     # print(text_Chinese)
    #     count(text_Chinese)
    count(get_lyric_by_url('https://mojim.com/cny100012x37x11.htm'))
