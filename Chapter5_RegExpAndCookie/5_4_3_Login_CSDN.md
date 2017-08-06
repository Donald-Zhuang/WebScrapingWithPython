　　这周学习的主题是正则表达式和cookie，原本是计划每天晚上11点下班到家，练上一两个钟就把这部分过了，结果这周各种事情和不再状态，所以没整完，直至今天才把相关问题过掉。其实这部分也挺不错的，也并没有想象中容易，所以好事多磨。这周练习的综合习题就是模拟登陆CSDN，实现过程不难，最终实现代码在最后面。

###1. 登陆的步骤 --> 请求和页面分析
　　第一步我们需要清楚登陆流程以及需要提交哪些数据到服务器以完成登陆认证。进入CSDN[登录界面](https://passport.csdn.net/account/login?ref=toolbar)， 我们实际登陆下，并通过F12进入chrome DevTools抓下相关数据，需要注意的是调试前我们要勾选如下选项，保证登陆成功页面跳转时，数据能保留下来，不被清空。
![这里写图片描述](http://img.blog.csdn.net/20170806094429955?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　　输入账号和密码后点击登陆。在众多请求中，我们可以找到有且仅有的一个POST请求，这个也就是我们相关登陆信息所在的请求了。
![这里写图片描述](http://img.blog.csdn.net/20170806094520578?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　　通过DevTools可以看到请求的主体如下。因此，POST到服务器的数据有五项，username，password，lt，execution和_eventId。前两项比较好理解，即为我们输入的账号和密码，那下面的三项是哪里蹦出来的？有果必有因，我们分析下页面源代码。
![这里写图片描述](http://img.blog.csdn.net/20170806094558023?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　　Ctrl + Shift + C（检查页面元素）选中密码输入框，Chrome页面分析工具跳到Element页如下位置。从这里我们可以看到如下信息，红框中三项也就是我们需要的数据了。通过注释（我最喜欢写注释这么干脆的孩子！！），我们可以知道LT这个参数是用于账号登陆时相应请求处理的流水号。如果没有这个流水号，请求会被判定非法并强制重新登陆。这样我们又学习到一个新的反爬手段了，然而我们此次就是要绕过这个机制——提取这个数据附到POST数据上。 
![这里写图片描述](http://img.blog.csdn.net/20170806094709226?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　　除了如上的请求数据外，我们还需要针对cookie做相关处理，因为我们登陆后的状态是记录在cookie中。


###2. 如何模拟 --> 流程代码实现
#### 1) Cookie的引入
　　HTTP协议是一种不保存状态（stateless）的协议，即不对通讯中请求和响应之间的通讯状态做保存。每次新请求都会有新响应，因此我们通讯过程中的相关信息得不到保存，登陆状态也不会被记录下来，这会导致我们每访问一个页面就需要重新登陆一次以鉴别身份。但，实际并不是这样，这是因为有cookie技术的引入。如下，客户端的request header中Cookie字段带有本地的cookie信息，访问时发给服务器，作为一种身份标示和认证。而服务器会根据实际需要发出Set-Cookie的响应，此时客户端会对应将cookie保存下来，后续访问服务器资源时，再附上，供服务器做处理。
![这里写图片描述](http://img.blog.csdn.net/20170806094740227?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　　具体实现如下，其中我加入了文件用于存放相关cookie信息，现在的目的是方便debug看情况。在实际应用中，可以通过直接读取cookie文件信息，然后进行http访问，可免去重复登录的操作。
``` python 
'''for cookie function'''
CookieFile  = "cookie.txt"
CookieJar   = http.cookiejar.MozillaCookieJar(CookieFile)        # 创建cookie对象
CookieProcessor = urllib.request.HTTPCookieProcessor(CookieJar)  # 创建cookie处理器
Opener  = urllib.request.build_opener(CookieProcessor, urllib.request.HTTPHandler) # 以对应的cookie处理器创建opener对象
urllib.request.install_opener(Opener)    #安装opener为全局
```
如果不想加入文件操作的话，可以参考如下实现，[Reference](https://docs.python.org/3.6/library/http.cookiejar.html#module-http.cookiejar)：
``` python
import http.cookiejar, urllib.request
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(Opener)    #安装opener为全局
```
 
#### 2) 反爬虫
``` python
Headers = {
        'Connection'    :'keep-alive',
        'Cache-Control' :'max-age=0',
        'User-Agent'    :'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept'        :'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#       'Accept-Encoding'   :'gzip, deflate, br',
        'Accept-Language'   :'zh-CN,zh;q=0.8,en;q=0.6',
        'Upgrade-Insecure-Request':'1',
        }
```
　　CSDN的反爬绕过是最简单的添加header的方式，可参考[反爬虫绕过初级——添加http header和gzip解压处理](http://blog.csdn.net/Donald_Zhuang/article/details/76407358)。CSDN貌似只检测User-Agent，因此添加这个header之后，再访问登陆页面就不会出现403 forbidden的提示。我一般直接采用下面这个header，避免服务器通过检测多个字段做反爬时，需要去查是哪些字段，再去添加。
　　可以看到下面这个headers被我注释掉了Accept-Encoding字段。因为这个字段应该是Transparent Negotiation的，也就是客户端如果请求有声明支持gzip，CSDN服务器就会采用gzip传输，否则就直接传输未经压缩的源文件，为了少去解压缩这部分工作，所以我直接注释掉了。

#### 3) 数据提取
``` python
'''data for login'''
LoginUrl    = "https://passport.csdn.net/account/login?ref=toolbar"
LoginData   ={
    "username" : "",
    "password" : ""
}

RegExp_Template         = "(?<=name=\"%s\" value=\")%s(?=(\">)?)"      # tempalate for Regular Expression
Lt_RegExp        = RegExp_Template % ( "lt",         "LT-\d{6}-\w+" )
Execution_RegExp = RegExp_Template % ( "execution",  "\w+" )
EventId_RegExp   = RegExp_Template % ( "_eventId",   "\w+" ) 

'''pretreatment for login'''
req = urllib.request.Request(LoginUrl, None, Headers)
String = urllib.request.urlopen(req).read().decode('utf-8')
CookieJar.save(ignore_discard=True, ignore_expires=True)

'''To get the data we need to post to Login Server'''
LoginData['lt'] = re.search(Lt_RegExp, String).group()
LoginData['execution']  = re.search(Execution_RegExp, String).group()
LoginData['_eventId']   = re.search(EventId_RegExp, String).group()
```
　　除了账号和密码我们可直接输入外，lt、execution、_eventId这三个需要在网页中抓取。首先需要请求下登陆页面--> 抓取响应页面 -->分析页面内容获取三个数据。
　　网上介绍的多是通过beautifulsoup分析页面数据，我看了下相关实现，感觉确实方便很多。不过既然是练习正则表达式了，那我还是采用正则抓取相关内容，这部分的正则也是比较简单的。关于正则表达式的，推荐通过[正则表达式30分钟入门教程](https://deerchao.net/tutorials/regex/regex.htm)学习。我测试正则一般都是将页面源码复制下来，然后在notepad++中测试是否能正确匹配，然后才置于源码中，这样可以避开一些坑。
![这里写图片描述](http://img.blog.csdn.net/20170806094843824?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　　通过对下面源码的解析，我们可以看到他们有一定的共性，也就是下面这条表达式：
>RegExp_Template = "(?<=name=\"%s\" value=\")%s(?=(\">)?)"

　　变量只是两个'%s'部分，为此我写成template方便编程和看code。这个表达式可分三部分，第一部分是_**(?<=name=\"%s\" value=\")**_，是一个零宽度正回顾后发断言，只匹配不占用字符；第二部分是我们需要的字符的正则，也就是第二个**%s**；第三部分是零宽度负回顾先行断言，也是只匹配不占用字符。根据下面的场景，我们可以知道，第三部分其实可以不用加上去，因为目标字符结尾都是\w，因此到点即会停止匹配。
　　这三个数据中，execution这个比较有趣，e后面这个数字就是访问次数，如果你的cookie为新时，那这个值为1，后续采用同个cookie访问登陆页，依次加一，所以可以用于检测cookie是否正常连续工作。 

#### 4) 模拟登陆
 
``` python
'''log in'''
PostData = urllib.parse.urlencode(LoginData).encode('utf-8')
req = urllib.request.Request(LoginUrl, PostData, Headers)
UrlData = urllib.request.urlopen(req)
CookieJar.save(ignore_discard=True, ignore_expires=True)
 
data = UrlData.read()
print('\n' + '='*10 + 'login response headers' + '='*10 + '\n', UrlData.info(), '\n'+'='*42 )
with open('LoginPage.html','wb') as hfile:
    hfile.write(data)
```

　　在集齐username，password，lt，execution和_eventId五项数据后，我们可以开始模拟登陆CSDN了。
　　urllib.parse.urlencode(LoginData).encode('utf-8')这部分是将数据转换成网络访问的格式，我们设置的数据是dictionary的，但实际POST到服务器的数据是下面这样的，因此需要做转换。
　　
![这里写图片描述](http://img.blog.csdn.net/20170806094942023?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　　
　　转换后，可以通过Request将POST data和Request Headers发送到对应的URL，登陆CSDN。此时相关信息也会被cookie记录下来，在下面的code中CookieJar.save(ignore_discard=True, ignore_expires=True)这个是保存cookie数据，在这里我们是保存到文件中，其中ignore_discard表示即便cookie即将被弃用也保存下来，而ignore_expires表示若该cookie已存在则直接覆盖。下面是一个cookie文件的实例。
　　
![这里写图片描述](http://img.blog.csdn.net/20170806095053060?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　　
　　登陆和保存cookie后，还有返回一个跳转页面，这个页面很重要，有多重要呢，请看下图，大量红圈数据，用心体会下，哈哈哈哈。
　　
![这里写图片描述](http://img.blog.csdn.net/20170806095124103?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvRG9uYWxkX1podWFuZw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

#### 4) 登陆后确认
　　我登陆后采用的确认页面是，http://my.csdn.net/?ref=toolbar，也就是看看自己的个人信息，至此，模拟登陆完成。

###3. 总结
　　总的来说，这个作为入门练习也是一个挺好玩的项目。这次debug和抓信息，感觉自己在整个访问过程中，就是处于裸奔状态，虽说csdn的登陆页面是https协议的，对外还好，但如果你的浏览器中加装其他插件呢？像一些广告去除插件，这种直接对访问数据进行拦截过滤的，如果直接过滤采集你的登陆和相关页面访问信息呢，细思极恐。最后附上整体实现代码，我菜鸡一枚，所以代码难免有考虑不足的地方，请多多指教。

``` python
#!/usr/local/bin/python3
#-*- coding: utf-8 -*-
 
import urllib.request
import urllib.parse
import http.cookiejar
import re
 
'''data for login'''
LoginUrl    = "https://passport.csdn.net/account/login?ref=toolbar"
VisitUrl    = "http://my.csdn.net/?ref=toolbar"
LoginData   ={
    "username" : "",
    "password" : ""
}
 
Headers = {
        'Connection'    :'keep-alive',
        'Cache-Control' :'max-age=0',
        'User-Agent'    :'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept'        :'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#       'Accept-Encoding'   :'gzip, deflate, br',
        'Accept-Language'   :'zh-CN,zh;q=0.8,en;q=0.6',
        'Upgrade-Insecure-Request':'1',
        }
 
'''please test the following regular expression before actual use'''
RegExp_Template         = "(?<=name=\"%s\" value=\")%s(?=(\">)?)"      # tempalate for Regular Expression
Lt_RegExp        = RegExp_Template % ( "lt",         "LT-\d{6}-\w+" )
Execution_RegExp = RegExp_Template % ( "execution",  "\w+" )
EventId_RegExp   = RegExp_Template % ( "_eventId",   "\w+" )
 
 
def Login_Func(LoginData):
 
    '''for cookie function'''
    CookieFile  = "cookie.txt"
    CookieJar   = http.cookiejar.MozillaCookieJar(CookieFile)
    CookieProcessor = urllib.request.HTTPCookieProcessor(CookieJar)
    Opener  = urllib.request.build_opener(CookieProcessor, urllib.request.HTTPHandler)
    urllib.request.install_opener(Opener)
 
    '''pretreatment for login'''
    req = urllib.request.Request(LoginUrl, None, Headers)
    String = urllib.request.urlopen(req).read().decode('utf-8')
    CookieJar.save(ignore_discard=True, ignore_expires=True)
 
    '''To get the data we need to post to Login Server'''
    LoginData['lt'] = re.search(Lt_RegExp, String).group()
    print("[DEBUG] Get LT:  %s "%Lt_RegExp, LoginData.get('lt'))
    LoginData['execution']  = re.search(Execution_RegExp, String).group()
    print("[DEBUG] Get execution: %s "%Execution_RegExp, LoginData.get('execution'))
    LoginData['_eventId']   = re.search(EventId_RegExp, String).group()
    print("[DEBUG] Get eventId: %s "%EventId_RegExp, LoginData.get('_eventId'))
 
    '''log in'''
    PostData = urllib.parse.urlencode(LoginData).encode('utf-8')
    req = urllib.request.Request(LoginUrl, PostData, Headers)
    UrlData = urllib.request.urlopen(req)
    CookieJar.save(ignore_discard=True, ignore_expires=True)
 
    data = UrlData.read()
    print('\n' + '='*10 + 'login response headers' + '='*10 + '\n', UrlData.info(), '\n'+'='*42 )
    with open('LoginPage.html','wb') as hfile:
        hfile.write(data)
 
    '''Check whether log in sucessfully'''
    req = urllib.request.Request(VisitUrl,None,Headers)
    UrlData = urllib.request.urlopen(req)
    data = UrlData.read()
    print('\n' + '='*10 + 'Visit response headers'+'='*10 + '\n', UrlData.info(), '\n'+'='*42 )
    with open('VisitPage.html','wb') as hfile:
        hfile.write(data)
 
if __name__ == '__main__':
    Login_Func(LoginData)
```
