from dotenv import load_dotenv
import os


load_dotenv()
cabinet_11 = os.getenv("ACCESS_11")
cabinet_12 = os.getenv("ACCESS_12")
cabinet_13 = os.getenv("ACCESS_13")
cabinet_14 = os.getenv("ACCESS_14")
TOKEN = os.getenv("VERTIS_TOKEN")
TLG_TOKEN = os.getenv("MARUSIA_TOKEN")

access3 = [cabinet_11, cabinet_12, cabinet_13, cabinet_14, 'petrovsky']


def make_message3(name, send_data):
    text = f'{name} - {send_data[0]}/{send_data[1]}'
    return text
