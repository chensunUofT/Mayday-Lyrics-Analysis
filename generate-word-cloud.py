from album_information import *
import sys
import os
import matplotlib.pyplot as plt
import jieba as jb
from PIL import Image
import numpy as np

from os import path
from wordcloud import WordCloud


def word_cloud_one_album(album_order):

    album_order = int(album_order)
    album_title = album_list[str(album_id_list[album_order])]
    cwd = os.getcwd()
    album_dir = cwd + '\\lyrics\\' + album_title + '\\'
    album_total_text = ''
    for _, _, filenames in os.walk(album_dir):
        for file_name in filenames:
            with open(album_dir+file_name, 'r') as f:
                text = f.read()
                album_total_text += text
    total_text_cut = ' '.join(jb.cut(album_total_text,cut_all=False))
    wordcloud = WordCloud().generate(total_text_cut)


    mask = np.array(Image.open(cwd + '\\mayday.png'))

    font = './fonts/SourceHanSerifSC-Regular.otf'
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    wordcloud = WordCloud(background_color="white", max_words=500, mask=mask, font_path=font)
    wordcloud.generate(total_text_cut)

    wordcloud.to_file(album_title+ '.png')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.figure()
    plt.show()



if __name__ == "__main__":
    word_cloud_one_album(sys.argv[-1])
