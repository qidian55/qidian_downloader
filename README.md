## [五五断更节][声援]起点小说下载器

运行程序爬取起点小说为txt格式，方便跑路。（注：未订阅章节只显示部分数据，限免除外）

起点中文网cookie形如以下形式：`hiijack=0; _csrfToken=sfdfsfew; newstatisticUUID=313_231; ywkey=fsdafsd; ywguid=43972834`，具体获取方式参见https://blog.csdn.net/weixin_44343074/article/details/105104206

使用格式如下：`python 起点.py dump $BOOK -c "$COOKIE"`，请将$COOKIE换成你自己的cookie，$BOOK换成你要爬取的书名/书号，如`python 起点.py dump 当外神降临异界之时 -c "hiijack=0; _csrfToken=sfdfsfew; newstatisticUUID=313_231; ywkey=fsdafsd; ywguid=43972834"`

### todo list

- [x] python脚本
- [ ] GUI界面