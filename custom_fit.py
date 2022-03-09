import requests
import datetime


month = datetime.date.today().strftime('%Y-%m')
start_month = f'{month}-01T00:00:00.000Z'


def artem_eremin(headers):
    data = {
        "pagination": {
            "page": 1,
            "page_size": 1000},
        "filter": {
            "period":
                {
                    "from": start_month,

                },
            "results": "ALL_RESULT_GROUP"
        },
    }

    stat_all_month = []
    URL = 'https://apiauto.ru/1.0/calltracking'
    r = requests.post(URL, json=data, headers=headers).json()
    try:
        unic_calls = set((map(lambda x: x['source']['raw'], r['calls'])))
        stat_all_month.append(len(unic_calls))
    except:
        stat_all_month.append(0)
    return f'Уникальных звонков за месяц-{stat_all_month[0]}'
