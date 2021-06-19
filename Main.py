import datetime
from time import sleep

from dotenv import load_dotenv
import os

from pip._vendor import requests

load_dotenv()
names = []

def Auth(data):
    URL = "https://apiauto.ru/1.0/auth/login"
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'x-authorization': os.getenv("VERTIS_TOKEN")}
    r = requests.post(URL, data=data, headers=headers).json()
    session_id = r['session']['id']
    Script(session_id)


def Script(session_id):
    start_time = f'{datetime.date.today()}T00:00:00.000Z'

    headers = {
        'X-Session-Id': session_id,
        'X-Authorization': os.getenv("VERTIS_TOKEN"),
        'Accept': 'application/json',
    }

    data = {
        "pagination": {
            "page": 1,
            "page_size": 50},
        "filter": {
            "period":
                {
                    "from": start_time
                }
            },
    }
    add_data = [{"results": "ALL_RESULT_GROUP"}, {'results': 'MISSED_GROUP'}]
    send_data = []
    for i in add_data:
        data['filter'].update(i)
        URL = 'https://apiauto.ru/1.0/calltracking'
        r = requests.post(URL, json=data, headers=headers).json()
        try:
            send_data.append(len(r['calls']))
        except:
            send_data.append(0)
    if send_data[0] == 0:
        message(send_data)
        send_data.clear()

def message(send_data):
    time = datetime.date.today().strftime('%d.%m')
    list_cabinet = ['АвтоТракт PROБЕГ', 'АвтоТракт NISSAN']
    text = f'{list_cabinet[names[0]]}\n' \
           f'Звонки за {time}\n' \
           f'Всего звонков - {send_data[0]}\n' \
           f'Пропущено - {send_data[1]}'

    token = os.getenv("MARUSIA_TOKEN")  # токен Маруси
    chat_id = '@calls_from_office'  # адрес канала

    URL = (
        'https://api.telegram.org/bot{token}/sendMessage'.format(token=token))
    data = {'chat_id': chat_id,
            'text': text
            }
    requests.post(URL, data=data)


def User():
    access = [os.getenv("ACCESS_1"), os.getenv("ACCESS_2")]
    for key in range(len(access)):
        names.append(key)
        Auth(access[key])
        names.clear()

if __name__ == '__main__':
    while True:
        User()
        sleep(673200)
