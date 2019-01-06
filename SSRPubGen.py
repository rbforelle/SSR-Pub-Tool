#!/usr/bin/python
# -*- coding:utf-8 -*-

import base64
import SSRSrvConf as SSRSrv
import argparse
import shutil
import os


def gen_pub_file(origin_file,pub_file):  # 生成订阅配置文件
    with open(origin_file, 'r') as f1:
        data = f1.read()
        print("--------intput: ", origin_file, "--------")
        print(data)
        data_bytes = data.encode("utf-8")  # get str to bytes
        base64_str = base64.b64encode(data_bytes).decode("utf-8")  # encode to b64 bytes then decode to str
        print("--------output: ", pub_file, "--------")
        print(base64_str)

        with open(pub_file, 'w') as f2:
            f2.write(base64_str)
            f2.close()
        f1.close()

def backup_file(path):
    # shutil.copyfile("old", "new")
    print("test")

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
    print("-------------------------")
    print("change group to: ", group)
    print("intput: ", origin_file)
    print("output: ", output_file)

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

def change_remarks(srv_num, remarks, origin_file, output_file):  # 修改指定服务器的备注
    index = 1
    f_in = open(origin_file, 'r')
    lines = f_in.readlines()
    f_in.close()
    f_out = open(output_file, 'w')
    for line in lines:
        if line.startswith("ssr://"):
            if index==srv_num:
                print("------------- srv", index, "-------------")
                srv = SSRSrv.SSRSrvConf()
                srv.import_from_ssr_link(line.rstrip('\n'))
                srv.set_remarks(remarks)
                srv.print_config()
                f_out.write(srv.ssr_link())
                f_out.write('\n')
            else:
                f_out.write(line)
            index += 1
        else:
            f_out.write(line)
    f_out.close()
    print("intput: ", origin_file)
    print("output: ", output_file)


def parseArg():
    parser = argparse.ArgumentParser()

    parser.add_argument("--generate", action="store_true", help="use this option to generate 'public/addr.txt' \
    when remarks or groups set at the same time")
    parser.add_argument("-i", "--input_file", action="store", default="addr_origin.txt", help="default = addr_origin.txt")
    parser.add_argument("-o", "--output_file", action="store")

    group = parser.add_argument_group("print server info")
    group.add_argument("-p", action="store_true", help="print server info")

    group2 = parser.add_argument_group("set remarks for server")
    group2.add_argument("-s", "--srv_num", action="store", type=int, help="server index to select")
    group2.add_argument("-r", "--remarks", action="store", help="remarks to set for the selected server")

    group3 = parser.add_argument_group("set groups for all servers")
    group3.add_argument("-g", "--group", action="store", help="group to set for all servers")

    arg = parser.parse_args()
    # print(arg)
    gen = False | arg.generate
    addr_origin_output = arg.output_file
    addr_origin = arg.input_file
    pub_file = "public/addr.txt"

    if arg.p:
        print_srv_info(addr_origin)  # 打印服务器信息
    elif arg.srv_num > 0:  # 如果输入了服务器号码，则为修改备注模式
        if arg.remarks is None:  # 没有输入备注，弹出提示
            parser.print_help()
        else:
            if arg.output_file is None:  # 如果没有指定输出，则直接覆盖源文件
                addr_origin_output = arg.input_file
            change_remarks(arg.srv_num, arg.remarks, addr_origin, addr_origin_output)
            addr_origin = addr_origin_output  # addr_origin的位置发生了改变
    elif arg.group is not None:  # 如果输入了group参数，则为修改group模式
        if arg.output_file is None:  # 如果没有指定输出，则直接覆盖源文件
            addr_origin_output = arg.input_file
        change_group(arg.group, addr_origin, addr_origin_output)
        addr_origin = addr_origin_output  # addr_origin的位置发生了改变
    else:
        # if no special flags is set
        gen = True
        if arg.output_file is not None:
            pub_file = arg.output_file

    if gen:
        gen_pub_file(addr_origin, pub_file)  # 生成订阅配置文件


if __name__ == "__main__":
    parseArg()
