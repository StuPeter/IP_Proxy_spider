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
