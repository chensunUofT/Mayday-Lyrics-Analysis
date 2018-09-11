from album_information import *
import sys
import os
import jieba as jb
from collections import Counter


def analyze(argument):
    if argument in ['all', 'ALL']:
        analyze_all_albums()
    else:
        analyze_one_album(int(argument)-1)
    return


def analyze_all_albums():
    cwd = os.getcwd()
    lyrics_dir = cwd + '\\lyrics\\'
    result_counter = Counter()
    for root, dirs, filenames in os.walk(lyrics_dir):
        if not dirs:
            for file_name in filenames:
                with open(root+'/'+file_name, 'r') as f:
                    text = f.read()
                    result_counter += count_text(text)
    words = result_counter.keys()
    result_copy = result_counter.copy()
    for word in words:
        if len(word) <= len('我'):
            del result_copy[word]
    print(result_copy.most_common(30))
    return


def analyze_one_album(album_order):
    album_title = album_list[str(album_id_list[album_order])]
    cwd = os.getcwd()
    album_dir = cwd + '\\lyrics\\' + album_title + '\\'
    result_counter = Counter()
    for _, _, filenames in os.walk(album_dir):
        for file_name in filenames:
            with open(album_dir+file_name, 'r') as f:
                text = f.read()
                result_counter += count_text(text)
    words = result_counter.keys()
    result_copy = result_counter.copy()
    for word in words:
        if len(word) <= len('我'):
            del result_copy[word]
    print(result_copy.most_common(30))
    # for x, _ in result_copy.most_common(30):
    #     print(x)
    return


def count_text(text):
    seg_list = jb.cut(text, cut_all=False)
    c = Counter(seg_list)
    return c


if __name__ == "__main__":
    # print(sys.argv[-1]+'1')
    analyze(sys.argv[-1])
