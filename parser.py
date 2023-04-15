import datetime
from datetime import datetime as dt
from time import sleep
from random import randint
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
from config import (
    DOC_CHOOZE, MY_TEL, MY_TZ, MAX_DATA,
    MAIN_URL, TIMEOUT, INTERVAL, Cities
)


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
        delay()
        elem = WebDriverWait(self.driver, timeout=TIMEOUT).until(ec.visibility_of_element_located((By.ID, DOC_CHOOZE)))
        elem.click()
        delay()

    def find_time(self):
        try:
            visit_time = self.driver.find_elements(By.CSS_SELECTOR, 'div.picker-scroll-container')[2] \
                .find_elements(By.CSS_SELECTOR, 'li.picker-scroll-item')
            for time in visit_time:
                t = time.find_element(By.CSS_SELECTOR, 'button.TimeButton').text
                r = dt.strptime(f'{" ".join(self.date_clean)} {t}', '%b %d %Y %I:%M %p')
                self.diff_minuts = (r - dt.now()).total_seconds() // 60
                if self.diff_minuts >= INTERVAL:
                    time.click()
                    slot = WebDriverWait(self.driver, timeout=TIMEOUT) \
                        .until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'button.createApp')))
                    slot.click()
                    return r
        except Exception:
            return 'Время не найдено'

    def find_date(self):
        delay()
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
                return 'Слот есть, но не успеть.'
            return 'Слоты за пределами интервала.'
        except Exception:
            return 'Слоты отсутствуют.'

    def date_add(self, elem):
        self.date_clean.append(elem)
        return self.date_clean


def city_circle(driver):
    x = 1
    while x == 1:
        for name, url in Cities.items():
            city = City(driver, name, url)
            f = city.find_date()
            print(f'{dt.now().time()} - {name}: {f}')
            if type(f) == datetime.datetime:
                send_message(f'{dt.now()} - Поймался слот на {DOC_CHOOZE[1]}:\n{name} - {f}\nОсталось {city.diff_minuts} минут\nwww.MyVisit.com')
                x = 2
                break
    return


def incert_and_push(driver, value, doc_value, batton_val):
    elem_input = WebDriverWait(driver, timeout=TIMEOUT).until(ec.visibility_of_element_located((By.ID, value)))
    elem_input.send_keys(doc_value)
    button = WebDriverWait(driver, timeout=TIMEOUT).until(ec.visibility_of_element_located((By.CLASS_NAME, batton_val)))
    button.click()
    return


def parce():
    options = Options()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    options.add_argument('start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(MAIN_URL)
    delay()
    tel_input = WebDriverWait(driver, timeout=TIMEOUT).until(ec.visibility_of_element_located((By.ID, 'mobileNumber')))
    tel_input.send_keys(MY_TEL)
    capcha_input = WebDriverWait(driver, timeout=TIMEOUT).until(
        ec.presence_of_element_located((By.NAME, 'userCaptchaInput'))
    )
    capcha_input.send_keys(Keys.NULL)
    WebDriverWait(driver, timeout=60).until(ec.title_contains('myVisit - instant appointment scheduling'))
    #    delay()
    chooze_provider = WebDriverWait(driver, timeout=TIMEOUT) \
        .until(ec.visibility_of_element_located((By.ID, "appContainer")))
    chooze_provider = chooze_provider.find_element(By.XPATH, '//*[@id="providers-tab"]/div[3]/div/div[2]')
    delay()
    chooze_provider = chooze_provider.find_element(By.XPATH, '//*[@id="mCSB_4_container"]/div/div[1]/ul/li[1]')
    chooze_provider.click()
    incert_and_push(driver, 'ID_KEYPAD', MY_TZ, 'exteranl-buttons-buttons')
    incert_and_push(driver, 'PHONE_KEYPAD', MY_TEL, 'exteranl-buttons-buttons')
    but1 = driver.find_element(By.CLASS_NAME, 'buttons')
    but1.click()
    city_circle(driver)
    return None


if __name__ == '__main__':
    parce()
