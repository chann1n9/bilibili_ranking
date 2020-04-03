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

#### 关于开发分支的使用

开发分支很多功能写得很粗糙留下很多坑要填

主要实现：

1. 向telegram发送数据

2. 定时爬取数据并声称csv

使用：`python brk.py run`

**注意：请自行修各项配置, 例如代理配置和telegram的channle id 和 token**

debug file in vscode:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: brk.py run",
            "type": "python",
            "request": "launch",
            "program": "brk.py",
            "console": "integratedTerminal",
            "args": ["run"]
        },
        {
            "name": "Python: 当前文件",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        },
        {
            "name": "Python: brk.py",
            "type": "python",
            "request": "launch",
            "program": "brk.py",
            "console": "integratedTerminal"
        }
    ]
}
```
##### 开发新功能
1. 将新功能代码开发在plugings目录下
2. 新的apscheduler的job放在job_master.py的Jobs类里
3. job_master.JobMaster.load_jobs中规定任务的时间参数
