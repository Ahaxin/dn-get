# !/usr/bin/env python
#-*-coding:utf-8-*-
#by fly2tomato

#实现功能：
#1，获得多瑙真实播放地址，该地址可直接在浏览器中播放或者用下载工具（迅雷，you-get等）下载，屏蔽广告
#2，大福利：免费看多瑙vipAV
#使用方法：
#1，浏览器登录多瑙，进入影片播放页面，将播放页面的url复制，
#2，然后在shell运行： python dn—get.py； 回车
#3，输入复制的url，回车
#4，获得真实播放地址，
#5，对于av，获得的地址是2min预览版，请将url中的'2'换成'1'，如'cr-snyncjp-2.mp4'换成'cr-snyncjp-1.mp4'
import cookielib
import urllib
import httplib
import urllib2
import re
import requests
import os
import sys
import time
from selenium import webdriver

url1 = 'http://www.dnvod.eu/'
url2 = 'http://www.dnvod.eu/Movie/Readyplay.aspx?id=qhYe%2fY0pcsk%3d'


#获取ASP.NET_SessionId
def getSessionID (url2):
    try:
        s = requests.Session()
        #r0 = s.get(url1)
        #headr0 =r0.headers
        #time.sleep(6)
        r1 = s.get(url2)
        header = r1.headers
        rrrr = [header]
        #print rrrr[0]['Set-Cookie']
        reg = r'ASP.NET_SessionId=(.*); path=/; HttpOnly'
        partern =  re.compile(reg)
        sessionID = partern.findall(rrrr[0]['Set-Cookie'])
        return sessionID
    except urllib2.URLError,e:
        print e.code
        print e.reason


#ASP.NET_SessionId有时间有效性，若程序返回-4 则说明ASP.NET_SessionId已过期需要重新获取，若返回-3则表示key不对
# cookies1 = '__cfduid=d58922e790c902ec87ff7384dcfc0b2451469995023; _gat=1; ASP.NET_SessionId=2ueljjviy4takln2vcmds345; jiathis_rdc=%7B%22http%3A//www.dnvod.eu/Adult/detail.aspx%3Fid%3D0cY7CF0zIt4%253d%22%3A0%7C1469995032649%2C%22http%3A//www.dnvod.eu/Adult/Readyplay.aspx%3Fid%3D%252bJRDqHAbXxw%253d%22%3A%220%7C1469995033515%22%7D; _ga=GA1.2.733351123.1469995023'
# cookies2 = '__cfduid=d58922e790c902ec87ff7384dcfc0b2451469995023; _gat=1; ASP.NET_SessionId=2ueljjviy4takln2vcmds345; _ga=GA1.2.733351123.1469995023'

def getCookies():
    #brower = webdriver.Chrome('/Users/Junior/dev/python/chromedriver')
    brower = webdriver.PhantomJS(executable_path="/Users/Junior/dev/python/phantomjs-2.1.1-macosx/bin/phantomjs")
    brower.get(url2)
    cookies = brower.get_cookies()
    cookie = cookies[5]
    cooki = cookie["value"]
    #print cooki
    #cookies = 'ASP.NET_SessionId='+sessionID
    return cooki
def getUserAgent():
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
    return user_agent

def getRealUrl(urlString):
    stringOne = urlString[26:]
    searchVodReg = r'/(.*)/'
    searchVodPattern = re.compile(searchVodReg)
    searchVodResult = searchVodPattern.findall(stringOne)
    whichTypeVod = searchVodResult
    vodString = whichTypeVod[0]
    urlPre = urlString[:27]+vodString+'/'


    urlPreLength = len(urlPre)
    urlMostimportant = urlString[urlPreLength:]
    vodList = ['vod','gvod','hvod','ivod','jvod','kvod','lvod','live']
    serverList = ['server1','server2','server3']

    try:
        urltoattend =  urlPre+urlMostimportant
        findrealRequest = urllib2.Request(urltoattend)
        findrealResponse = urllib2.urlopen(findrealRequest)
        realVIPURL = urltoattend
    except urllib2.URLError,e:
        for i in range(len(vodList)):
            urltoattend = urlString[:27] + vodList[i] + '/' + urlMostimportant
            findrealRequest = urllib2.Request(urltoattend)
            try:
                findrealResponse = urllib2.urlopen(findrealRequest)
                realVIPURL = urltoattend
                break
            except urllib2.URLError, e:
                for j in range(len(serverList)):
                    urltoattend = 'http://' + serverList[j] + '.dnplayer.tv/' + vodList[i] + '/' + urlMostimportant
                    try:
                        findrealRequest = urllib2.Request(urltoattend)
                        findrealResponse = urllib2.urlopen(findrealRequest)
                        realVIPURL = urltoattend
                        break
                    except urllib2.HTTPError, e:
                        print "获取高清播放地址中..."
    return  realVIPURL




