import datetime
from datetime import timedelta
import requests, json
from time import sleep
import dateutil
from dateutil import parser
from dotenv import load_dotenv
import os


load_dotenv()

mark = ['','']
TOKEN = os.getenv("VERTIS_TOKEN")
headers = {'Accept': 'application/json',
           'Content-Type': 'application/json',
           'X-Authorization': TOKEN}

def login(auth_data):
    url = "https://apiauto.ru/1.0/auth/login"
    r = requests.post(url, data=auth_data, headers=headers)
    json_obj = json.loads(r.text)
    session_id = json_obj['session']['id']
    func(session_id)


# часть бота
def bot(text):
    token = os.getenv("MARUSIA_TOKEN") # токен Маруси
    chat_id = '@calls_from_office' # адрес канала

    url = ('https://api.telegram.org/bot{token}/sendMessage'.format(token=token))
    data = {'chat_id': chat_id,
            'text': text
            }
    requests.post(url, data=data)


# авторизация и работа с апи
def func(session_id):
    times = (datetime.datetime.now() - timedelta(minutes=30)).isoformat().replace(':','%3A')
    url2 = 'https://apiauto.ru/1.0/dealer/call-history?from='+str(times)+'%2B03%3A00'
    headers = {'Accept': 'application/json',
           'X-Session-Id': session_id,
           'X-Authorization': TOKEN}

    req_obj = requests.get(url2, headers=headers)
    json_resp = json.loads(req_obj.text)
    if len(json_resp['calls']) == 0:
        pass
    else:
        for i in json_resp['calls']:
            day = dateutil.parser.parse(i['timestamp']).strftime('%d.%m.%y')
            calltime = (dateutil.parser.parse(i['timestamp']) + timedelta(hours=3)).strftime('%H:%M')
            report = (day + '\n' + 'Звонок по ' + str(mark[0]) + '\n' +
                      'с номера ' + str(i['source_phone']) + '\n' +
                      'время звонка ' + calltime)
            bot(report)


def cabinet():
    acesses = ['{"login": "ap1it@yandex.ru", "password": "123Testapi"}',
                '{"login": "ap1it2@yandex.ru", "password": "123Testapi2"}']
    for auth_data in acesses:
        if auth_data == acesses[0]:
            mark[0] = 'Haval'
        else:
            mark[0] = 'Peugeot'
        #print(auth_data)
        login(auth_data)



while True:
    sleep(1800)
    cabinet()