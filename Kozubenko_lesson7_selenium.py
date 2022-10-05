from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
from pymongo import MongoClient

print('start')
'''
# change 'ip:port' with your proxy's ip and port
# proxy_ip_port = 'http://157.230.239.42:1337'   # US-
# proxy_ip_port = 'http://172.105.184.208:8001'  # US
# proxy_ip_port = 'http://93.188.8.25:3128'  # GE-

proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = proxy_ip_port
proxy.ssl_proxy = proxy_ip_port

capabilities = webdriver.DesiredCapabilities.CHROME
proxy.add_to_capabilities(capabilities)

driver = webdriver.Chrome(desired_capabilities=capabilities)
'''

driver = webdriver.Chrome()

# driver.get('https://2ip.ua/ua/')
driver.get('https://account.mail.ru/')

print('page is loaded')
time.sleep(2)
# driver.quit()



'''
# time.sleep(25)
print('ищу логин')
button_login = driver.find_element(By.XPATH, "//button[@class='resplash-btn resplash-btn_primary resplash-btn_mailbox-big svelte-j4p44z']")
button_login.click()
# time.sleep(25)
'''

# WebElement fr = driver.find_element(By.XPATH, "//iframe[@class='ag-popup__frame__layout__iframe']")
# driver.switch_to.frame(fr)


print('нажата Войти')
'''
while True:
    wait = WebDriverWait(driver, 35)
    try:
        element_name = driver.find_element(By.NAME, 'username')
        # element_name =
        element_name.send_keys('study.ai_172@mail.ru')
        element_name.send_keys(Keys.ENTER)
        break
    except NoSuchElementException:
        print("Скролл окончен")
        break
'''
element_name = driver.find_element(By.NAME, 'username')
element_name.send_keys('study.ai_172@mail.ru')
element_name.send_keys(Keys.ENTER)
time.sleep(10)
element_password = driver.find_element(By.NAME, 'password')
element_password.send_keys('NextPassword172#')
time.sleep(1)
element_password.send_keys(Keys.ENTER)

print('вхожу')
time.sleep(3)

while True:
    wait = WebDriverWait(driver, 3)
    try:
        button_cookie = driver.find_element(By.XPATH, "//a[@class='cmpboxbtn cmpboxbtnyes cmptxt_btn_yes']")
        button_cookie.click()
        print('cookies ON')
        break
    except NoSuchElementException:
        print("Куков нет")
        break

print('cookies ON')

# class_name = 'llc_normal'
# class_name = 'js-letter-list-item js-tooltip-direction_letter-bottom'

# Making a Connection with MongoClient
client = MongoClient()
# database
db = client['emails']
# collection
test_address = db['study.ai_172@mail.ru']


def get_data_from_page():
    time.sleep(3)
    list_links_tmp = driver.find_elements(By.XPATH, f"//a[contains(@class, 'js-letter-list-item js-tooltip-direction_letter-bottom')]")
    list_links = []
    for letter in list_links_tmp:
        letter_link = letter.get_attribute('href')
        # print(letter_link)
        list_links.append(letter_link)
    print(len(list_links))
    time.sleep(3)
    list_senders_tmp = driver.find_elements(By.XPATH, "//a[contains(@class, 'js-letter-list-item js-tooltip-direction_letter-bottom')]/div[4]/div[1]/div[1]/span[1]")
    list_senders = []
    for sender in list_senders_tmp:
        sender_name = sender.get_attribute('title')
        # print(sender_name)
        list_senders.append(sender_name)
    print(len(list_senders))
    time.sleep(3)
    list_dates_tmp = driver.find_elements(By.XPATH, "//a[contains(@class, 'js-letter-list-item js-tooltip-direction_letter-bottom')]/div[4]/div[1]/div[5]")
    list_dates = []
    for date in list_dates_tmp:
        date_index = date.get_attribute('title')
        # print(date_index)
        list_dates.append(date_index)
    print(len(list_dates))
    time.sleep(3)
    list_subjects_tmp = driver.find_elements(By.XPATH, "//a[contains(@class, 'js-letter-list-item js-tooltip-direction_letter-bottom')]/div[4]/div[1]/div[3]/span[1]/div/span[1]")
    list_subjects = []
    for subj in list_subjects_tmp:
        subject = subj.text
        # print(subject)
        list_subjects.append(subject)
    print(len(list_subjects))
    time.sleep(3)
    return {
        'links': list_links,
        'senders': list_senders,
        'dates': list_dates,
        'subjects': list_subjects
    }


mails_dict_first = get_data_from_page()
last_mail_from_dict = mails_dict_first['links'][-1]

for i in range(len(mails_dict_first['links'])):
    x_email = mails_dict_first['links'][i]
    if not len(list(db.test_address.find({'links': x_email}))):
        db.test_address.insert_one({
            'links': mails_dict_first['links'][i],
            'senders': mails_dict_first['senders'][i],
            'dates': mails_dict_first['dates'][i],
            'subjects': mails_dict_first['subjects'][i]
        })

time.sleep(3)

scroll = driver.find_element(By.XPATH, '//div[@aria-label="grid"]')
scroll.is_selected()
while True:
    time.sleep(3)
    scroll.send_keys(Keys.PAGE_DOWN)
    time.sleep(5)
    mails_dict_new = get_data_from_page()
    for i in range(len(mails_dict_new['links'])):
        x_email = mails_dict_new['links'][i]
        if not len(list(db.test_address.find({'links': x_email}))):
            db.test_address.insert_one({
                'links': mails_dict_new['links'][i],
                'senders': mails_dict_new['senders'][i],
                'dates': mails_dict_new['dates'][i],
                'subjects': mails_dict_new['subjects'][i]
            })
    if last_mail_from_dict == mails_dict_new['links'][-1]:
        break
    else:
        last_mail_from_dict = mails_dict_new['links'][-1]


print()
driver.quit()
