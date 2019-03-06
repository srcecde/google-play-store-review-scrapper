import random
import time
from pprint import pprint   
from selenium import webdriver
import pandas as pd

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
actions = ActionChains(driver)
time.sleep(5)

def load_url(url, sleep=5):
    URL = 'https://play.google.com/store/apps/details?id='+url+'&hl=en&showAllReviews=true'
    driver.get(URL)
    time.sleep(sleep)


def action(r):
    for _ in range(r):
        actions.send_keys(Keys.SPACE).perform()
        time.sleep(random.randint(2, 3))

def scrap(element, name):
    rate = []
    review = []
    df = pd.DataFrame()
    for i in element:
        a =  i.find_element_by_xpath('.//div[@aria-label]')

        try:
            time.sleep(1)
            i.find_element_by_xpath('.//button[@jsname="gxjVle"]').click()
        except Exception as e:
            pass

        x =  i.find_element_by_xpath('.//span[@jsname="bN97Pc"]')
        y =  i.find_element_by_xpath('.//span[@jsname="fbQN7e"]')

        r = [int(i) for i in a.get_attribute("aria-label").split() if i.isdigit()][0]
        rate.append(r)

        if y.text.strip():
            review.append(y.text)

        else:
            review.append(x.text)
    df["rate"] = rate
    df["review"] = review
    df.to_csv(name.replace(".", "_")+".csv")

def main():
    with open("appsid.txt", "r") as f:
        appid = f.read().splitlines()

    for aid in appid:
        load_url(aid)
        for i in range(150):
            print(i)
            time.sleep(random.randint(2, 3))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                xx = driver.find_element_by_xpath('.//div[@jsname="i3y3Ic"]')
                if xx:
                    xx.click()
            except:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        element = driver.find_elements_by_xpath('.//div[@jscontroller="H6eOGe"]')
        scrap(element, aid)

main()
