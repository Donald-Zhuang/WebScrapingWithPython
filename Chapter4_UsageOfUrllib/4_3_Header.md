　　爬虫练习，在找禁止爬虫的网站时，找到一个HTTPS协议的，鉴于该网站比较special（人类进步的阶梯^_^），所以下面的网站的相关信息都被码掉。本文我是选了request，没有用[Requests](http://docs.python-requests.org/zh_CN/latest/index.html)，就了解到的信息如果采用这个库，整体代码实现会少些，也不会遇到我后面处理的编码问题，不过感觉有些坑还是要踩下，这样了解的东西会多点。
　　在运行爬虫的时候发现Python提示--> urlopen error unknown url type: https
　　也就是不支持https协议，不过https现在这么流行，一定有解决办法。随后了解到是安装Python时，系统没有安装openssl-devel导致，因此需重新安装openssl-devel库 -->具体参考[python内置的urllib模块不支持https协议的解决办法](http://blog.csdn.net/zyz511919766/article/details/25049365)，不过我用的是Ubuntu，而Ubuntu采用的安装指令是下面这两条。
``` shell
sudo apt-get install openssl
sudo apt-get install libssl-dev
```
　　安装好openssl-devel库后，重新安装Python，采用如下代码测试，没有提示不支持了，也确认该网站是禁止爬虫的。　

```　python
#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
import urllib.request

url='https://abc.de/'
urllib.request.urlretrieve(url, 'test.html')
```
![403 forbidden错误](http://img.blog.csdn.net/20170730204724978?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　　这个网站是练第一关的，解法是通过urllib.request添加http请求头部字段，实现模拟浏览器访问，代码如下：
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
　　实际测试效果如下，不再提示403 forbidden了，也就是反爬成功。不过新问题出现，一大波乱码，一开始我以为是编码问题，于是根据网页的charset信息加了data.decode('utf-8')，但测试提示报错，随后尝试各种编解码方式都没有用。
![绕过反爬出现乱码](http://img.blog.csdn.net/20170730204926159?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　　重新回来看response header，在看到content-encoding字段的时候，才想起还有一个幺蛾子，所以参考[Python 抓取网页乱码原因分析](https://zhuanlan.zhihu.com/p/21057822)介绍补刀
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
　　测试效果如下，成功绕过反爬策略和实现gzip解压
![绕过成功](http://img.blog.csdn.net/20170730205313413?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

　　我在测试另一套实现方式（如下，主要是为了方便编辑header）的时候，也发现网站关注了Accept-Language是否在请求头中，如果没有会返回403错误。
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
