　　这周和大家分享下腾讯视频评论抓取爬虫，实际抓下来的数据里面除了评论还有其他不少有价值的信息，有部分用户数据可以使用的，不过具体就看大家自己怎么用了。
　　这个demo的具体源码在最后面，下文将对这个demo的实现过程进行说明。
　　其实我挺期待有人评论下我的文章写得怎么样的，会不会啰嗦或者没啥价值的，这样我也可以改进，所以看着不爽，评论下，我改进，哈哈哈。

###页面和请求分析
　　我们要抓的评论主要是深度解读，当然下面的精彩短评和最新短评原理一致。首先ctrl + u查看源码，检索相关评论信息，没抓到合意的内容，因此，结合页面是动态变化的，因此初判数据是通过js加载的。
![这里写图片描述](http://img.blog.csdn.net/20170819114528470?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　　F12开启DevTools，开启过滤js，点击查看更多，有如下request。
![这里写图片描述](http://img.blog.csdn.net/20170819114541713?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　　复制页面请求网址，访问得如下数据情况，抓如下title的值，通过python print出来，可以知道这个就是我们要的评论内容了
![这里写图片描述](http://img.blog.csdn.net/20170819114559461?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
![这里写图片描述](http://img.blog.csdn.net/20170819114615569?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　　那刚才说的精彩短评和最新评论呢，我们可以看出这个在刷新页面后就固定了，那我们应该在刷新时就抓这个数据，清空devtool中的数据，F5刷新页面，抓到如下数据，也就是我们想要的一波。
![这里写图片描述](http://img.blog.csdn.net/20170819114627619?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　　接下来我们是分析请求链接的规律，我们不断点查看更多，直到没有更多评论，然后来回点这几个js查看其header请求规律，发现如下两处在变化，其他的都没变。
![这里写图片描述](http://img.blog.csdn.net/20170819114635559?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

　不变部分分析，upcomment后面的序列，我们根据这个视频的网址https://v.qq.com/x/cover/yoz60y87rdgl1vp/h002446mgco.html， 可知这个是cover后面的那个序列，这个应该是视频的id，既然id在网址中，那非常有利于抓整个网站的各个片源评论，具体见下图。而reqnum则是抓取评论的个数，后面这部分直接去掉也能抓到正确的数据，实际去掉更方便处理数据。
![这里写图片描述](http://img.blog.csdn.net/20170819114646092?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　　然后关于commentid，这个明显就是指各个commentid，分析后也可以发现实际上就是上一个链接的最后一个comment的id，那就实现循环赋值了，整合下来，链接模型就是:
>url_temp  = 'https://video.coral.qq.com/filmreviewr/c/upcomment/%s?commentid=%s&reqnum=%d'

![这里写图片描述](http://img.blog.csdn.net/20170819114701804?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

　　但我们还有解决一个问题，起始条件和终止条件。一开始我们是不知道commentid的，那抓下刷新页面的第一个comment请求，发现是没有commentid的，故应该是有默认值，既然如此，我们直接https://video.coral.qq.com/filmreviewr/c/upcomment/yoz60y87rdgl1vp?commentid=&reqnum=3  也就是commentid置空，抓到起始数据，u所以rl template可以采用。
![这里写图片描述](http://img.blog.csdn.net/20170819114728436?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　　终止条件部分，我们抓最后一个请求，如下为请求的全部内容，我们可以看到，last id还是有的，hasnext为true，这些都不能作为终止条件，但commentid这一节内容为空了（实际内容里面的retnum就是说明此次返回的comment数量，直接可以用），也就是没有内容了，那肯定是可以做为终止条件的。这个请求很重要，因为给了我们一个宏观的认识，也是我们分析评论数据的原型。
![这里写图片描述](http://img.blog.csdn.net/20170819114754581?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

###数据分析
　　上面说的最后一个请求是分析的原型，抓出来情况是下面这个，是一个json，下面标红部分就是我们此次比较关注的内容。reqnum是本次请求的评论个数，retnum是实际返回的个数，last上面有提及是作为组下个访问请求的关键，而commentid里面的内容则是我们想要的评论相关信息了。
![这里写图片描述](http://img.blog.csdn.net/20170819114744992?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

　　分析完整体架构，我们具体分析下commentid的内容，下面我抓取一个评论的数据，其他评论是一样的。
``` json
{
    'targetid': '2013224236',        
    'id': '6294901728253477340',        #comment id
    'rootid': '0',
    'parent': '0',
    'userid': '69443701',               #user id
    'up': '2434',                       #点有用的个数
    'poke': 351,                        #点没用的个数
    'rep': '352',        
    'orireplynum': '444',               #回复个数
    'source': 0,
    'checktype': '1',
    'checkstatus': '1',
    'hotscale': '15',
    'isdeleted': '0',
    'address': '',
    'rank': '-1',
    'time': 1500821525,
    'title': '人点烛，鬼吹灯，胡八一要为革命事业添砖加瓦',    #评论标题
    'abstract': '我已经做......',           #简介
    'content': '<p><span style="text-indent: 2em;">我已经做好了准备，做好了这篇影评发表之后，我会被骂个狗血淋头，.....。</p>',                                     #评论具体内容
    'type': '2',
    'video': [],
    'picture': [],
    'richtype': 2304,
    'custom': '',
    'thirdid': '',
    'timeDifference': '07月23日 22:52:05',
    'replyuser': '',                        #这篇评论回复谁的
    'replyuserid': '0',                     #被回复人id
    'replyhwvip': 0,
    'replyhwlevel': 0,
    'replyhwannual': 0,
    'userinfo':                             #品论人的详细信息
    {
        'userid': 69443701,
        'nick': 'abc',
        'head': 'http://q3.qlogo.cn/g?b=qq&k=',
        'gender': 0,
        'uidex': 'ecec****************33c8403',
        'region': '::',
        'hwvip': '1',
        'hwlevel': '5',
        'hwannual': 1,
        'wbuserinfo': [],
        'identity': '',
        'viptype': 0,
        'thirdlogin': 0,
        'specialidentity': 1
    },
    'score': None,
    'uped': 0,
    'poked': 0
},
```

#具体代码实现
我这个代码只实现抓单个指定视频的数据，如果要自动抓多个的话，稍加调整即可。
``` python
#!/usr/local/bin/python3
#-*- coding: utf-8 -*-

import urllib.request
import http.cookiejar
import gzip
import io
import json

#For templates and configrations
url_temp  = 'https://video.coral.qq.com/filmreviewr/c/upcomment/%s?commentid=%s&reqnum=%d'

#For simulate the behaviour of web browser
host    = 'video.coral.qq.com'
refer  = 'https://v.qq.com/txyp/coralComment_yp_1.0.htm'
Headers = {
        'Host':            host,
        'Connection':      'keep-alive',
        'Cache-Control':    'max-age=0',
        'User-Agent':      'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
        'Accept':          'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer':          refer,
        'Accept-Encoding':  'gzip, deflate',
        'Accept-Language':  'zh-CN,zh;q=0.8,en;q=0.6',
        'Upgrade-Insecure-Requests':  '1',
        }

#cookie处理
def BuildAndInstall_Opener():

    cjar    = http.cookiejar.CookieJar()
    cprocs  = urllib.request.HTTPCookieProcessor(cjar)
    opener  = urllib.request.build_opener(cprocs)
    
    urllib.request.install_opener(opener)

#GZip解码
def Decode_GzipString(data):

    buf = io.BytesIO(data)
    gf  = gzip.GzipFile(fileobj = buf)
    data= gf.read()
    return data

def Get_Data(url):

    req = urllib.request.Request(url, None, Headers)
    content = urllib.request.urlopen(req)

    '''get the content'''
    data = content.read()

    '''data process: Get full data'''
    encoding = content.getheader('Content-Encoding')
    if ( encoding == 'gzip' ):
        data = Decode_GzipString(data)
    
    if len(data) == 0:
        print(data)
        print('[DBG ERR ] Get Data Error ')
    else:
        #如果抓的数据不是很多，也可以直接采用正则。
        data = json.loads(data.decode('utf-8'))

    return data['data']

def Analyse_Comments(data):
    if len(data['commentid']) == 0 :
        print('='*50,'end of comment', '='*50)
        return '0'
    else:
        for comment in data['commentid']:
            if comment['isdeleted'] == '0':
                print('user:', comment['userinfo']['nick'], end = '')
                if comment['replyuser'] != '' :
                    print(' reply to ',comment['replyuser'], end = '')
                #输出格式化，实际内容保留照片的html元素，方便后续处理。
                commstr = comment['content'].replace(u'<p>',u'\r\n\t')
                commstr = re.sub('<[a-zA-Z/]*?>', '',commstr)
                print('\r\ncomment:', commstr) 
            else:
                print(comment['title'], ' is been deleted.')
        return data['last']
    
if __name__ == '__main__':
    
    BuildAndInstall_Opener()
    LastCommentId = ''
    VideoId = input('Please input the videoid which you want to get its comments: \r\n')
    while True:
        url = url_temp % (VideoId, LastCommentId, 10)        
        data = Get_Data(url)
        if len(data) == 0:
            break
        LastCommentId = Analyse_Comments(data) 
        if LastCommentId == '0':
            break
```