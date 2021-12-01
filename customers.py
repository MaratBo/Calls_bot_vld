from dotenv import load_dotenv
import os


load_dotenv()

#avtotrakt
cabinet_1 = os.getenv("ACCESS_1")
cabinet_2 = os.getenv("ACCESS_2")
cabinet_3 = os.getenv("ACCESS_3")
cabinet_4 = os.getenv("ACCESS_4")
cabinet_5 = os.getenv("ACCESS_5")
cabinet_6 = os.getenv("ACCESS_6")
#avangard
cabinet_7 = os.getenv("ACCESS_7")
cabinet_8 = os.getenv("ACCESS_8")
cabinet_9 = os.getenv("ACCESS_9")
cabinet_10 = os.getenv("ACCESS_10")
#petrovsky
cabinet_11 = os.getenv("ACCESS_11")
cabinet_12 = os.getenv("ACCESS_12")
cabinet_13 = os.getenv("ACCESS_13")
cabinet_14 = os.getenv("ACCESS_14")
#M2O
cabinet_15 = os.getenv('ACCESS_15')
cabinet_16 = os.getenv('ACCESS_16')

access = [cabinet_1, cabinet_2, cabinet_3, cabinet_4, cabinet_5, 'avtotrakt']
access2 = [cabinet_7, cabinet_8, cabinet_9, cabinet_10, 'avangard']
access3 = [cabinet_11, cabinet_12, cabinet_13, cabinet_14, 'petrovsky']
access4 = [cabinet_15, cabinet_16,'m2o']

test_list_trakt = []
test_list_av = []
test_list_petr = []
test_list_m2o = []

def make_message(name_group, name, send_data):
    text = f'{name} - {send_data[0]}/{send_data[1]}'
    if name_group == 'avangard':
        test_list_av.append(text)
        return test_list_av
    elif name_group == 'avtotrakt':
        test_list_trakt.append(text)
        return test_list_trakt
    elif name_group == 'petrovsky':
        test_list_petr.append(text)
        return test_list_petr
    elif name_group == 'm2o':
        test_list_m2o.append(text)
        return test_list_m2o
