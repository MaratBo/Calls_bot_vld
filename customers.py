from dotenv import load_dotenv
import os


load_dotenv()

#avtotrakt
cabinet_1 = os.getenv("ACCESS_1")
cabinet_2 = os.getenv("ACCESS_2")
cabinet_3 = os.getenv("ACCESS_3")
cabinet_4 = os.getenv("ACCESS_4")
cabinet_5 = os.getenv("ACCESS_5")
#avtoforum_krs
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
#axis
cabinet_17 = os.getenv('ACCESS_17')
#July
cabinet_18 = os.getenv('ACCESS_18')
cabinet_19 = os.getenv('ACCESS_19')
cabinet_20 = os.getenv('ACCESS_20')
cabinet_21 = os.getenv('ACCESS_21')
#мельников никита
cabinet_22 = os.getenv('ACCESS_22')
cabinet_23 = os.getenv('ACCESS_23')
cabinet_24 = os.getenv('ACCESS_24')
#еремин егор
cabinet_25 = os.getenv('ACCESS_25')
cabinet_26 = os.getenv('ACCESS_26')
cabinet_27 = os.getenv('ACCESS_27')

#гурина саша
cabinet_28 = os.getenv('ACCESS_28')
cabinet_29 = os.getenv('ACCESS_29')


access = [cabinet_1, cabinet_2, cabinet_3, cabinet_4, cabinet_5, "@calls_stat", 'avtotrakt']
access2 = [cabinet_7, cabinet_8, cabinet_9, cabinet_10, '@avangard_calls', 'avangard']
access3 = [cabinet_11, cabinet_12, cabinet_13, cabinet_14, '@petrovsky_calls', 'petrovsky']
access4 = [cabinet_15, cabinet_16, '@m2o_autoru', 'm2o']
access5 = [cabinet_17, '@axis_bets', 'axis']
access6 = [cabinet_6, '@avtoforum_krs', 'avtorum']
access7 = [cabinet_22, cabinet_23, '@reginas_autoru', 'chelyabinsk']
access8 = [cabinet_18, cabinet_19, cabinet_20, cabinet_21, '@july_autoru', 'july']
access9 = [cabinet_24, '@chl_autoru', 'mias']
access10 = [cabinet_25, '@skoda_planeta', 'skoda_planeta']
access11 = [cabinet_26, '@planeta_auto_ug', 'geely_planeta']
access12 = [cabinet_27, '@planetaugprobeg', 'planeta_used']
access13 = [cabinet_28, '@autopartnertmn', 'partner_auto']
access14 = [cabinet_29, '@agradtmn', 'avtograd']

accesses = [access, access2, access3, access4, access5, access6, access7, access8, access9, access10, access11,
            access12, access13, access14]

test_list_trakt = []
test_list_av = []
test_list_petr = []
test_list_m2o = []
test_list_axis = []
test_list_avtorum = []
test_list_july = []
test_list_chl = []
test_list_mias = []
test_list_skoda_planeta = []
test_list_geely_planeta = []
test_list_used_planeta = []
test_list_partner_auto = []
test_list_avtograd = []


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
    elif name_group == 'axis':
        test_list_axis.append(text)
        return test_list_axis
    elif name_group == 'avtorum':
        test_list_avtorum.append(text)
        return test_list_avtorum
    elif name_group == 'chelyabinsk':
        test_list_chl.append(text)
        return test_list_chl
    elif name_group == 'july':
        test_list_july.append(text)
        return test_list_july
    elif name_group == 'mias':
        test_list_mias.append(text)
        return test_list_mias
    elif name_group == 'skoda_planeta':
        test_list_skoda_planeta.append(text)
        return test_list_skoda_planeta
    elif name_group == 'geely_planeta':
        test_list_geely_planeta.append(text)
        return test_list_geely_planeta
    elif name_group == 'planeta_used':
        test_list_used_planeta.append(text)
        return test_list_used_planeta
    elif name_group == 'partner_auto':
        test_list_partner_auto.append(text)
        return test_list_partner_auto
    elif name_group == 'avtograd':
        test_list_avtograd.append(text)
        return test_list_avtograd
