from album_information import album_id_list, album_list, songs_number
from get_lyric_and_title import get_lyric_by_url, get_song_title_by_url


import os


if __name__ == "__main__":

    # make '\lyrics' directory
    cwd = os.getcwd()
    lyric_path = cwd + '\\lyrics\\'
    if not os.path.exists(lyric_path):
        os.mkdir(lyric_path)

    # create text files for lyrics in all albums
    for album_id in album_id_list:

        # make directories for each album
        album_title = album_list[str(album_id)]
        path = lyric_path + album_title
        if not os.path.exists(path):
            os.mkdir(path)

        # get lyrics, create and write text files
        for song_id in range(1, 1+songs_number[str(album_id)]):
            url = r"https://mojim.com/cny100012x" + str(album_id) + "x" + str(song_id) + ".htm"
            lyric = get_lyric_by_url(url)
            song_title = get_song_title_by_url(url)
            with open(path+'\\'+song_title+'.txt', 'w') as f:
                f.write(lyric)
