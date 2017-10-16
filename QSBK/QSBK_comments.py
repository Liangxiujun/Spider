# coding=utf-8
import urllib
import urllib2
import re
import  thread
import time

#糗事百科爬虫类
class QSBK:
    #初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        #初始化headers
        self.headers = {'User-Agent' :self.user_agent}
        #存放段子变量，每个原始是每一页的段子
        self.stories = []
        #存放程序是否继续变量
        self.enable = False

    #传入某一页索引获得页面代码
    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            #构建请求的request
            request = urllib2.Request(url,headers=self.headers)
            #利用urlopen获取页面代码
            response = urllib2.urlopen(request)
            #将页面转码为UTF8编码
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print u"error,链接糗事百科失败，错误原因",e.reason
                return None
    #传入某一页代码，返回本业不带图片的段子列表
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "page load error"
            return None
        #正则获取段子作者，正文，点赞数（如果正则获取为空，可能是糗百页面改版，页面查看元素调试）
        pattern = re.compile('h2>(.*?)</h2.*?content">.*?<span>(.*?)</.*?number">(.*?)</',re.S)
        items = re.findall(pattern,pageCode)
        #用来存储每一页的段子
        pageStories = []
        #遍历正则表达式的匹配结果
        for item in items:
            #item[0] 段子作者，item[1] 内容正文 item[2] 点赞数
            pageStories.append([item[0].strip(),item[1].strip(),item[2].strip()])
        return pageStories

    #加载炳提取页面内容，加入到列表中
    def loadPage(self):
        if self.enable==True:
            if len(self.stories)<2:
                #获取新一页
                pageStories = self.getPageItems(self.pageIndex)
                #将该页的段子存放在全局的list中
                if pageStories:
                    self.stories.append(pageStories)
                    #获取完成之后页面索引加一，表示下次读取下一页
                    self.pageIndex +=1
    #调用方法，每次敲回车获取一个段子
    def getOneStory(self,pageStories,page):
        #遍历一页的段子
        for story in pageStories:
            input = raw_input()
            #每当输入回车一次，判断一下是否要加载新的页面
            self.loadPage()
            #输入Q，退出程序结束
            if input == "Q":
                self.enable = False
                return
            print u"第%d页\t发布人：%s\t 赞：%s\n%s" %(page,story[0],story[2],story[1])
    #开始方法
    def start(self):
        print u'正在读取糗事百科，按回车查看新段子，Q键退出'
        #设置变量为True，程序可以正常运行
        self.enable = True
        #先加载一页内容
        self.loadPage()
        #局部变量，控制当前读到第几页
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                #从全局list中获取一页的段子
                pageStories = self.stories[0]
                #当前读到的页面+1
                nowPage +=1
                #将全局的list第一个元素删除，因为已经取出
                del self.stories[0]
                #输出该页段子
                self.getOneStory(pageStories,nowPage)

spider = QSBK()
spider.start()
