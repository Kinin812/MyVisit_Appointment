from random import randint
from time import sleep
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
MY_TEL = '0559578701'
MY_TZ = '347812687'
MOUNTH = 'апр'
MAX_DATA = 20
MAIN_URL = 'https://myvisit.com/#!/home/signin/'
TIMEOUT = 300

Cities = [
    {'Hadera': 'https://myvisit.com/#!/home/service/2144'},
    {'Netanya': 'https://myvisit.com/#!/home/service/2146'},
    {'Tayba': 'https://myvisit.com/#!/home/service/2749'},
    # {'Kphar-Saba': 'https://myvisit.com/#!/home/service/2110'},
    {'Gertsliya': 'https://myvisit.com/#!/home/service/2245'},
    {'Petakh-Tikva': 'https://myvisit.com/#!/home/service/2113'},
    {'Bney-Brak': 'https://myvisit.com/#!/home/service/2163'},
#    {'Rosh-Ha-Ain': 'https://myvisit.com/#!/home/service/2167'},
#   {'RAmat-Gan-Givataim': 'https://myvisit.com/#!/home/service/2097'},
#     {'Tel-Aviv': 'https://myvisit.com/#!/home/service/2099'},
#     {'Yaffo': 'https://myvisit.com/#!/home/service/2165'},
#     {'Um-El-Fahm': 'https://myvisit.com/#!/home/service/8977'},
#     {'Holon': 'https://myvisit.com/#!/home/service/2153'},
#     {'Rishon-Le-Tsion': 'https://myvisit.com/#!/home/service/2241'},
]


def delay():
    sleep(randint(5, 7))


def find_time(driver, date):
    try:
        delay()
        visit_time = driver.find_elements(By.CSS_SELECTOR, 'div.picker-scroll-container')[2] \
            .find_element(By.CSS_SELECTOR, 'li.picker-scroll-item').find_element(By.CSS_SELECTOR, 'button.TimeButton')
        visit_time.click()
        delay()
        slot = driver.find_element(By.CSS_SELECTOR, 'button.createApp')
        slot.click()
        delay()
        return visit_time.text
    except Exception:
        return 'Время не найдено'


def find_date(driver):
    try:
        date_source = driver.find_element(By.CSS_SELECTOR, 'div.picker-scroll-container') \
            .find_element(By.CSS_SELECTOR, 'li.picker-scroll-item') \
            .find_element(By.CLASS_NAME, 'calendarDay') \
            .find_elements(By.CSS_SELECTOR, 'div.ng-binding')
        date_clean = []
        for elem in date_source[1:3]:
            date_clean.append(elem.text)
        if date_clean[1] == MOUNTH and int(date_clean[0]) <= MAX_DATA:
            fff = find_time(driver, date_clean[0])
            date_clean.append(fff)
            return date_clean
        return 'Нет подходящей даты'
    except Exception:
        print("")


def city_circle(driver):
    x = 1
    while x == 1:
        for city in Cities:
            for key, item in city.items():
                driver.get(item)
                elem = WebDriverWait(driver, timeout=TIMEOUT).until(lambda d: d.find_element(By.ID, DOC_CHOOZE))
                elem.click()
                delay()
                f = find_date(driver)
                print(key, f)
                if type(f) == list:
                    send_message(f'Поймался слот: {key} - {f[0]} {f[1]} {f[2]}')
                    x = 2
                    break


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
    # chooze_provider = driver.find_element(By.ID, "appContainer").find_element(By.CSS_SELECTOR,
    #         'li.provider-tile').find_element(By.PARTIAL_LINK_TEXT, '56.png')
    chooze_provider.click()

    incert_and_push(driver, 'ID_KEYPAD', MY_TZ, 'exteranl-buttons-buttons')
    incert_and_push(driver, 'PHONE_KEYPAD', MY_TEL, 'exteranl-buttons-buttons')
    city_circle(driver)
    return None


if __name__ == '__main__':
    parce()
