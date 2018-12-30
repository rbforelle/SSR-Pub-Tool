#!/usr/bin/python
# -*- coding:utf-8 -*-

import base64
import SSRSrvConf as SSRSrv

def gen_pub_file(origin_file,pub_file):  # 生成订阅配置文件
    with open(origin_file, 'r') as f1:
        data = f1.read()
        print("original_ssr_servers_data:")
        print(data)
        data_bytes = data.encode("utf-8")  # get str to bytes
        base64_str = base64.b64encode(data_bytes).decode("utf-8")  # encode to b64 bytes then decode to str
        print("base64_ssr_servers_data:")
        print(base64_str)

        with open(pub_file, 'w') as f2:
            f2.write(base64_str)
            f2.close()
        f1.close()

def change_group(group,origin_file,output_file):  # 批量修改ssr链接的group信息
    # 服务器自动配置的时候没有group信息
    # 多个服务器配置复制到文本文件以后
    # 可以通过这个函数统一修改group信息
    index = 1
    f_in = open(origin_file, 'r')
    lines = f_in.readlines()
    f_in.close()
    f_out = open(output_file, 'w')
    for line in lines:
        if line.startswith("ssr://"):
            print("------------- new srv",index,"-------------")
            # print(line.rstrip('\n'))
            srv = SSRSrv.SSRSrvConf()
            srv.import_from_ssr_link(line.rstrip('\n'))
            # srv.print_config()
            srv.set_group(group)
            f_out.write(srv.ssr_link())
            f_out.write("\n")
            print(srv.ssr_link())
            srv.print_config()
            index+=1
        else:
            f_out.write(line)
    f_out.close()

def print_srv_info(origin_file):  # 打印文件中的ssr链接指向的服务器信息
    index = 1
    f_in = open(origin_file, 'r')
    lines = f_in.readlines()
    f_in.close()
    for line in lines:
        if line.startswith("ssr://"):
            print("------------- srv", index, "-------------")
            # print(line.rstrip('\n'))
            srv = SSRSrv.SSRSrvConf()
            srv.import_from_ssr_link(line.rstrip('\n'))
            srv.print_config()
            index += 1

if __name__ == "__main__":
    origin_file = "addr_origin.txt"  # file to contain the original ssr server addresses
    pub_file = "public/addr.txt"  # file to publish the address

    print_srv_info(origin_file)  # 打印服务器信息
    # change_group("test_group", origin_file, origin_file)
    gen_pub_file(origin_file,pub_file)  # 生成订阅配置文件
