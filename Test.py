from dotenv import load_dotenv
import os
import datetime
from pip._vendor import requests

load_dotenv()
names = []


VERTIS_TOKEN = "Vertis trailer-auto-71355e04bfd2b0456eee92b6c960a0cf92f9c1c5"
def Auth(data):
    URL = "https://apiauto.ru/1.0/auth/login"
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'x-authorization': VERTIS_TOKEN}
    r = requests.post(URL, data=data, headers=headers).json()
    print(r)
    session_id = r['session']['id']
    message(session_id)


# def Script(session_id):
#     start_time = f'{datetime.date.today()}T00:00:00.000Z'
#
#     headers = {
#         'X-Session-Id': session_id,
#         'X-Authorization': os.getenv("VERTIS_TOKEN"),
#         'Accept': 'application/json',
#     }
#
#     data = {
#         "pagination": {
#             "page": 1,
#             "page_size": 50},
#         "filter": {
#             "period":
#                 {
#                     "from": start_time
#                 }
#             },
#     }
#     add_data = [{"results": "ALL_RESULT_GROUP"}, {'results': 'MISSED_GROUP'}]
#     send_data = []
#     for i in add_data:
#         data['filter'].update(i)
#         URL = 'https://apiauto.ru/1.0/calltracking'
#         r = requests.post(URL, json=data, headers=headers).json()
#         try:
#             send_data.append(len(r['calls']))
#         except:
#             send_data.append(0)
#     if send_data[0] != 0:
#         message(send_data)
#         send_data.clear()

def message(send_data):
    time = datetime.date.today().strftime('%d.%m')
    list_cabinet = ['АвтоТракт PROБЕГ', 'АвтоТракт NISSAN']
    # text = f'{list_cabinet[names[0]]}\n' \
    #        f'Звонки за {time}\n' \
    #        f'Всего звонков - {send_data[0]}\n' \
    #        f'Пропущено - {send_data[1]}'

    token = "1058094375:AAGMLM3QLXHaHqsZFib0GLczOXpr5HI4-Yk"  # токен Маруси
    chat_id = '@calls_from_office'  # адрес канала

    URL = (
        'https://api.telegram.org/bot{token}/sendMessage'.format(token=token))
    data = {'chat_id': chat_id,
            'text': send_data
            }
    requests.post(URL, data=data)



def User():
    access = ["{'login': 'ap1it@yandex.ru', 'password': '123Testapi'}"]
    for key in range(len(access)):
        names.append(key)
        print(access[key])
        Auth(access[key])
        names.clear()



User()