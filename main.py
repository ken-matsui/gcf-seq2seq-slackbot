# coding: utf-8

import json
import logging

from plugins.app import default_func


class Message(object):
    """Slackのメッセージクラス"""
    token = ""
    team_id = ""
    channel_id = ""  # 投稿されたチャンネルID
    channel_name = ""  # チャンネル名
    timestamp = 0
    user_id = ""
    user_name = ""  # 投稿ユーザー名
    text = ""  # 投稿内容
    trigger_word = ""  # OutgoingWebhooksに設定したトリガー

    def __init__(self, params):
        self.team_id = params["team_id"]
        self.channel_id = params["channel_id"]
        self.channel_name = params["channel_name"]
        self.timestamp = params["timestamp"]
        self.user_id = params["user_id"]
        self.user_name = params["user_name"]
        self.text = params["text"]
        self.trigger_word = params["trigger_word"]

    def __str__(self):
        res = self.__class__.__name__
        res += "@{0.token}[channel={0.channel_name}, user={0.user_name}, text={0.text}]".format(self)
        return res


def _say(text):
    """Slackの形式でJSONを返す"""
    return json.load({
        "text": "response: " + text,  # 投稿する内容
        "username": "mybot",  # bot名
        "icon_emoji": "",  # botのiconを絵文字の中から指定
    })


def main(request):
    msg = Message(request.form)
    print(str(msg))

    # query = request.body["text"]
    return _say(default_func(request))
