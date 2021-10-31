from dotenv import load_dotenv
import os


load_dotenv()
cabinet_7 = os.getenv("ACCESS_7")
cabinet_8 = os.getenv("ACCESS_8")
cabinet_9 = os.getenv("ACCESS_9")
cabinet_10 = os.getenv("ACCESS_10")
TOKEN = os.getenv("VERTIS_TOKEN")
TLG_TOKEN = os.getenv("MARUSIA_TOKEN")

access2 = [cabinet_7, cabinet_8, cabinet_9, 'avangard']


def make_message(name, send_data):
    text = f'{name} - {send_data[0]}/{send_data[1]}'
    return text
