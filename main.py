import datetime
import calendar
from datetime import timedelta
from time import sleep
from customers import access, access2, access3, access4, make_message
from dotenv import load_dotenv
import os
import requests

from balance import check_balance

load_dotenv()
rest_money = []
which_cabinet = []
test_list_trakt = []
test_list_av = []
test_list_petr = []
calls_text = ''
TOKEN = os.getenv("VERTIS_TOKEN")
TLG_TOKEN = os.getenv("MARUSIA_TOKEN")


def auth(data, key):
    URL = "https://apiauto.ru/1.0/auth/login"
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'x-authorization': TOKEN}
    r = requests.post(URL, data=data, headers=headers).json()
    try:
        session_id = r['session']['id']
        script(session_id, key)
    except:
        pass


def script(session_id, key):  # возвращает список принятых и пропущ звонков
    name_group = which_cabinet[0][-1]
    name = which_cabinet[0][key].split("'")[-2]
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
            unic_calls = set((map(lambda x: x['source']['raw'], r['calls'])))
            send_data.append(len(unic_calls))
        except:
            send_data.append(0)
    global calls_text
    if send_data[0] != 0:
        text = make_message(name_group, name, send_data)
        calls_text = '\n'.join(text)
        send_data.clear()
    balance_info = check_balance(headers, name)  # возвращает готовый текст по балансу
    if balance_info is not None:
        rest_money.append(balance_info)


def message(sms, CHAT_ID):
    URL = (
        'https://api.telegram.org/bot{token}/sendMessage'.format(token=TLG_TOKEN))
    data = {'chat_id': CHAT_ID,
            'text': sms
            }
    requests.post(URL, data=data)


def user(access):
    which_cabinet.append(access)
    time = datetime.date.today().strftime('%d.%m')
    for key in range(len(access)-1):
        auth(access[key], key)
    # отправляем собранный текст по звонкам
    if access[-1] == 'avtotrakt':
        CHAT_ID = "@calls_stat"
    elif access[-1] == 'avangard':
        CHAT_ID = '@avangard_calls'
    elif access[-1] == 'm2o':
        CHAT_ID = '@m2o_autoru'
    else:
        CHAT_ID = "@petrovsky_calls"
    message(f'Звонки за {time} (всего/пропущ.)\n'
            f'{calls_text}', CHAT_ID)

    # тут запуск бота по балансу
    value = ''
    if len(rest_money) > 0:
        for i in rest_money:
            if i is not None:
                value += f'{i}\n'
        text = f'Балансы кабинетов:\n{value}'
        if access[-1] == 'avtotrakt':
            CHAT_ID = '@calls_stat'
            message(text, CHAT_ID)
            rest_money.clear()
        elif access[-1] == 'avangard':
            CHAT_ID = '@avangard_calls'
            message(text, CHAT_ID)
            rest_money.clear()
        elif access[-1] == 'petrovsky':
            CHAT_ID = '@petrovsky_calls'
            message(text, CHAT_ID)
            rest_money.clear()
        elif access[-1] == 'm2o':
            CHAT_ID = '@m2o_autoru'
            message(text, CHAT_ID)
            rest_money.clear()
    which_cabinet.clear()


if __name__ == '__main__':
    while True:
        time_now = datetime.datetime.now() + timedelta(hours=3)  # смещение на американском сервере + 3ч
        h = time_now.hour
        m = time_now.minute
        d = time_now.date().strftime("%d")
        print(f'check time {h}:{m}')
        if m in range(0, 41) and h == 21:
            print(f'start script {d}-{h}:{m}')
            user(access)
            which_cabinet.clear()
            user(access2)
            which_cabinet.clear()
            user(access3)
            which_cabinet.clear()
            user(access4)
            which_cabinet.clear()
            sleep(84600)
        else:
            sleep(1200)
