import requests
import json
import urllib.parse
import time
import textwrap
from time import sleep

TOKEN = 'TOKEN'
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

#TELEGRAM BOT FUNCTIONS


class MessageResponse(object):
    def __init__(self, data):
        self.__dict__ = json.loads(data)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    #print (url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def get_last_chat_id_and_text(updates):
    try:
        num_updates = len(updates["result"])
    except:
        num_updates = 1
    last_update = num_updates - 1
    try:
        text = updates["result"][last_update]["message"]["text"]
    except:
        text = ""
    #print(updates)
    try:
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    except:
        chat_id = ""
    try:
        person_id = updates["result"][last_update]["message"]["from"]["id"]
    except:
        person_id = ""
    return (text, chat_id, person_id)


def send_message_markdown(text, chat_id):
    textparsed = urllib.parse.quote_plus(text)
    textparsed = textparsed.replace("-","\-")
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=MarkdownV2".format(textparsed, chat_id)
    #content = get_url(url)
    print(get_json_from_url(url))
    return text


def send_message(text, chat_id):
    textparsed = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(textparsed, chat_id)
    content = get_url(url)
    response = MessageResponse(content)
    message_id = response.result.get('message_id')
    return text, message_id

'''
Break a very long msg by sending it as separate msg,
this is because telgram has a limit on the length of the message text
'''
def send_long_message(text, chat_id):
    textparsed = urllib.parse.quote_plus(text)
    lines = textwrap.wrap(textparsed, 3500, break_long_words=False)
    for line in lines:
        url = URL + "sendMessage?text={}&chat_id={}".format(line, chat_id)
        get_url(url)
        sleep(1)
    return text


def send_silent_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&disable_notification={}".format(text, chat_id, True)
    get_url(url)


def send_photo(photo,chat_id):
    url = URL + "sendPhoto?chat_id={}&photo={}".format(chat_id,photo)
    #print(url)
    get_url(url)
    return photo


def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)


def send_message_html(text, chat_id):
    textparsed = urllib.parse.quote_plus(text)
    print(textparsed)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=HTML".format(textparsed, chat_id)
    #content = get_url(url)
    print(get_json_from_url(url))
    return text



