import requests
import json
import os


class Telegram():
    def __init__(self, chat_id, token):
        super().__init__()
        def read_conf():
            with open(os.getcwd() + '/config/telegram.json') as f:
                conf = json.loads(f.read())
            return conf
        self.proxies = {
            'http': '',
            'https': ''
        }
        self.headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        self.API_URL = "https://api.telegram.org/"
        self.token = token
        self.chat_id = chat_id

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

    def sendmessage(self, text):
        url = self.API_URL + self.token + '/sendMessage'
        msg_form = {"chat_id": self.chat_id,
            "text": text,
            "parse_mode": "MarkdownV2"
            }
        requests.get(url, data=json.dumps(msg_form), proxies=self.proxies, headers=self.headers)
        