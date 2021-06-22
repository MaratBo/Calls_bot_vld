import datetime
from time import sleep

from dotenv import load_dotenv
import os

from pip._vendor import requests


load_dotenv()
names = []
cabinet_1 = os.getenv("ACCESS_1")
cabinet_2 = os.getenv("ACCESS_2")
TOKEN = os.getenv("VERTIS_TOKEN")
TLG_TOKEN = os.getenv("MARUSIA_TOKEN")


def auth(data):
    URL = "https://apiauto.ru/1.0/auth/login"
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'x-authorization': TOKEN}
    r = requests.post(URL, data=data, headers=headers).json()
    print(r)
    session_id = r['session']['id']
    script(session_id)


def script(session_id):
    start_time = f'{datetime.date.today()}T00:00:00.000Z'

    headers = {
        'X-Session-Id': session_id,
        'X-Authorization': TOKEN,
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
    ADD_DATA = [{"results": "ALL_RESULT_GROUP"}, {'results': 'MISSED_GROUP'}]
    send_data = []
    for i in ADD_DATA:
        data['filter'].update(i)
        URL = 'https://apiauto.ru/1.0/calltracking'
        r = requests.post(URL, json=data, headers=headers).json()
        try:
            send_data.append(len(r['calls']))
        except:
            send_data.append(0)
    if send_data[0] != 0:
        message(send_data)
        send_data.clear()

def message(send_data):
    time = datetime.date.today().strftime('%d.%m')
    LIST_CABINET = ['АвтоТракт PROБЕГ', 'АвтоТракт NISSAN']
    text = f'{LIST_CABINET[names[0]]}\n' \
           f'Звонки за {time}\n' \
           f'Всего звонков - {send_data[0]}\n' \
           f'Пропущено - {send_data[1]}'

    TOKEN_BOT = TLG_TOKEN  # токен Маруси
    CHAT_ID = '@calls_stat'  # адрес канала

    URL = (
        'https://api.telegram.org/bot{token}/sendMessage'.format(token=TOKEN_BOT))
    data = {'chat_id': CHAT_ID,
            'text': text
            }
    requests.post(URL, data=data)


def user():
    access = [cabinet_1, cabinet_2]
    for key in range(len(access)):
        names.append(key)
        auth(access[key])
        names.clear()


if __name__ == '__main__':
    while True:
        user()
        sleep(86400)
