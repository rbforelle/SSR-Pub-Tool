#!/usr/bin/python
# -*- coding:utf-8 -*-

import base64
import socket
import json
import platform
import argparse

def b64_url_decode(code):  # 处理padding，补足等号
    return base64.urlsafe_b64decode(str(code+'='*(4-len(code)%4)))
def b64_url_encode(str):  # 处理padding，去掉等号
    return base64.urlsafe_b64encode(str.encode("utf-8")).decode("utf-8").rstrip('=')

def get_host_ip():  # 得到服务器自己的ip地址
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

class SSRSrvConf():
    def __init__(self,host="",port=0,protocol="",method="",obfs="",password="",obfsparam="",protoparam="",remarks="",group=""):
        self.host = host
        self.port = port
        self.protocol = protocol
        self.method = method
        self.obfs = obfs
        self.password = password
        self.obfsparam = obfsparam
        self.protoparam = protoparam
        self.remarks = remarks
        self.group = group

    def set_group(self,group):
        self.group = group

    def set_remarks(self,remarks):
        self.remarks = remarks

    def import_from_conf(self,config_file):  # 从配置文件导入服务器设置
        with open(config_file) as f:  # 判断文件是否符合存在/符合要求
            d = json.load(f)
            self.host = get_host_ip()
            self.port = str(d['server_port'])
            self.password = d['password']
            self.method = d['method']
            self.protocol = d['protocol']
            self.protoparam = d['protocol_param']
            self.obfs = d['obfs']
            self.obfsparam = d['obfs_param']
            self.group = d.get('group', "")
            self.remarks = d.get('remarks', "")
            f.close()

    def print_config(self):  # 打印服务器配置
        print("server:".ljust(15),self.host)
        print("port:".ljust(15), self.port)
        print("password:".ljust(15), self.password)
        print("method:".ljust(15), self.method)
        print("protocol:".ljust(15), self.protocol)
        print("protoparam:".ljust(15), self.protoparam)
        print("obfs:".ljust(15), self.obfs)
        print("obfsparam:".ljust(15), self.obfsparam)
        print("remarks:".ljust(15), self.remarks)
        print("group:".ljust(15), self.group)

    def ssr_link_base64(self):  # 计算当前服务器的链接，不带ssr://
        base64_pass = b64_url_encode(self.password)
        base64_protoparam = b64_url_encode(self.protoparam)
        base64_obfsparam = b64_url_encode(self.obfsparam)
        base64_remarks = b64_url_encode(self.remarks)
        base64_group = b64_url_encode(self.group)

        # ssr: // base64(host: port:protocol: method:obfs: base64pass
        # /?obfsparam = base64param & protoparam = base64param
        # & remarks = base64remarks & group = base64group & udpport = 0 & uot = 0)
        # 中间的base64参数不带末尾等于号
        # https://github.com/shadowsocksrr/shadowsocks-rss/wiki/SSR-QRcode-scheme

        ssr_link_origin = self.host + ":" + self.port + ":" + self.protocol + ":" \
                          + self.method + ":" + self.obfs + ":" + base64_pass \
                          + "/?obfsparam=" + base64_obfsparam \
                          + "&protoparam=" + base64_protoparam \
                          + "&remarks=" + base64_remarks \
                          + "&group=" + base64_group \

        base64_ssr_link = b64_url_encode(ssr_link_origin)  # 最后对ssr链接计算base64
        return base64_ssr_link

    def ssr_link(self):  # 输出ssr链接
        # 返回可以被导入的ssr链接
        return "ssr://" + self.ssr_link_base64()

    def import_from_ssr_link(self,ssr_link):  # 通过链接导入服务器配置
        link_base64 = ssr_link.split("//")[1]  # 去除ssr链接前面的ssr://
        link_original = b64_url_decode(link_base64).decode()  # 解码得到原始链接内容
        # print(link_original)
        # 切分ssr链接，得到必要部分和可选部分
        # 具体参见https://github.com/shadowsocksrr/shadowsocks-rss/wiki/SSR-QRcode-scheme
        main_part_list = link_original.split("/?")[0].split(":")  # 必要部分以":"分割
        optional_part_list = link_original.split("/?")[1].split("&")  # 可选部分以"&"分割

        self.host = main_part_list[0]
        self.port = main_part_list[1]
        self.protocol = main_part_list[2]
        self.method = main_part_list[3]
        self.obfs = main_part_list[4]
        self.password = b64_url_decode(main_part_list[5]).decode("utf-8")

        d = {}  # 把可选部分输出到dict
        for item in optional_part_list:
            item_after_split = item.split('=')
            d[item_after_split[0]] = b64_url_decode(item_after_split[1]).decode("utf-8")
        # 可选部分的选项可能会变动
        # 用dict搜索关键词录入信息，默认值为空
        self.obfsparam = d.get('obfsparam', "")
        self.protoparam = d.get('protoparam', "")
        self.remarks = d.get('remarks', "")
        self.group = d.get('group', "")


def parseArg():
    if platform.system() == "Linux":  # 判断平台方便测试
        config_file = "/etc/shadowsocks-r/config.json"
    else:
        config_file = "config.json"

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--import_from", action="store", default=config_file, help="file to import server config")
    parser.add_argument("-p" , action="store_true", help="print server config")

    arg = parser.parse_args()
    srv1 = SSRSrvConf()
    if arg.import_from.startswith("ssr://"):  # 判断是链接还是配置文件
        srv1.import_from_ssr_link(arg.import_from)
    else:
        srv1.import_from_conf(arg.import_from)  # 一般在服务器上通过配置文件导入设置
    if arg.p:
        srv1.print_config()  # 打印当前服务器配置
    else:
        print(srv1.ssr_link())


if __name__ == "__main__":
    parseArg()
