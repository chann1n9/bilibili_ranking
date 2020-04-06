import requests
import json
import os
import re
from utils.conf_reader import ConfReader
from requests.exceptions import ProxyError
from utils.logger import Logger


LOG = Logger(__name__)
logger = LOG.get_logger()

class Telegram():
    def __init__(self, chat_id, token):
        super().__init__()

        self.conf = ConfReader(os.getcwd() + '/config/telegram.json').get_conf_as_dict()
        proxies = self.conf['proxies']
        self.proxies = {
            'http': proxies,
            'https': proxies
        }
        self.headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        self.API_URL = "https://api.telegram.org/"
        class TGMethod:
            sendMessage = '/sendMessage'
            getUpdates = '/getUpdates'
        self.method = TGMethod()
        if chat_id and token:
            self.token = token
            self.chat_id = chat_id
        else:
            self.token = self.conf['token']
            self.chat_id = self.conf['chat_id']

    '''
    Markdownv2 Sample

    *bold \*text*
    _italic \*text_
    __underline__
    ~strikethrough~
    *bold _italic bold ~italic bold strikethrough~ __underline italic bold___ bold*
    [inline URL](http://www.example.com/)
    [inline mention of a user](tg://user?id=123456789)
    `inline fixed-width code`
    ```
    pre-formatted fixed-width code block
    ```
    ```python
    pre-formatted fixed-width code block written in the Python programming language
    ```
    '''
    def sendmessage_as_markdown(self, text):
        url = self.API_URL + self.token + self.method.sendMessage
        msg_form = {"chat_id": self.chat_id,
            "text": text,
            "parse_mode": "MarkdownV2"
            }
        requests.get(url, data=json.dumps(msg_form), proxies=self.proxies, headers=self.headers)

    def sendmessage_as_text(self, text):
        url = self.API_URL + self.token + self.method.sendMessage
        msg_form = {"chat_id": self.chat_id,
            "text": text,
            }
        requests.get(url, data=json.dumps(msg_form), proxies=self.proxies, headers=self.headers)

    '''
    HTML Sample

    <b>bold</b>, <strong>bold</strong>
    <i>italic</i>, <em>italic</em>
    <u>underline</u>, <ins>underline</ins>
    <s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>
    <b>bold <i>italic bold <s>italic bold strikethrough</s> <u>underline italic bold</u></i> bold</b>
    <a href="http://www.example.com/">inline URL</a>
    <a href="tg://user?id=123456789">inline mention of a user</a>
    <code>inline fixed-width code</code>
    <pre>pre-formatted fixed-width code block</pre>
    <pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>
    '''
    def sendmessage_as_html(self, text):
        url = self.API_URL + self.token + self.method.sendMessage
        msg_form = {"chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML"
            }
        requests.get(url, data=json.dumps(msg_form), proxies=self.proxies, headers=self.headers)

    def get_updates(self):
        url = self.API_URL + self.token + self.method.getUpdates
        try:
            r = requests.get(url, proxies=self.proxies, headers=self.headers)
        except ProxyError as e:
            logger.warning('telegram代理设置错误 Proxy is {}'.format(self.proxies))
            return e
        return r

        