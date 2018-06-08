from album_information import album_id_list, album_list
from get_lyric import get_lyric_by_url


import os


if __name__ == "__main__":
    cwd = os.getcwd()
    for album_id in album_id_list:
        album_title = album_list[str(album_id)]
        path = cwd + '\\' + album_title
        if not os.path.exists(path):
            os.mkdir(path)
        for song_id in range(1, 20):
            url = r"https://mojim.com/cny100012x" + str(album_id) + "x" + str(song_id) + ".htm"
            lyric = get_lyric_by_url(url)
            # TODO: 解析歌名
            # TODO：保存歌词文本至本地
