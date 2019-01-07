# SSR-Pub-Tool
小工具，帮助生成ssr订阅配置文件

我有几个服务器给亲朋友好一起用，但是服务器地址每次更换要通知他们实在是太麻烦了，还要考虑到他们的接受能力，技术水平。。。让他们订阅源，自动更新服务器是最好不过的。。。源的修改其实也不太频繁，没必要用要一个服务器来自动维护，毕竟我也不是卖号的，就写了个工具来帮助生成订阅文件。<br>
<br>
还可以批量修改服务器的group，订阅源的服务器group需要相同<br><br>

## 使用流程：
1. 在ssr服务器上运行SSRSrvConf.py读取配置文件生成SSR链接<br>
2. 复制到主机上的addr.txt内，一行一个链接<br>
3. 主机上运行SSRPubGen.py，生成订阅配置文件addr.txt<br>
4. 发布addr.txt<br><br>

## 命令行参数说明：
### SSRSrvConf.py:
usage: SSRSrvConf.py [-h] [-i IMPORT_FROM] [-p]<br><br>
-i default = /etc/shadowsocks-r/config.json<br>
#### 导入配置，生成ssr链接：<br>
SSRPubGen.py<br>
SSRPubGen.py -i config.json<br>
#### 导入并查看当前服务器配置：<br>
SSRPubGen.py -p<br><br>


### SSRPubGen.py:
usage: SSRPubGen.py [-h] [--generate] [-i INPUT_FILE] [-o OUTPUT_FILE] [-p]
                    [-s SRV_NUM] [-r REMARKS] [-g GROUP]<br><br>
-i default = addr_origin.txt<br>
-o default = public/addr.txt<br>

#### 查看所有服务器信息：<br>
SSRPubGen.py -p<br>
#### 修改1号服务器的备注为"sample_server"：
SSRPubGen.py -s 1 -r sample_server<br>
#### 修改所有服务器的分组信息为"test_group"：
SSRPubGen.py -g test_group<br>
#### 生成配置订阅文件：<br>
SSRPubGen.py<br>
SSRPubGen.py -i addr_origin.txt -o public/addr.txt<br>
SSRPubGen.py -i addr_origin.txt -g test_group --generate -o public/addr.txt<br><br>
注意：修改remarks和group的时候默认不会直接生成配置文件，除非指定--generate参数<br><br>
## addr.txt发布
可以直接把Public文件夹push到私人仓库<br>
然后使用静态页面托管服务例如netlify, coding pages发布就好了<br>
