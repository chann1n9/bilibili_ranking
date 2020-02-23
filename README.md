# bilibili_ranking

#### 介绍
此脚本为爬取bilibili排行榜的新视频，旧的排行榜内容为上一次运行此脚本时生成


#### 安装教程

1. 请使用python3.6及以上
2. 请输入以下命令安装依赖包：

`pip3 install -r requirements.txt`

若丢失requirements.txt文件或想单独安装：

`pip3 install requests`

`pip3 install lxml`

`pip3 install cssselect`


【注意】如果有使用sock5的需求请讲第一条命令改为：
`pip3 install requests[socks]`


#### 使用说明

请填写下面变量：

file_path 此变量为脚本生成文件保存路径 【默认】：脚本运行目录

proxies 代理地址，如果过于频繁使用此脚本被b站封ip，请使用代理  【默认】：空

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request

