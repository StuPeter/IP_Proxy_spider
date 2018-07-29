#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2018/7/27
# @Author  : 圈圈烃
# @File    : checking_ip
# @Description: 对parsing_html.py中获取并保存的代理ip进行格式化，查重和检验
#
#
from bs4 import BeautifulSoup
import requests
import time


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


