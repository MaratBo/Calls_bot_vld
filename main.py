import datetime
from datetime import timedelta
from time import sleep
from customers import accesses, make_message
from dotenv import load_dotenv
import os
import requests

from balance import check_balance
from sale_back import sale_back
from custom_fit import artem_eremin


load_dotenv()
rest_money = []
my_ex = []
which_cabinet = []
calls_text = ''
TOKEN = os.getenv("VERTIS_TOKEN")
TLG_TOKEN = os.getenv("MARUSIA_TOKEN")
flag = []
dealer_name = []
target_calls = ''
custom_message = ''


def auth(data: dict, key: int):
    URL = "https://apiauto.ru/1.0/auth/login"
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'x-authorization': TOKEN}
    r = requests.post(URL, data=data, headers=headers).json()
    try:
        session_id = r['session']['id']
        script(session_id, key)
    except:
        print(f"{data} not access")
        pass


def script(session_id: str, key: int):  # возвращает список принятых и пропущ звонков
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
                    "from": start_time,
                }
        },
    }
    global target_calls
    if dealer_name[0] in ['avangard', 'petrovsky', 'm2o', 'axis']:
        target_calls = 'уникальные/целевые'
        ADD_DATA = [{"targets": "ALL_TARGET_GROUP"}, {"targets": "TARGET_GROUP"}]
    else:
        target_calls = 'уникальные/пропущенные'
        ADD_DATA = [{"results": "ALL_RESULT_GROUP"}, {'results': 'MISSED_GROUP'}]
    global send_data
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
        flag.append(True)
    else:
        flag.append(None)

    if dealer_name[0] in ['geely_planeta', 'planeta_used', 'chery_planeta', 'skoda_planeta']:
        global custom_message
        custom_message = artem_eremin(headers)
    else: pass

    balance_info = check_balance(headers, name)  # возвращает готовый текст по балансу
    if balance_info is not None:
        rest_money.append(balance_info)

    sale_again = sale_back(headers, name)  # снова в продаже
    if sale_again is not None:
        my_ex.append(sale_again)


def message(sms, CHAT_ID):
    URL = (
        'https://api.telegram.org/bot{token}/sendMessage'.format(token=TLG_TOKEN))
    data = {'chat_id': CHAT_ID,
            'text': sms
            }
    requests.post(URL, data=data)
    flag.clear()


def user(access):
    which_cabinet.append(access)
    time = datetime.date.today().strftime('%d.%m')
    dealer_name.append(access[-1])
    for key in range(len(access) - 2):
        auth(access[key], key)
    # отправляем собранный текст по звонкам
    if True in flag:
        CHAT_ID = access[-2]
        message(f'Звонки за {time} {target_calls}\n'
                f'{calls_text}', CHAT_ID)
        if custom_message:
            message(custom_message, CHAT_ID)
        else: pass
    else:
        print(f'{access[-1]} - not calls')
    dealer_name.clear()

    ''' тут запуск бота по балансу'''
    value = ''
    if len(rest_money) > 0:
        for i in rest_money:
            if i is not None:
                value += f'{i}\n'
        text = f'Балансы кабинетов:\n{value}'
        if access[-1] == 'avtotrakt':
            CHAT_ID = '@calls_stat'
            text = f'{text} @Danil_Bashkin'
            message(text, CHAT_ID)
            rest_money.clear()
        else:
            CHAT_ID = access[-2]
            message(text, CHAT_ID)
            rest_money.clear()

    values = ''
    if len(my_ex) > 0:
        for i in my_ex:
            if i is not None:
                values += f'{i}\n'
            text = f'Ваш автомобиль снова в продаже:\n{values}'
            CHAT_ID = access[-2]
            message(text, CHAT_ID)
            my_ex.clear()
    which_cabinet.clear()


if __name__ == '__main__':
    while True:
        time_now = datetime.datetime.now() + timedelta(hours=3)  # смещение на американском сервере + 3ч
        h = time_now.hour
        m = time_now.minute
        d = time_now.date().strftime("%d")
        print(f'check time {h}:{m}')
        if m in range(0, 30) and h == 18:
            print(f'start script {d}-{h}:{m}')
            for i in accesses:
                user(i)
                which_cabinet.clear()
            sleep(84600)
        else:
            sleep(1200)