#获取cookie，当网站出现5秒等待时，用这个方法获得cookie
#cookies = 'ASP.NET_SessionId='+getCookies()
#获取cookie，当网站未出现5秒等待时，用这个方法获得cookie
cookies = 'ASP.NET_SessionId='+getSessionID(url2)[0]


#构建user agent
user_agent = getUserAgent()
#构建headers
headers = {"User-Agent": user_agent,
"Content-Type": "application/x-www-form-urlencoded",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Referer": "http://www.dnvod.eu/",
#"Content-Length": "36",
"Accept-Encoding": "",
"Accept-Language": "de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2,zh;q=0.2,zh-TW;q=0.2,fr-FR;q=0.2,fr;q=0.2",
"X-Requested-With": "XMLHttpRequest",
"DNT": "1",
"Cookie": cookies}
headers2 = {"Host": "www.dnvod.eu",
"Content-Length": "36",
"Cache-Control": "nax-age=0",
"Accept": "*/*",
"Origin": "http://www.dnvod.eu",
"X-Requested-With": "XMLHttpRequest",
"User-Agent": user_agent,
"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
"DNT": "1",
"Referer": "http://www.dnvod.eu/Movie/Readyplay.aspx?id=%2bWXev%2bhf16w%3d",
"Accept-Encoding": "",
"Accept-Language": "de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2,zh;q=0.2,zh-TW;q=0.2,fr-FR;q=0.2,fr;q=0.2",
"Connection": "keep-alive",
"Cookie": cookies}



loopString = True
while(loopString):
    inputArg = raw_input('1,直接输入多瑙观看页面URL，请按1\n2,搜索影片，请按2\n请输入：')
    if inputArg == '1':
        inputurl = raw_input('\n输入多瑙观看页面URL：\n')
        playUrl = inputurl
        loopString = False
    elif inputArg == '2':
        inputMovieName = raw_input('\n查找视频名称：')
        if inputMovieName[0:2] == 'av':
            urlSearch = 'http://www.dnvod.eu/Adult/Search.aspx?tags='+inputMovieName[2:len(inputMovieName)]
            searchRequest = urllib2.Request(urlSearch,None,headers)
            searchResponse = urllib2.urlopen(searchRequest)
            searchdataResponse = searchResponse.read()
            #print searchdataResponse
            searchReg = r'<a href="(.*%3d)">'
        else:
            urlSearch = 'http://www.dnvod.eu/Movie/Search.aspx?tags='+inputMovieName
            searchRequest = urllib2.Request(urlSearch,None,headers)
            searchResponse = urllib2.urlopen(searchRequest)
            searchdataResponse = searchResponse.read()
            #print searchdataResponse
            #searchReg = r'<a href="/\w(.*%3d)">'
            searchReg = r'<a href="(.*%3d)">'
        searchPattern = re.compile(searchReg)
        searchResult = searchPattern.findall(searchdataResponse)
        searchRegName = r'3d" title="(.*)">'
        searchPatternName = re.compile(searchRegName)
        searchResultName = searchPatternName.findall(searchdataResponse)
        #print searchResult
        print('搜索到'+str(len(searchResult))+'个结果：\n')

        for i in range(len(searchResultName)):
            print str(i+1)+': '+searchResultName[i]+'\n'

        whichResultStr = raw_input('请输入数字：')
        whichResultInt = int(whichResultStr)-1

        filmIdReg = r'id=(.*%3d)'
        filmIdPattern = re.compile(filmIdReg)
        filmIdResult = filmIdPattern.findall(searchResult[whichResultInt])
        #print filmIdResult
        if inputMovieName[0:2] == 'av':
    	    searchUrl = 'http://www.dnvod.eu/Adult/detail.aspx?id='+filmIdResult[0]
        else:
    	    searchUrl = 'http://www.dnvod.eu/Movie/detail.aspx?id='+filmIdResult[0]

        #print 'searchResult: '+searchResult[whichResultInt]
        #print 'searchUrl: '+searchUrl
        detailRequest = urllib2.Request(searchUrl,None,headers)
        detailResponse = urllib2.urlopen(detailRequest)

        detaildataResponse = detailResponse.read()
        #print detaildataResponse
        detailReg = r'Readyplay.aspx\?id=(.*)" target'
        detailPattern = re.compile(detailReg)
        detailResult = detailPattern.findall(detaildataResponse)
        totalEps = len(detailResult)
        #print detailResult
        whichEpisodeStr = raw_input("一共有"+str(totalEps)+"集，请选择集数：")
        whichEpisodeInt = int(whichEpisodeStr)-1
        if inputMovieName[0:2] == 'av':
            playUrl = 'http://www.dnvod.eu/Adult/Readyplay.aspx?id='+detailResult[whichEpisodeInt]
        else:
    	    playUrl = 'http://www.dnvod.eu/Movie/Readyplay.aspx?id='+detailResult[whichEpisodeInt]
        print '播放页面URL：\n'+playUrl
        loopString = False
    else:
        print '\n输入错误，请重新输入'



