from datetime import datetime as dt

DOC_LINK_ID = {
    'Zeut': ['6f2ffb58-b985-436c-a3f7-f5913299fa30', 'Zeut'],
    'Maavar': ['36aac445-7d4d-4088-baa2-43658d2ca803', 'Maavar'],
}

USERS_DATA = {
    'Kirill': ['0553161687', '347812679'], # exemple 'Ivan': ['055xxxxxxx', 'TZ number'],
    'Nina': ['0559578701', '347812687']
}

Person = 'Nina'
DOC = 'Maavar'
DOC_CHOOZE = DOC_LINK_ID[DOC][0]  # Appointment document chooze
MY_TEL = USERS_DATA[Person][0]  # Telephone number
MY_TZ = USERS_DATA[Person][1]  # Teudat Zeut number
MAX_DATA = dt(2023, 5, 25, 0, 0, 0)
MAIN_URL = 'https://myvisit.com/#!/home/signin/'
TIMEOUT = 120  # Seconds
INTERVAL = 120  # Minuts between slot and current time

Cities = {
    # 'Hadera': 'https://myvisit.com/#!/home/service/2144',
    'Sderot': 'https://myvisit.com/#!/home/service/3078',
    'Netanya': 'https://myvisit.com/#!/home/service/2146',
    'Tayba': 'https://myvisit.com/#!/home/service/2749',
    'Kphar-Saba': 'https://myvisit.com/#!/home/service/2110',
    'Gertsliya': 'https://myvisit.com/#!/home/service/2245',
    'Petakh-Tikva': 'https://myvisit.com/#!/home/service/2113',
    'Bney-Brak': 'https://myvisit.com/#!/home/service/2163',
    'Rosh-Ha-Ain': 'https://myvisit.com/#!/home/service/2167',
    # 'RAmat-Gan-Givataim': 'https://myvisit.com/#!/home/service/2097',
    'Tel-Aviv': 'https://myvisit.com/#!/home/service/2099',
    'Yaffo': 'https://myvisit.com/#!/home/service/2165',
    'Um-El-Fahm': 'https://myvisit.com/#!/home/service/8977',
    'Holon': 'https://myvisit.com/#!/home/service/2153',
    'Rishon-Le-Tsion': 'https://myvisit.com/#!/home/service/2241',
    'Hayfa': 'https://myvisit.com/#!/home/service/2219',
}
