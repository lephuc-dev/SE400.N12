from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import pandas as pd

def scraping_dynamic_web_pages(url, time_rest):
    options = webdriver.ChromeOptions()
    options.headless=True
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    # instantiate height of webpage 
    last_height = driver.execute_script('return document.body.scrollHeight')

    loop = True
    count=0

    # scroll to bottom of webpage
    while loop:
        driver.execute_script(
            'window.scrollTo(0, document.body.scrollHeight);')

        # wait for content to load
        time.sleep(time_rest)

        new_height = driver.execute_script('return document.body.scrollHeight')

        loop=(new_height!=last_height)

        last_height == new_height

        if count > 50:
            break
        count +=1

    web_page = driver.page_source
    driver.close()

    return web_page



def extract_text(string):
    new_string = ""

    for c in string:
        if c.isalpha():
            new_string = new_string + c
        elif c.isspace():
            new_string = new_string + c

    return new_string.lstrip()


def format_cost(string_cost):
    new_cost = ''

    for c in string_cost:
        if c.isdigit():
            new_cost = new_cost + c

    new_cost = float(new_cost)

    return new_cost


def string_to_int(s):
    n = 0

    for c in s:
        if c.isdigit():
            n = n * 10 + int(c)

    return n


def format_humidity(humidity_text):
    new_humidity = 0

    for c in humidity_text:
        if c.isdigit():
            new_humidity = new_humidity * 10 + int(c)

    return new_humidity


