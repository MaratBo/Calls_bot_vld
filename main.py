import datetime
import calendar
from datetime import timedelta
from time import sleep

from dotenv import load_dotenv
import os
import requests
from balance import check_balance



load_dotenv()
rest_money = []
names = []
calls_text = ''
cabinet_1 = os.getenv("ACCESS_1")
cabinet_2 = os.getenv("ACCESS_2")
cabinet_3 = os.getenv("ACCESS_3")
cabinet_4 = os.getenv("ACCESS_4")
cabinet_5 = os.getenv("ACCESS_5")
cabinet_6 = os.getenv("ACCESS_6")
TOKEN = os.getenv("VERTIS_TOKEN")
TLG_TOKEN = os.getenv("MARUSIA_TOKEN")


def auth(data):
    URL = "https://apiauto.ru/1.0/auth/login"
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'x-authorization': TOKEN}
    r = requests.post(URL, data=data, headers=headers).json()
    session_id = r['session']['id']
    script(session_id)


def script(session_id):  # возвращает список принятых и пропущ звонков
    start_time = f'{datetime.date.today()}T00:00:00.000Z'
    global calls_text
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
            unic_calls = set((map(lambda x: x['source']['raw'], r['calls'])))
            send_data.append(len(unic_calls))
        except:
            send_data.append(0)
    if send_data[0] != 0:
        LIST_CABINET = ['PROБЕГ', 'NISSAN', 'Peugeot/Ford', 'Chevrolet', 'Lada', 'МБ']
        text = f'{LIST_CABINET[names[0]]} - ' \
               f'{send_data[0]}/{send_data[1]}'
        calls_text += f'{text}\n'
        send_data.clear()
    balance_info = check_balance(headers, names)  # возвращает готовый текст по балансу
    if balance_info is not None:
        rest_money.append(balance_info)


def message(sms):
    TOKEN_BOT = TLG_TOKEN  # токен Маруси
    CHAT_ID = '@calls_stat'  # адрес канала

    URL = (
        'https://api.telegram.org/bot{token}/sendMessage'.format(token=TOKEN_BOT))
    data = {'chat_id': CHAT_ID,
            'text': sms
            }
    requests.post(URL, data=data)


def user():
    time = datetime.date.today().strftime('%d.%m')
    access = [cabinet_1, cabinet_2, cabinet_3, cabinet_4, cabinet_5, cabinet_6]
    for key in range(len(access)):
        names.append(key)  # запись ключей по порядку 1-5, потом удаляет.
        auth(access[key])
        names.clear()
    # отправляем собранный текст по звонкам
    message(f'Звонки за {time} (всего/пропущ.)\n'
            f'{calls_text}')
    # тут запуск бота по балансу
    value = ''
    if len(rest_money) > 0:
        for i in rest_money:
            if i is not None:
                value += f'{i}\n'
        text = f'Балансы кабинетов:\n{value}'
        message(text)


if __name__ == '__main__':
    while True:
        date = datetime.date.today()
        day_name = calendar.day_name[date.weekday()]
        time_now = datetime.datetime.now() + timedelta(hours=3) # смещение на американском сервере + 3ч
        h = time_now.hour
        m = time_now.minute
        print(f'check time {h}:{m}')
        if day_name != 'Saturday' and day_name != 'Sunday' and m in range(10, 30) and h == 18:
            print(f'start script {h}:{m}')
            user()
            sleep(84600)
        else:
            sleep(1200)
