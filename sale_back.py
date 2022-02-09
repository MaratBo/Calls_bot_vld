import datetime

import os
import requests


TOKEN = os.getenv("VERTIS_TOKEN")
URL = 'https://apiauto.ru/1.0/comeback'
d = datetime.date.today()
sag = []


def sale_back(headers, name):
    data = {
        "pagination": {
            "page": 1,
            "page_size": 5
        },
        "filter": {
            "creation_date_from": 0,
        },
        "only_last_seller": True,

    }
    r = requests.post(URL, json=data, headers=headers).json()
    try:
        offer_created = r['comebacks'][0]['offer']['created']
        date = str(offer_created).split('T')[0]
        if date == str(d):
            mark = r['comebacks'][0]['offer']['car_info']['mark']
            model = r['comebacks'][0]['offer']['car_info']['model']
            url = r['comebacks'][0]['offer']['mobile_url']
            text = f'{name} {mark} {model}\n{url}'
            sag.append(text)
            return text
        else:
            pass
        sag.clear()
    except:
        pass
