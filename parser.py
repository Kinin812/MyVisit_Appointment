import datetime
from random import randint
from time import sleep
from datetime import datetime as dt
from dateutil.parser import parse as ps
from bot import send_message
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

DOC_LINK_ID = {
    'Zeut': '6f2ffb58-b985-436c-a3f7-f5913299fa30',
    'Maavar': '36aac445-7d4d-4088-baa2-43658d2ca803',
}
DOC_CHOOZE = DOC_LINK_ID['Zeut']
MY_TEL = '0553161687'
MY_TZ = '347812679'
MAX_DATA = datetime.datetime(2023, 9, 30, 0, 0, 0)
MAIN_URL = 'https://myvisit.com/#!/home/signin/'
TIMEOUT = 300
INTERVAL = 120  # minuts

Cities = [
    {'Test': 'https://www.myvisit.com/#!/home/service/2247'},
    # {'Hadera': 'https://myvisit.com/#!/home/service/2144'},
    # {'Netanya': 'https://myvisit.com/#!/home/service/2146'},
    # {'Tayba': 'https://myvisit.com/#!/home/service/2749'},
    # {'Kphar-Saba': 'https://myvisit.com/#!/home/service/2110'},
    # {'Gertsliya': 'https://myvisit.com/#!/home/service/2245'},
    # {'Petakh-Tikva': 'https://myvisit.com/#!/home/service/2113'},
    # {'Bney-Brak': 'https://myvisit.com/#!/home/service/2163'},
    #     {'Rosh-Ha-Ain': 'https://myvisit.com/#!/home/service/2167'},
    #     {'RAmat-Gan-Givataim': 'https://myvisit.com/#!/home/service/2097'},
    #     {'Tel-Aviv': 'https://myvisit.com/#!/home/service/2099'},
    #     {'Yaffo': 'https://myvisit.com/#!/home/service/2165'},
    #     {'Um-El-Fahm': 'https://myvisit.com/#!/home/service/8977'},
    #     {'Holon': 'https://myvisit.com/#!/home/service/2153'},
    #     {'Rishon-Le-Tsion': 'https://myvisit.com/#!/home/service/2241'},
]


def delay():
    sleep(randint(5, 7))


class City:
    def __init__(self, driver, name, url):
        self.date_clean_without_time = None
        self.diff_minuts = None
        self.driver = driver
        self.name = name
        self.date_clean = []
        self.driver.get(url)
        elem = WebDriverWait(self.driver, timeout=TIMEOUT).until(lambda d: d.find_element(By.ID, DOC_CHOOZE))
        elem.click()
        delay()

    def find_time(self):
        try:
            delay()
            visit_time = self.driver.find_elements(By.CSS_SELECTOR, 'div.picker-scroll-container')[2] \
                .find_elements(By.CSS_SELECTOR, 'li.picker-scroll-item')
            for time in visit_time[1:]:
                t = time.find_element(By.CSS_SELECTOR, 'button.TimeButton').text
                r = dt.strptime(f'{" ".join(self.date_clean)} {t}', '%b %d %Y %I:%M %p')
                self.diff_minuts = (r - dt.now()).total_seconds() // 60
                if self.diff_minuts >= INTERVAL:
                    time.click()
                    delay()
                    slot = self.driver.find_element(By.CSS_SELECTOR, 'button.createApp')
                    slot.click()  # Todo
                    sleep(200)
                    if not self.driver.find_element(ec.visibility_of_element_located('formErrorMessage')):
                        return r
                    else:
                        return 'Что-то не так... не забронировать время'
        except Exception:
            return 'Время не найдено'

    def find_date(self):
        try:
            date_source = self.driver.find_element(By.CSS_SELECTOR, 'div.picker-scroll-container') \
                .find_element(By.CSS_SELECTOR, 'li.picker-scroll-item') \
                .find_element(By.CLASS_NAME, 'calendarDay') \
                .find_elements(By.CSS_SELECTOR, 'div.ng-binding')
            for elem in date_source[1:3]:
                self.date_add(elem.text)
            self.date_add('2023')
            self.date_clean[0], self.date_clean[1] = self.date_clean[1], self.date_clean[0]  # Дата в формате списка
            self.date_clean_without_time = ps(" ".join(self.date_clean))  # Дата в формате datetime
            if self.date_clean_without_time <= MAX_DATA:
                q = self.find_time()
                if q != 'Время не найдено':
                    return q
                return f'Слот есть, но не успеть. {q}'
            return 'Даты за пределами интервала.'
        except Exception:
            return 'Даты отсутствуют.'

    def date_add(self, elem):
        self.date_clean.append(elem)
        return self.date_clean


def city_circle(driver):
    x = 1
    while x == 1:
        for i in Cities:
            for name, url in i.items():
                city = City(driver, name, url)
                f = city.find_date()
                print(f'{name}: {f}')
                if type(f) == datetime:
                    send_message(
                        f'Поймался слот: {name} - {f}\nОсталось {city.diff_minuts} минут\nwww.MyVisit.com')
                    x = 2
    return


def incert_and_push(driver, value, doc_value, batton_val):
    elem_input = WebDriverWait(driver, timeout=TIMEOUT).until(lambda d: d.find_element(By.ID, value))
    elem_input.send_keys(doc_value)
    button = WebDriverWait(driver, timeout=TIMEOUT).until(
        lambda d: d.find_element(By.CLASS_NAME, batton_val))
    button.click()
    delay()
    return


def parce():
    options = Options()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    options.add_argument('start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(MAIN_URL)
    delay()
    tel_input = WebDriverWait(driver, timeout=TIMEOUT).until(lambda d: d.find_element(By.ID, 'mobileNumber'))
    tel_input.send_keys(MY_TEL)
    capcha_input = WebDriverWait(driver, timeout=TIMEOUT).until(lambda s: s.find_element(By.NAME, 'userCaptchaInput'))
    capcha_input.send_keys(Keys.NULL)
    WebDriverWait(driver, timeout=60).until(ec.title_contains('myVisit - instant appointment scheduling'))
    delay()
    chooze_provider = driver.find_element(By.ID, "appContainer").find_element(By.XPATH,
                                                                              '//*[@id="providers-tab"]/div[3]/div/div[2]').find_element(
        By.XPATH, '//*[@id="mCSB_4_container"]/div/div[1]/ul/li[1]')
    chooze_provider.click()

    incert_and_push(driver, 'ID_KEYPAD', MY_TZ, 'exteranl-buttons-buttons')
    incert_and_push(driver, 'PHONE_KEYPAD', MY_TEL, 'exteranl-buttons-buttons')
    but1 = driver.find_element(By.CLASS_NAME, 'buttons')
    but1.click()
    delay()
    city_circle(driver)
    return None


if __name__ == '__main__':
    parce()
