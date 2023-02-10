from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

def scraping_dynamic_web_pages(url, time_rest):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    # instantiate height of webpage 
    last_height = driver.execute_script('return document.body.scrollHeight')


    loop = True

    # scroll to bottom of webpage
    while loop:
        driver.execute_script(
            'window.scrollTo(0, document.body.scrollHeight);')

        # wait for content to load
        time.sleep(time_rest)

        new_height = driver.execute_script('return document.body.scrollHeight')

        loop=(new_height!=last_height)

        last_height == new_height

    web_page = driver.page_source
    driver.close()

    return web_page
