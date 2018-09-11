今天总算是赶了个夜车把之前差点烂尾的Mayday歌词项目改了个差不多了，于是决定记点笔记。
上Github repo： [https://github.com/chensunUofT/Mayday-Lyrics-Analysis](https://github.com/chensunUofT/Mayday-Lyrics-Analysis)

首先，词频统计需要素材，于是一番小规模调研之后锁定了这个页面：
[http://mojim.com/cnh100012.htm]
以及专辑及歌词页面：
[http://mojim.com/cn100012x54.htm]
[http://mojim.com/cny100012x54x12.htm]
可以看出，专辑及歌曲页面的url都是有pattern可循的：
http://mojim.com/cny100012x `ID1` x `ID2` .htm
其中ID1为专辑ID，由于太多了而需要的只是其中几张唱片，所以手动记录；ID2为歌曲数量，写的时候偷了个懒，也手动记录了，其实可以写一个判断的。  # TODO_1

通过上边的方法得到所需歌词页面的url之后，需要从页面得到歌曲标题及歌词内容。
歌曲标题部分比较简单，可以从页面title中获得。
```python
def get_song_title_by_url(url):
    req = requests.get(url=url)
    tree = fromstring(req.content)
    title = tree.findtext('.//title').split(' 歌词')[0].replace('?', '')
    return title
```
歌词部分就比较坑了，先看一下源码：

![](http://www.sunchen.tech/wp-content/uploads/2018/09/f5672decb6249f683ebd8645fdcf16b7.png)

可以说是一片乱七八糟了。经过一通观察，发现每个歌词页面源码的歌词行都是带
`<dt id='fsZx2' class='fsZx2' >`
这个tag的。于是通过这一特征定位歌词行：
```python
for html_line in req.iter_lines(1024):
    try:
        html_line = html_line.decode('utf-8')
        if 'fsZx2' in html_line:
            html_line_to_read = html_line
            break
```
然后把这一行按换行符(` r'<br />' `)split开。然后呢，我们发现歌词有时候会出现两次（例如截图中的情况），那我只想要一次，然后我就发现，带时间戳的行肯定都是歌词内容，于是祭出大杀器Regular Expression筛选出带时间戳的行：
```python
re_sentence_pattern = re.compile('\[\d\d:\d\d\.\d\d\].*')
for line in lines:
    re_result = re.findall(re_sentence_pattern, line)
```
然后呢，这行还有可能是例如`五月天 天使`或者`作词：阿信`这种内容，为了筛掉，带有中文冒号`：`或者`五月天`字样的，就都不要啦。此处手动对不起《晚安，地球人》：
> 紫皮肤　大脑袋　血液不绿也不蓝　在我已经毁灭的星球　我比五月天还帅

哎呀，三点了，赶紧言归正传……
得到所需歌词行之后，去掉时间戳，就可以把歌词取出来啦。
```python
if re_result:
    if '：' not in re_result[0] and '五月天' not in re_result[0]:
        lyric_lines.append(re_result[0].split(r']')[-1])
```
由于某些歌曲里重复行数实在太多（憨人、人生海海 了解一下？），做一下去重，替换掉一些奇怪的会引起bug的字符之后用换行符连接：
```python
lyric_lines_no_repeat = list(set(lyric_lines))
lyric_lines_no_repeat.sort(key=lyric_lines.index)
lyric = '\n'.join(lyric_lines_no_repeat).replace('\u2027', ' ')
```
这个lyric就是我们可以用来写进文本、拿来分析的歌词啦！阶段性任务完成！
写入文本文件部分较为简单，略去不表。
接下来是词频统计部分。先说如何读取到所有文件。如果是想统一某一张专辑，就先定位到专辑对应的目录，然后
```python
for _, _, filenames in os.walk(album_dir):
    for file_name in filenames:
        with open(album_dir+file_name, 'r') as f:
            text = f.read()
```
就ok了。如果要统计所有专辑，就需要列出歌词目录下所有子目录下的所有文件路径：
```python
for root, dirs, filenames in os.walk(lyrics_dir):
    if not dirs:
        for file_name in filenames:
            with open(root+'/'+file_name, 'r') as f:
                text = f.read()
```
打开文件之后，利用jieba工具包进行中文分词，用Counter进行统计：
```python
def count_text(text):
    seg_list = jb.cut(text, cut_all=False)
    c = Counter(seg_list)
    return c
```
之后，去掉短词，输出想得到的统计结果就ok了。

最后说说这个项目我最得意的地方：词云！

![](http://www.sunchen.tech/wp-content/uploads/2018/09/%E8%87%AA%E4%BC%A0.png)

这里不得不提到wordcloud这个库：[https://github.com/amueller/word_cloud] 小小star不成敬意。
至于我这边，看似我前天晚上弄了半宿，其实今天想来也没遇到什么太大的坑，最想实现的遮罩功能也实现了，开心~
噢对了，这里想起一个坑，关于带参数运行的。python里是可以调用`sys.argv`（ [https://www.tutorialspoint.com/python/python_command_line_arguments.htm] ）来获取运行参数的，只不过获取到的是字符串，需要类型转换一下。如果觉得用命令行带上参数来运行不高雅，可以在pycharm里设置一下：

![](http://www.sunchen.tech/wp-content/uploads/2018/09/9010d76a7b93bfbfd71f542a7e68ebdb.png)

![](http://www.sunchen.tech/wp-content/uploads/2018/09/17d5a6895c6ba0bc66ca1957a63ae5e6.png)

把需要的参数写在parameters里就ok了。
