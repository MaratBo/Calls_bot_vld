import datetime
import os
import requests
from datetime import timedelta
from time import sleep
from dotenv import load_dotenv
from balance import check_balance
from avangard_spb import access2, make_message


load_dotenv()
rest_money = []
calls_text = ''
calls_text_2 = ''
cabinet_1 = os.getenv("ACCESS_1")
cabinet_2 = os.getenv("ACCESS_2")
cabinet_3 = os.getenv("ACCESS_3")
cabinet_4 = os.getenv("ACCESS_4")
cabinet_5 = os.getenv("ACCESS_5")
cabinet_6 = os.getenv("ACCESS_6")
TOKEN = os.getenv("VERTIS_TOKEN")
TLG_TOKEN = os.getenv("MARUSIA_TOKEN")
which_cabinet = []


def make_message_one(name, send_data):
    global calls_text
    text = f'{name} - {send_data[0]}/{send_data[1]}'
    calls_text += f'{text}\n'


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
    global calls_text, calls_text_2
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
        if name_group != 'avangard':
            make_message_one(name, send_data)
            send_data.clear()
        else:
            text = make_message(name, send_data)
            calls_text_2 += f'{text}\n'
            send_data.clear()
    balance_info = check_balance(headers, name)  # возвращает готовый текст по балансу
    if balance_info is not None:
        rest_money.append(balance_info)


def message(sms, CHAT_ID):
    TOKEN_BOT = TLG_TOKEN  # токен Маруси
    URL = (
        'https://api.telegram.org/bot{token}/sendMessage'.format(token=TOKEN_BOT))
    data = {'chat_id': CHAT_ID,
            'text': sms
            }
    #requests.post(URL, data=data)
    print(sms)


def user(access):
    which_cabinet.append(access)
    CHAT_ID = '@calls_stat'
    CHAT_ID_AVANGARD = '@avangard_calls'
    time = datetime.date.today().strftime('%d.%m')
    for key in range(len(access)-1):
        auth(access[key], key)
    # отправляем собранный текст по звонкам
    if access[-1] == 'avtotrakt':
        message(f'Звонки за {time} (всего/пропущ.)\n'
                f'{calls_text}', CHAT_ID)
    else:
        message(f'Звонки за {time} (всего/пропущ.)\n'
                f'{calls_text_2}', CHAT_ID_AVANGARD)
    # запуск бота по балансу
    value = ''
    if len(rest_money) > 0:
        for i in rest_money:
            if i is not None:
                value += f'{i}\n'
        text = f'Балансы кабинетов:\n{value}'
        if access[-1] == 'avtotrakt':
            message(text, CHAT_ID)
            rest_money.clear()
        if access[-1] == 'avangard':
            message(text, CHAT_ID_AVANGARD)



if __name__ == '__main__':
    while True:
        access = [cabinet_1, cabinet_2, cabinet_3, cabinet_4, cabinet_5, 'avtotrakt']
        time_now = datetime.datetime.now() + timedelta(hours=3)  # смещение на американском сервере + 3ч
        h = time_now.hour
        m = time_now.minute
        print(f'check time {h}:{m}')
        if m in range(0, 30) and h == 18:
            print(f'start script {h}:{m}')
            user(access)
            which_cabinet.clear()
            user(access2)
            sleep(84600)
        else:
            sleep(1200)
