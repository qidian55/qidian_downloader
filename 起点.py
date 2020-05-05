#coding:utf-8
#“作者有话说”已丢弃
from bs4 import BeautifulSoup
import requests
import argparse
import json
import tqdm

def download(sh):
    if br.head('https://m.qidian.com/book/%s'%sh).status_code==404:
        exit('书号不存在或书籍已下架')
    html=br.get('https://m.qidian.com/book/%s'%sh).text
    sm=html[:html.find('_')]
    sm=sm[sm.find('<title>')+7:]
    print('正在下载'+sm)
    with open('%s.epub'%sm,'wb') as fout:
        for chunk in br.get('http://download.qidian.com/epub/%s.epub'%sh, stream=True).iter_content(chunk_size=512):
            if chunk:
                fout.write(chunk)
        fout.close()
    print('下载完成')

def search(gjc,check=False):
    i=1
    html=requests.get('https://www.qidian.com/search?kw=%s&page=%s'%(gjc,i)).text
    soup=BeautifulSoup(html,'html.parser')
    info=soup.find_all('h4')
    j=0
    while j<len(info):
        if info[j].a['data-eid']!='qd_S05':
            info=info[:j]
        j=j+1
    if check:
        if j==1 or info[0].a.get_text()==gjc:
            return info[0].a['data-bid']
    while True:
        for all in info:
            print(all.a['data-bid'].ljust(10),all.a.get_text())
        if j<10:
            break
        c=input('\n回车浏览下一页')
        if c=="":
            i=i+1
            html=requests.get('https://www.qidian.com/search?kw=%s&page=%s'%(gjc,i)).text
            soup=BeautifulSoup(html,'html.parser')
            info=soup.find_all('h4')
            j=0
            while j<len(info):
                if info[j].a['data-eid']!='qd_S05':
                    info=info[:j]
                j=j+1
        else:
            break
    print('没有更多了!')

def dump(sh,fs='web'):
    if br.head('https://m.qidian.com/book/%s'%sh).status_code==404:
        exit('书号不存在或书籍已下架')
    html=br.get('https://m.qidian.com/book/%s'%sh).text
    sm=html[html.find('<title>')+7:html.find('_')]
    zz=html[html.find('_')+1:html.find('著_')]
    print('找到书籍《%s》'%sm)
    html=br.get('https://m.qidian.com/book/%s/catalog'%sh).text
    datas=html[html.find('g_data.volumes')+17:]
    datas=datas[:datas.find(';')]
    datas=json.loads(datas)
    ids=[]
    n=sum([len(data['cs']) for data in datas])
    f=open('%s.txt'%sm,'w',encoding='utf-8')
    f.write('书名：%s\n'%sm)
    f.write('作者：%s\n'%zz)
    f.write('原文链接：https://book.qidian.com/info/%s\n\n目录\n'%sh)
    for data in datas:
        f.write('%s\n'%data['vN'])
        for each in data['cs']:
            f.write(' %s\n'%each['cN'])
            ids.append(each['id'])
    f.write('\n')
    print('准备爬取%d章节'%len(ids))
    t=tqdm.tqdm(total=len(ids),ascii=True)
    i=0
    while i<len(ids):
        try:
            sj=br.get('https://m.qidian.com/book/%s/%s'%(sh,ids[i])).text
        except:
            print('下载第%d章出错，重试'%i)
            continue
        sj=sj[sj.find('g_data.chapter')+17:]
        sj=sj[:sj.find('g_data.chapterUrlTpl')-2]
        sj=json.loads(sj)
        f.write('%s\n'%sj['chapterName'])
        f.write(sj['content'].replace('<p>','\n')+'\n\n')
        i=i+1
        t.update()
    f.close()
    t.close()
    print('爬取完成')

def check(sh):
    i=1
    ml=category(sh)
    ml=[y['cN'] for x in ml for y in x['cs']]
    for t in ml:
        n=t[:t.find('章')]
        n=n[n.find('第')+1:]
        if n.isnumeric():
            n=int(n)
            if abs(n-i)<2:print(t,end='\r')
            else:print('\n章节缺失：第%d-%d章\n%s'%(i+1,n-1,t))
            i=n
        else:
            print(t)

br=requests.Session()
parser=argparse.ArgumentParser()
parser.add_argument('command',help='可用命令：dump/download\tsearch')
parser.add_argument('argv',help='可用参数：书号/书名\t关键词')
parser.add_argument('-c','--cookie',help='使用cookie')

args=parser.parse_args()
if args.cookie:
    qidian_cookie_dict=dict([l.split("=", 1) for l in args.cookie.split("; ")])
    br.cookies.update(qidian_cookie_dict)
if args.argv.startswith('https://'):args.argv=args.argv.split('/')[4]
if args.command=='dump':
    if args.argv.isnumeric():
        dump(args.argv)
    else:
        dump(search(args.argv,True))
elif args.command=='download':
    if args.argv.isnumeric():
        download(args.argv)
    else:
        download(search(args.argv,True))
elif args.command=='search':
    search(args.argv)
elif args.command=='check':
    check(args.argv)