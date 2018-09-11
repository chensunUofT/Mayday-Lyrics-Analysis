from album_information import *
import sys
import os
import matplotlib.pyplot as plt
import jieba as jb
from PIL import Image
import numpy as np

from os import path
from wordcloud import WordCloud

# d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

def word_cloud_one_album(album_order):

    print(0)
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
    print(1)
    # print(total_text_cut)

    mask = np.array(Image.open(cwd + '\\mayday.png'))

    font = './fonts/SourceHanSerifSC-Regular.otf'
    # Display the generated image:
    # the matplotlib way:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    print(2)

    # lower max_font_size
    # wordcloud = WordCloud(collocations=False, font_path=font, width=2000, height=2000, margin=2).generate(total_text_cut)
    wordcloud = WordCloud(background_color="white", max_words=500, mask=mask, font_path=font)
    wordcloud.generate(total_text_cut)

    # plt.figure(figsize=(20,20))
    # plt.imshow(wordcloud, interpolation="bilinear")
    # plt.axis("off")
    # plt.show()

    wordcloud.to_file('mayday_wc2.png')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.figure()
    # plt.imshow(mask, cmap=plt.cm.gray, interpolation='bilinear')
    # plt.axis("off")
    plt.show()

    print(3)

if __name__ == "__main__":
    print(-1)
    word_cloud_one_album(sys.argv[-1])
