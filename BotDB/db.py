import os
import sqlite3 as db
import time

import pandas as pd
from lxml import html
from fake_useragent import UserAgent
from statistics import mean
from selenium import webdriver

ua = UserAgent()


def sql_start():
    global conn, cur
    conn = db.connect('db.sqlite3')
    cur = conn.cursor()
    if conn:
        print('DB is OK!')
    conn.execute('CREATE TABLE IF NOT EXISTS general('
                 'id INTEGER PRIMARY KEY, '
                 'name TEXT, '
                 'url TEXT, '
                 'xpath TEXT)')
    conn.commit()


# Добавление данных от пользователя в таблицы
async def sql_add_command():
    df = pd.read_excel('file.xlsx')
    for i, row in df.iterrows():
        cur.execute('INSERT INTO general(name, url, xpath) '
                    'VALUES (?, ?, ?)', tuple(row))
    conn.commit()


# Скачиваем страницы с полным HTML кодом
async def get_pages(url, name):
    options = webdriver.FirefoxOptions()
    options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    options.set_preference('general.useragent.override', str(ua.firefox))
    try:
        driver = webdriver.Firefox(
            executable_path=r'parser_zuzublers\geckodriver.exe',
            options=options
        )
        driver.get(url)
        time.sleep(3)

        with open(f'{name}.html', 'w', encoding='utf-8') as file:
            file.write(driver.page_source)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


# Парсим скачанные страницы
async def lets_some_parse(df):
    names_list = df['Название'].to_list()
    urls_list = df['URL'].to_list()
    xpath_list = df['Xpath'].to_list()
    average_prices = []
    for (name, url, xpath) in zip(names_list, urls_list, xpath_list):
        await get_pages(url=url, name=name)
        with open(f'{name}.html', 'r', encoding='utf-8') as file:
            tree = html.fromstring(file.read())
            data = tree.xpath(f'{xpath}')
            price_list = []
            for item in data:
                price = int(item.text_content()
                            .strip('руб.').replace(',', '').replace(' ', ''))
                price_list.append(price)
            average_prices.append(mean(price_list))
        os.remove(f'{name}.html')
    os.remove('file.xlsx')
    return average_prices
