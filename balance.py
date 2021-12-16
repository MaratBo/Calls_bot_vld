import requests


URL = 'https://apiauto.ru/1.0/dealer/account'


def check_balance(headers, name):
    """первый пуш менее 7 дней, второй 5 дней, третий если один день"""
    r = requests.get(URL, headers=headers).json()
    try:
        days_to_empty = r['rest_days']
        if days_to_empty in [1, 5, 7, 8]:
            text = f'{name}\nденьги закончатся через {days_to_empty} дн.'
            return text
    except:
        pass
