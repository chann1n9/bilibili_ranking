import requests
import json
import os
from utils.conf_reader import ConfReader


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
        url = self.API_URL + self.token + '/sendMessage'
        msg_form = {"chat_id": self.chat_id,
            "text": text,
            "parse_mode": "MarkdownV2"
            }
        r = requests.get(url, data=json.dumps(msg_form), proxies=self.proxies, headers=self.headers)
        if r.status_code != 200:
            self.sendmessage_as_text(text)

    def sendmessage_as_text(self, text):
        url = self.API_URL + self.token + '/sendMessage'
        msg_form = {"chat_id": self.chat_id,
            "text": text,
            }
        requests.get(url, data=json.dumps(msg_form), proxies=self.proxies, headers=self.headers)
        