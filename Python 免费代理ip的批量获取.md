#Python 免费代理ip的批量获取
---
##简介
网络爬虫的世界，向来都是一场精彩的攻防战。现在许多网站的反爬虫机制在不断的完善，其中最令人头疼的，莫过于直接封锁你的ip。但是道高一尺魔高一丈，在爬取网页的时候，使用上代理ip，便可以有效的避免自己的ip被封锁。

想要使用代理ip，目前你可以去相应的代理网站购买代理ip（*如果是大型的项目还是推荐去购买*），也可以去使用一些代理网站提供的免费的代理ip，不过这些ip还是存在很多问题的，有些不可用，有些不稳定，有些时效短。不过如果量大的话，还是有不少可以使用的。

基于这个目的，利用Python的requests库写了一个简单的代理ip池，“下载+验证”程序。下面将简单介绍代码思路和使用方法。


##Python实现思路

###1. 确定获取免费代理ip的网页
通过寻找，发现目前有些提供免费代理ip网站有以下三类情况：

1. 所有的免费代理ip信息在网页标签中
2. 所有的免费代理ip信息在网页标签中，不过使用了一些隐藏标签
3. 所有的免费代理ip信息在图片中

为了使付出和回报成正比，我就不去选择第二类和第三类的完整获取免费的ip。本文将选择第一类网页进行提取（这一类的网站的数量也是较多的，基本满足小规模的使用需求），我在此选取了以下5个网站：

1. 无忧代理  : [http://www.data5u.com/](http://www.data5u.com/)
![](https://i.imgur.com/Dt6OeeT.png)


2. 快代理   : [https://www.kuaidaili.com/](https://www.kuaidaili.com/)
![](https://i.imgur.com/AnFp8YG.png)


3. 小舒代理  : [http://www.xsdaili.com/](http://www.xsdaili.com/)
![](https://i.imgur.com/VVidiSZ.png)


4. 西刺代理  : [http://www.xicidaili.com/](http://www.xicidaili.com/)
![](https://i.imgur.com/NWvQm5M.png)


5. 89免费代理: [http://www.89ip.cn/](http://www.89ip.cn/)
![](https://i.imgur.com/ixn5hcb.png)

###2. 解析网页

####1. 获取网页
要解析一个网页，第一步就是先获取页面。因为有多个页面要获取，为了方便就编写一个获取页面的函数，便于之后进行调用。函数如下：

    def get_html(url, open_proxy=False, ip_proxies=None):
    """
    获取页面的html文件
    :param url: 待获取页面的链接
    :param open_proxy: 是否开启代理，默认为False
    :param ip_proxies: 若开启，代理地址
    :return:
    """
    try:
        pattern = re.compile(r'//(.*?)/')
        host_url = pattern.findall(url)[0]
        headers = {
            "Host": host_url,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }
        if open_proxy:   # 判断是否开启代理
            proxies = {"http": "http://" + ip_proxies, }  # 设置代理，例如{"http": "http://103.109.58.242:8080", }
            res = requests.get(url, headers=headers, proxies=proxies, timeout=5)
        else:
            res = requests.get(url, headers=headers, timeout=5)
        res.encoding = res.apparent_encoding  # 自动确定html编码
        print("Html页面获取成功 " + url)
        return res.text     # 只返回页面的源码
    except Exception as e:
        print("Html页面获取失败 " + url)
        print(e)

这个函数设置了三个参数，分别是：待获取页面的链接、是否开启代理、代理地址。最终的返回值为网页的源码文本。

其中headers部分是伪装为浏览器请求头，这个函数还设置了利用代理去获取页面，也就是说你可以利用已有的代理去获取这些页面。

####2. 保存ip
当我们对获取的每个页面进行解析时，都会获取页面上的代理ip，同样的，每个页面获取的代理ip都要保存下来，在此写一个保存函数，将获得的代理ip写入文件。在这里我是将代理ip写入txt文件。函数如下：

    def save_ip(data, save_path):
    """
    将获取的ip信息保存到文件中
    :param data: 代理ip数据，数据类型为列表
    :param save_path: 代理ip保存路径
    :return:
    """
    try:
        print("总共获取 " + str(len(data)) + " 条数据")
        with open(save_path, "a") as f:
            for i in range(len(data)):
                f.write(data[i])
            f.close()
            print("文件保存成功")
    except Exception as e:
        print("文件保存失败！！！")
        print(e)

####3. 页面解析
这里就是最关键的页面解析了，由于不同的网站，代理ip在其中的所在位置也都不同，因此这里需要对每个网站单独写解析函数，在此我以“[无忧代理](http://www.data5u.com/)”为例子，函数如下：

    def get_data5u_free_ip(ip_proxies, save_path, open_proxy):
    """
    获取无忧代理的免费ip
    :param ip_proxies: 要使用的代理ip（这里是用代理ip去爬代理ip）
    :param save_path: 代理ip保存路径
	:param open_proxy: 是否开启代理，默认为False
    :return:
    """
    url_list = [
        "http://www.data5u.com/free/index.shtml",
        "http://www.data5u.com/free/gngn/index.shtml",
        "http://www.data5u.com/free/gnpt/index.shtml",
        "http://www.data5u.com/free/gwgn/index.shtml",
        "http://www.data5u.com/free/gwpt/index.shtml"
    ]
    ip_list_sum = []    # 代理ip列表
    for i in range(5):
        res_text = get_html(url_list[i], open_proxy=open_proxy, ip_proxies=ip_proxies)
        # 抓取错误页面，主动报异常
        if res_text.find("错误") != -1:
            raise AttributeError('错误页面')
        # 页面解析
        soup = BeautifulSoup(res_text, "html.parser")
        tags = soup.find_all("ul", class_="l2")
        for tag in tags:
            ip_list = []
            ip_info_format = ""
            sps = tag.find_all("li")
            for sp in sps:
                ip_info = sp.get_text()
                ip_list.append(ip_info)
            for j in range(len(sps)):
                # 格式化IP信息
                if j == len(sps) - 1:
                    ip_info_format += str(ip_list[j]) + "\n"
                else:
                    ip_info_format += str(ip_list[j]) + "___"
            ip_list_sum.append(ip_info_format)
    save_ip(ip_list_sum, save_path)


## 最后
希望对大家有所帮助！：-）
    

