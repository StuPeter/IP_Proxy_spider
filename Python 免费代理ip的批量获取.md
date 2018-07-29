#Python 免费代理ip的批量获取
---
##简介
网络爬虫的世界，向来都是一场精彩的攻防战。现在许多网站的反爬虫机制在不断的完善，其中最令人头疼的，莫过于直接封锁你的ip。但是道高一尺魔高一丈，在爬取网页的时候，使用上代理ip，便可以有效的避免自己的ip被封锁。

想要使用代理ip，目前你可以去相应的代理网站购买代理ip（*如果是大型的项目还是推荐去购买*），也可以去使用一些代理网站提供的免费的代理ip，不过这些ip还是存在很多问题的，有些不可用，有些不稳定，有些时效短。不过如果量大的话，还是有不少可以使用的。

基于这个目的，利用Python的requests库写了一个简单的批量获取免费代理ip的程序，其中包括“下载+验证”程序。下面将简单介绍代码思路和使用方法。


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

###2. 下载代理ip ([parsing_html.py](https://github.com/StuPeter/IP_Proxy_spider/blob/master/parsing_html.py))

#### 2.1. 获取网页
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

#### 2.2. 保存ip
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

#### 2.3. 页面解析
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

如果要获取完整的程序，可以去我的GitHub：[IP _Proxy _spider](https://github.com/StuPeter/IP_Proxy_spider)，或则我的csdn下载页面：[https://download.csdn.net/download/q_quanting/10570293](https://download.csdn.net/download/q_quanting/10570293)

###3. 验证代理ip ([checking_ip.py](https://github.com/StuPeter/IP_Proxy_spider/blob/master/checking_ip.py))

#### 3.1. 文件查重
在第二部分获取代理ip中，我是将获取的代理ip信息直接保存在txt文件中，因此我写了一个简单的函数用于查重，这里的查重思路就是获取txt文件中的每一行元素，组成列表。对列表使用自带的set函数，这里需要注意的是：**这种方法会改变列表原来的顺序**。函数如下：

    def check_repeat(path):
    """
    检查文件中每一行的内容是否重复，删除重复内容
    :param path: 文件路径
    :return:
    """
    try:
        # 读取文件
        data_list = []
        with open(path, "r") as fr:
            lines = fr.readlines()
            fr.close()
        for line in lines:
            data_list.append(line)
        new_data_list = list(set(data_list))    # 查重
        file_name = path.split("/")
        print(file_name[-1] + "文件共有 " + str(len(data_list)) + " 条数据")
        print("经过查重,现在共有 " + str(len(new_data_list)) + " 条数据")
        # 保存文件
        with open(path, "w") as f:
            for i in range(len(new_data_list)):
                f.write(new_data_list[i])
            f.close()
            print(file_name[-1] + "文件查重成功")
    except Exception as e:
        print("文件查重失败！！！")
        print(e)

#### 3.2. 代理ip格式化
对于我们从网页获取的ip的格式基本为以下格式：
    
    5.135.66.232___8554___透明___http___法国___XXXX___XX___7.869 秒___4秒前
	220.230.120.101___8286___高匿___http___韩国___XXXX___XX___4.14 秒___11秒前

可以看出来，从页面解析出来的代理ip的信息中间都是使用“---”进行隔开，为了方便直接使用，在此需要将上述的的格式转换为以下格式：

    5.135.66.232:8554
	220.230.120.101:8286

函数如下：

    def ip_format(read_path, save_path):
    """
    将文件中的代理ip进行格式化转换，并进行查重
    :param read_path: 读取待转换的代理ip的文件路径
    :param save_path: 转换完成的代理ip的保存路径
    :return:
    """
    data_list = []
    with open(read_path, "r") as fr:
        lines = fr.readlines()
        fr.close()
    for line in lines:
        new_line = line.split("___")
        ip_format_line = new_line[0].replace(" ", "") + ":" + new_line[1] + "\n"
        data_list.append(ip_format_line)
    with open(save_path, "a") as fs:
        for i in range(len(data_list)):
            fs.write(data_list[i])
        fs.close()
        print("文件保存成功")
        fs.close()

#### 3.3. 验证代理ip
由于免费的代理ip很多都是无法使用，或是不稳定，或是时效短。所以验证代理ip是否可用，就非常有必要。主要的验证原理就是，使用代理ip去访问网页，判断是否能够正常访问。在此我选择的网站是“[站长之家](http://ip.chinaz.com/)”，这个网站可用直接返回你当前使用的ip以及ip所在地。这里需要注意的是**访问前可以设定连接超时的时间**如果访问时间超过一定时间，就直接跳过这个代理ip。我建议是设定在2秒内，具体的可以看以下函数：

    def ip_test(ip_proxies):
    """
    验证单个代理ip是否可用
    :param ip_proxies: 待验证ip，例如：101.96.10.36:88
    :return:
    """
    url = "http://ip.chinaz.com/"
    headers = {
        "Host": "ip.chinaz.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "https://blog.csdn.net/Winterto1990/article/details/51220307",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }
    proxies = {"http": "http://" + ip_proxies, }   # 设置代理
    res = requests.get(url, headers=headers, proxies=proxies, timeout=1)    # timeout为设定的相应时长，建议在2秒内
    # 解析网页
    soup = BeautifulSoup(res.text, "html.parser")
    info_list = soup.find_all("p", {"class": "getlist pl10"})
    for info in info_list:
        is_local = info.get_text()
        print(info.get_text())
    return is_local.find("XXX.XXX.XXX.XXX")  # 判断是否为本地的地址

验证效果如下：
![](https://i.imgur.com/eGALm3Z.png)

#### 3.4. 批量验证代理ip
最后便是批量的对代理ip进行验证，实际上这就是调用3.3.中验证代理ip中的程序。具体程序如下：

    def ip_batch_inspection(read_path, save_path):
    """
     验证多个代理ip是否可用
    :param read_path: 代理ip文件路径
    :param save_path: 验证可用的代理ip保存路径
    :return:
    """
    with open(read_path, "r") as fr:
        lines = fr.readlines()
        fr.close()
        count = 0
        file_name = read_path.split("/")
        print(file_name[-1] + "文件共有 " + str(len(lines)) + " 条数据")
        for line in lines:
            count += 1
            ip_proxies = line.replace("\n", "")
            try:
                is_local = ip_test(ip_proxies)  # 如果是本地ip，返回值为大于0数值
                if is_local < 0:
                    with open(save_path, "a") as fs:
                        fs.write(ip_proxies + "\n")
            except Exception as e:
                pass
                # print("ip不可用")
            print("验证中......%.2f%%" % (count/len(lines)*100))
        print("验证完毕")


###4. 使用的例程 ([get_proxy.py](https://github.com/StuPeter/IP_Proxy_spider/blob/master/get_proxy.py))
这里就是将上述的函数都整合起来，就能够实现批量获取免费的代理ip。

    #!/usr/bin/env python  
	# _*_ coding:utf-8 _*_  
	#  
	# @Version : 1.0  
	# @Time    : 2018/7/27
	# @Author  : 圈圈烃
	# @File    : get_proxy
	# @Description: 下载+验证，获取可用ip
	#
	#
	from checking_ip import *
	from parsing_html import *


	def main():

	    today = time.strftime("%Y_%m_%d")     # 当前日期
	    ip_pools_path = "ip_proxy\\" + today + "_ip_pools.txt"                 # 原始ip保存路径
	    ip_format_pools_path = "ip_proxy\\" + today + "_ip_format_pools.txt"   # 格式化后ip保存路径
	    ip_use_path = "ip_proxy\\" + today + "_ip_use.txt"                     # 可用ip保存路径
	
	    open_proxy = True  # 是否要开启代理模式
	    if not open_proxy:
	        # 不开启代理模式，直接获取代理ip
	        get_data5u_free_ip(None, ip_pools_path)
	        get_kuaidaili_free_ip(None, ip_pools_path)
	        get_xsdaili_free_ip(None, ip_pools_path)
	        get_xicidaili_free_ip(None, ip_pools_path)
	        get_89ip_free_ip(None, ip_pools_path)
	    else:
	        # 开启代理模式，获取代理ip
	        available_ip_path = "ip_proxy\\ip_use.txt"  # 目前可用的代理ip的保存路径
	        ip_use_list = []
	        with open(available_ip_path, "r") as fr:
	            ip_use_lines = fr.readlines()
	            for ip_use_line in ip_use_lines:
	                ip_use_line_new = ip_use_line.replace("\n", "")
	                ip_use_list.append(ip_use_line_new)
	        for i in range(len(ip_use_list)):
	            # 获取ip建立IP池
	            try:
	                print("正在使用第" + str(i) + "条代理ip")
	                get_data5u_free_ip(ip_use_list[i], ip_pools_path, open_proxy)
	                break
	            except:
	                pass
	        for i in range(len(ip_use_list)):
	            # 获取ip建立IP池
	            try:
	                print("正在使用第" + str(i) + "条代理ip")
	
	                get_kuaidaili_free_ip(ip_use_list[i], ip_pools_path, open_proxy)
	                break
	            except:
	                pass
	        for i in range(len(ip_use_list)):
	            # 获取ip建立IP池
	            try:
	                print("正在使用第" + str(i) + "条代理ip")
	                get_xsdaili_free_ip(ip_use_list[i], ip_pools_path, open_proxy)
	                break
	            except:
	                pass
	        for i in range(len(ip_use_list)):
	            # 获取ip建立IP池
	            try:
	                print("正在使用第" + str(i) + "条代理ip")
	                get_xicidaili_free_ip(ip_use_list[i], ip_pools_path, open_proxy)
	                break
	            except:
	                pass
	        for i in range(len(ip_use_list)):
	            # 获取ip建立IP池
	            try:
	                print("正在使用第" + str(i) + "条代理ip")
	                get_89ip_free_ip(ip_use_list[i], ip_pools_path, open_proxy)
	                break
	            except:
	                pass
	    # 筛选ip进行查重
	    ip_format(ip_pools_path, ip_format_pools_path)
	    check_repeat(ip_format_pools_path)
	    # 验证ip可用性
	    ip_batch_inspection(ip_format_pools_path, ip_use_path)
	
	
	if __name__ == '__main__':
	    main()

####实现效果
![](https://i.imgur.com/V1WdAEO.png)

## 最后
完整程序，欢迎下载

我的csdn资源：[https://download.csdn.net/download/q_quanting/10570293](https://download.csdn.net/download/q_quanting/10570293)

我的GitHub：[https://github.com/StuPeter/IP_Proxy_spider](https://github.com/StuPeter/IP_Proxy_spider)

希望对大家有所帮助！：-）
   

