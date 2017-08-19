# WebScrapingWithPython
这个仓库的code都是基于python3的，在脚本中也有相关信息体现。这个仓库中除了代码，也有一些markdown文档，用于介绍这个仓库中部分代码。

Chapter3 [基本练习](https://github.com/Donald-Zhuang/WebScrapingWithPython/tree/master/Chapter3_SimplePythonScripts)
这一章主要是做基础练习，提供了斐波拉切数列输出、文件操作、随机数生成、9*9算法表生成。

Chapter4 [Urllib库的使用](https://github.com/Donald-Zhuang/WebScrapingWithPython/tree/master/Chapter4_UsageOfUrllib)
这一章围绕这python3的urllib库的使用展开，关于urllib库可以参考python官方库文档[Urllib](https://docs.python.org/3/library/urllib.html)进行深入了解。这个目录提供了http header的修改实现，主要通过[add_header 函数](https://github.com/Donald-Zhuang/WebScrapingWithPython/blob/master/Chapter4_UsageOfUrllib/4_3_1_AddHeader_by_add_header.py)和[python 字典添加的方式](https://github.com/Donald-Zhuang/WebScrapingWithPython/blob/master/Chapter4_UsageOfUrllib/4_3_2_AddHeader_by_dictionary.py)两种方式实现，我比较喜欢后者的实现方式，简洁也方便修改。HTTP请求[GET](https://github.com/Donald-Zhuang/WebScrapingWithPython/blob/master/Chapter4_UsageOfUrllib/4_5_1_HttpMethodGET.py)和[POST](https://github.com/Donald-Zhuang/WebScrapingWithPython/blob/master/Chapter4_UsageOfUrllib/4_5_1_HttpMethodGET.py)的demo code，后者是比较重要的一个demo，因为爬虫模拟登陆时常会用到。在这两个之后，也提供了[http代理服务](https://github.com/Donald-Zhuang/WebScrapingWithPython/blob/master/Chapter4_UsageOfUrllib/4_5_3_HttpProxy.py)的demo代码和请求过程中的[异常处理](https://github.com/Donald-Zhuang/WebScrapingWithPython/blob/master/Chapter4_UsageOfUrllib/4_8_URLError.py)，这两部分挺重要的，相信你也不想抓数据抓到一半就因为异常断了或者被禁止访问了，然后后面自己连正常访问这个网站都不行，这两个简单demo就是这部分的简单模型，实际应用会比这个稍微复杂一点 。
这部分我也整了一篇markdown文档介绍了[模拟浏览器请求头和gzip解压](https://github.com/Donald-Zhuang/WebScrapingWithPython/blob/master/Chapter4_UsageOfUrllib/4_3_Header.md)。

Chapter5 [正则表达式和cookie](https://github.com/Donald-Zhuang/WebScrapingWithPython/tree/master/Chapter5_RegExpAndCookie)
这章就是正则表达式和cookie的应用，也是对上一章的学习进行搭积木的操作。这里面在基本实验后，提供了两个模型一个是查找页面中，以[正则匹配.cn或者.com结尾的网页链接](https://github.com/Donald-Zhuang/WebScrapingWithPython/blob/master/Chapter5_RegExpAndCookie/5_4_1_findURL.py)和[抓取页面中的Email地址 ](https://github.com/Donald-Zhuang/WebScrapingWithPython/blob/master/Chapter5_RegExpAndCookie/5_4_2_findEMail.py)，后者用到了正则表达式的零宽度正回顾后发断言使匹配准确些。
在整cookie部分的时候，这里提供了一个[模拟登陆CSDN](https://github.com/Donald-Zhuang/WebScrapingWithPython/blob/master/Chapter5_RegExpAndCookie/5_4_3_Cookie_Login_CSDN.py)的demo和对应[介绍文章](https://github.com/Donald-Zhuang/WebScrapingWithPython/blob/master/Chapter5_RegExpAndCookie/5_4_3_Login_CSDN.md)说明相关实现原理。

Chapter6 [各类爬虫demo](https://github.com/Donald-Zhuang/WebScrapingWithPython/tree/master/Chapter6_WebCrawler)
这一章主要是提供各种基本爬虫demo，如[京东手机照片抓取](https://github.com/Donald-Zhuang/WebScrapingWithPython/blob/master/Chapter6_WebCrawler/6_1_photoCrawler_jd.py)，[网页内Url链接抓取demo](https://github.com/Donald-Zhuang/WebScrapingWithPython/blob/master/Chapter6_WebCrawler/6_2_UrlCrawler_jd.py)，[糗事大百科热点抓取](https://github.com/Donald-Zhuang/WebScrapingWithPython/blob/master/Chapter6_WebCrawler/6_3_TextCrawler_qiushibaike.py)和[微信公众号文章抓取](https://github.com/Donald-Zhuang/WebScrapingWithPython/blob/master/Chapter6_WebCrawler/6_3_TextCrawler_qiushibaike.py)。这些demo提供了爬虫的一些最基本功能的操作练习，基本上写完这些demo就可以做一些简单好玩的小爬虫。

Chapter7 [浏览器模拟](https://github.com/Donald-Zhuang/WebScrapingWithPython/tree/master/Chapter7_BrowserSimulation) 
这一张就是过下之前的实现，也没什么特殊的，不过我也有想法后续吧这个demo做得完善些，加入其它因素。

Chapter9 [定向抓取腾讯视频评论](https://github.com/Donald-Zhuang/WebScrapingWithPython/blob/master/Chapter9_VideoComment/TencentVideoComment_Crawer.py)
这一章的demo相对比较好玩点，通过分析页面请求抓取视频的“深度解读”，涉及的东西有js和json，为此也专门整了一篇[文章](https://github.com/Donald-Zhuang/WebScrapingWithPython/blob/master/Chapter9_VideoComment/Article%20About%20this%20crawer.md)介绍这个虫子。

未完待续.....