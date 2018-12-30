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

## SSRSrvConf.py:
类SSRSrvConf保存服务器信息<br>
### self.import_from_conf(config_file)
一般在服务器上通过配置文件导入设置<br>
### self.import_from_ssr_link(example_ssr_link)
也可以通过链接导入设置<br>
### self.ssr_link()
返回ssr链接<br><br>

## SSRPubGen.py:
### gen_pub_file(origin_file,pub_file)
读取origin_file里的信息，通过base64转换成订阅配置文件<br>
origin_file里为ssr链接，一行一个，参见addr_origin_example.txt<br>
默认origin_file=addr_origin.txt, pub_file=public/addr.txt 已经添加到.gitignore里保证个人服务器信息不会一起commit<br>

### change_group(group,origin_file,output_file):
批量修改origin_file里的ssr链接的group参数<br><br>

## addr.txt发布
可以直接把Public文件夹push到私人仓库<br>
然后使用静态页面托管服务例如netlify, coding pages发布就好了<br>