requestFir = urllib2.Request(playUrl,None,headers)
responseFir  = urllib2.urlopen(requestFir)
data_responseFir = responseFir.read()
#print data_responseFir

para1 = playUrl[20:25]#Adult or Movie
#print para1
reg     = r'id:.*\'(.*)\','
pattern = re.compile(reg)
result  = pattern.findall(data_responseFir)
para2   = result[0]

urlSec = 'http://www.dnvod.eu/'+para1+'/GetResource.ashx?id='+para2+'&type=htm'
#data = 'key=4c4e0393d0b0444cb72b0dcd9bc13417'

regkeyString = r'key:.*\'(.*)\','
patternkeyString = re.compile(regkeyString)
resultkeyString = patternkeyString.findall(data_responseFir)
keyString = resultkeyString[0]


data = urllib.urlencode({'key':keyString})
requestSec = urllib2.Request(urlSec,data,headers)
responseSec = urllib2.urlopen(requestSec)
real_url = responseSec.read()
#print real_url
#print "\nID:                 "+para2
#print '\nKey:                '+keyString
#print '\nASP.NET_SessionId:  '+sessionID

if real_url == "-4":
    print 'ASP.NET_SessionID已过期，请重新获取'
elif real_url == "-3":
    print 'key错误，请重新设置key'
else:
    print "\n~~~~~~~~真实播放地址（直接复制到浏览器打开或者用工具下载）：~~~~~~~~\n"
    if cmp(para1,"Adult") == 0:
        pattern0 = re.compile(r'(\d||\d\d||\d_\d)\.mp4')
        num0 = re.split(pattern0,real_url)
        hdurl = num0[0]+'1'+'.mp4'+num0[2]
        if hdurl == real_url:
            print '该片为免费资源，播放地址为：\n'+hdurl+'\n'
        else:
            print '预览版: \n'+real_url+'\n'
            print '完整版: \n'+hdurl+'\n'
    else:
        pattern = re.compile(r'(\d||\d\d||\d\d\d||\d\d\d\d||\d\d\d\d\d||\d\d\d\d\d\d||\d\d\d\d\d\d\d||\d\d\d\d\d\d\d\d)\.mp4')
        num = re.split(pattern,real_url)
        #print num
        #print "低清版: \n"+real_url+'\n'
        hdurl0 = num[0] + 'hd-' + num[1] + '.mp4' + num[2]
        hdurl = getRealUrl(hdurl0)
        print "\n 高清版: \n"+hdurl+'\n'

bDownload = raw_input('\n是否需要下载视频到当前目录(for mac and linux only)？(y/n)')
if bDownload == 'y':
    os.system('axel -a -n 5 '+hdurl)
else:
    isPlay = raw_input('\n是否需要在线播放该视频(for mac and linux only)？(y/n)')
    if isPlay == 'y':
        os.system('mplayer '+hdurl)
    else:
	print '\nlove & peace\nfly2tomato\n'
