import os
from dotenv import load_dotenv
from pip._vendor import requests

load_dotenv()
def test():
    headers = {
        'X-Session-Id': '56001158|1624048375111.7776000.yEPbhcVhz7ange5FnoS2Ug.Co7AcruCNjriZgUSd0LdMRXhZL4g2ZHKTRLFtqAjSsU',
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
                    "from": "2021-06-18T00:00:00.000Z",
                    # "from": "2021-06-12T09:00:00.000Z",

                    "to": "2021-06-18T19:00:00.000Z"
                }
        },
    }

    URL = 'https://apiauto.ru/1.0/calltracking'
    r = requests.post(URL, json=data, headers=headers).json()
    print(r)

test()