from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import common
import openpyxl
import time
from bs4 import BeautifulSoup as bs
import requests


def parse(el):
    base = []
    text = (el.find_element(by=By.CLASS_NAME, value="o-info").find_elements(by=By.TAG_NAME, value="a"))
    base.append(f"{text[0].text}")
    base.append(f"{text[1].text}")
    url_olimp = el.find_element(by=By.CLASS_NAME, value="none_a.black").get_attribute('href')
    base.append(url_olimp)
    raiting = el.find_element(by=By.CLASS_NAME, value="pl_rating").text
    base.append(raiting)
    try:
        dop_info = el.find_element(by=By.CLASS_NAME, value="none_a.black.olimp_desc").text
    except(common.NoSuchElementException):
        dop_info = ''
    base.append(dop_info)
    request = requests.get(url_olimp)
    soup = bs(request.text, 'html.parser')
    steps = soup.find_all('tr', {'class': "notgreyclass"})
    for step in steps:
        date = (step.text).replace('\n', ' ')
        base.append(date)

    return base


def get_olipics(driver):
    olimpics = []
    for i in range(4):
        scroll(5, 1, driver)
    olimpics.append(driver.find_elements(by=By.CLASS_NAME, value="fav_olimp.olimpiada "))
    return olimpics


def scroll(count, delay, driver):
    for i in range(count):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)


def main():
    yadisk = 'https://olimpiada.ru/activities?subject%5B7%5D=on&class=any&type=any&period_date=&period=year'
    options = webdriver.ChromeOptions()
    # options.add_argument(
    #         r"C:\Users\theqoocjil\AppData\Local\Google\Chrome\User Data")
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    driver.get(yadisk)
    olimpics = get_olipics(driver)
    olimpics = olimpics[0]
    wb = openpyxl.Workbook()
    ws = wb.active
    header = ['Name', '2', '3']
    ws.append(header)
    for el in olimpics:
        data = parse(el)
        ws.append(data)
    wb.save("inf.xlsx")


if __name__ == "__main__":
    main()