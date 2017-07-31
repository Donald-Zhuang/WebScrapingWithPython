　　这阵子在学习爬虫，做练习需要一个禁止爬虫且只需添加Header就能绕过的网站。运气不错，找到一个HTTPS协议的，考虑到该网站内容比较special（人类进步的阶梯^_^），所以本文会把网站的相关信息码掉。
　　python处理http协议部分，本文采用的是urllib.request，没有用[Requests](http://docs.python-requests.org/zh_CN/latest/index.html)。通过相关网站介绍可知，如果采用这个库，本文中各个实现的代码会少些，也不会遇到我后面处理的gzip解压缩问题。不过对于我这种新手来说，有时适当踩些坑有利于学习，毕竟“朝抵抗力最大的路径走”，收获的东西会更多。
　　在做Demo时,Python提示--> urlopen error unknown url type: https，也就是不支持https协议。随后查到是安装Python时，系统没有安装openssl-devel导致，因此需重新安装openssl-devel库 -->具体可以参考[python内置的urllib模块不支持https协议的解决办法](http://blog.csdn.net/zyz511919766/article/details/25049365)。不同于文章介绍的，我的系统是Ubuntu，而Ubuntu采用的安装指令是下面这两条。
``` shell
sudo apt-get install openssl
sudo apt-get install libssl-dev
```
　　安装好openssl-devel库后，重新安装一遍Python，采用如下代码测试，不再提示不支持，也确认该网站是禁止爬虫的。　

```　python
#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
import urllib.request

url='https://abc.de/'
urllib.request.urlretrieve(url, 'test.html')
```

![403 forbidden错误](http://img.blog.csdn.net/20170730204724978?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

　　这个网站真是练爬虫第一关的不错选择，对付这个网站的反爬虫策略，解法是通过urllib.request中添加http请求头部字段，实现模拟浏览器访问，具体代码如下。下面的这些字段都是通过chrome的F12抓下来的，删除了一部分：
``` python
#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
import urllib.request

url='https://abc.de/'
req = urllib.request.Request(url)
req.add_header('Host', 'abc.de')
req.add_header('Connection','keep-alive')
req.add_header('Cache-Control','max-age=0')
req.add_header('Upgrade-Insecure-Request','1')
req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
req.add_header('Accept-Encoding', 'gzip, deflate, sdch, br')
req.add_header('Accept-Language','zh-CN,zh;q=0.8,en;q=0.6')

data = urllib.request.urlopen(req).read()

print(data)
```
　　实际测试绕过成功，不再提示403 forbidden了。不过出现新的问题，抓下来的数据是一大波encode的数据。一开始我以为是编码问题，于是根据网页的charset信息加了data.decode('utf-8')，但提示报错，随后尝试其他各种编解码处理方式都没有用。

![绕过反爬出现乱码](http://img.blog.csdn.net/20170730204926159?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

　　无计之下，重新回来看response header，在看到content-encoding字段的时候，才想起还有一个幺蛾子，所以google解决方案，随后参考[Python 抓取网页乱码原因分析](https://zhuanlan.zhihu.com/p/21057822)添加如下代码

![header信息](http://img.blog.csdn.net/20170730205159064?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

　　专栏代码实现不能直接套用，有错误，因此添加调整代码如下：

``` python
#-*- coding: utf-8 -*-
import urllib.request
import gzip
import io 

data = urllib.request.urlopen(req)
encoding = data.getheader('Content-Encoding')
content = data.read()
if encoding == 'gzip':
    buf = io.BytesIO(content)
    gf = gzip.GzipFile(fileobj=buf)
    content = gf.read()
    
#with open('test.html',"wb") as fb:
#    fb.write(data)
    
print(content)
```

　　调整后测试效果如下，成功绕过反爬策略和实现gzip解压，解决了数据无法识别的问题。

![绕过成功](http://img.blog.csdn.net/20170730205313413?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

　　考虑到上面添加header的方式比较麻烦，而参考书中提供的另一种方式也半斤八两，所以我尝试了另一种方式，具体代码如下。测试时也发现网站，去除Accept-Language会导致绕过失败，依旧返回403错误。这也就说明，该网站是通过多个字段来判别是否为爬虫访问，所以以后处理的时候，可以尽量把正常访问时浏览器提交字段都提交一遍，避免不必要的麻烦。
``` python
#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
import urllib.request
import gzip
import io 

'''[TEST]'''
url = 'https://abc.de/'

Headers = {
        'Host':'abc.de',
        'Connection':'keep-alive',
        'Cache-Control':'max-age=0',
        'Upgrade-Insecure-Request':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch, br',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6'
}

req = urllib.request.Request(url, None, Headers)
data =urllib.request.urlopen(req).read()
print(data)
```
