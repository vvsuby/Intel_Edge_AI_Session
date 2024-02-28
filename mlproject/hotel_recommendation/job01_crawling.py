from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

start_url = 'https:/www.yanolja.com/'
button_region_xpath = '//*[@id="__next"]/div[1]/main/section/section/section/section[1]/div/div/div/button'
driver.get(start_url)
time.sleep(0.5)
hotel_url = driver.find_element('xpath', '//*[@id="__next"]/div[1]/section[1]/section/section/section[1]/div[1]/a[1]').get_attribute('href')
driver.get(hotel_url)
time.sleep(0.5)
button_region = driver.find_element(By.XPATH, button_region_xpath)
driver.execute_script('arguments[0].click();', button_region)
time.sleep(0.5)
button_jeonra_xpath = 'html/body/div[3]/div/div/div/div/main/section/div/ul[1]/li[8]'
button_jeonra = driver.find_element(By.XPATH, button_jeonra_xpath)
driver.execute_script('arguments[0].click();', button_jeonra)
time.sleep(0.5)
all_url = driver.find_element('xpath', '/html/body/div[3]/div/div/div/div/main/section/div/ul[2]/li/a').get_attribute('href')
driver.get(all_url)
time.sleep(0.5)
button_popular_xpath = '//*[@id="__next"]/div[2]/section[1]/button'
button_popular = driver.find_element(By.XPATH, button_popular_xpath)
driver.execute_script('arguments[0].click();', button_popular)
time.sleep(0.5)
button_many_xpath = '/html/body/div[4]/div/div/section/div/ul/li[5]/button'
button_many = driver.find_element(By.XPATH, button_many_xpath)
driver.execute_script('arguments[0].click();', button_many)
time.sleep(1)
for i in range(13):
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(0.5)
list_review_url = []
hotel_name1 = []
hotel_name2 = []

for i in range(1, 151):
    base = driver.find_element(By.XPATH, f'//*[@id="__next"]/div[2]/section[2]/div/div/div[{i}]/a').get_attribute("href")
    list_review_url.append(f"{base}/review")
    title1 = driver.find_element(By.XPATH, f'//*[@id="__next"]/div[2]/section[2]/div/div/div[{i}]/a/div[1]/div[2]/div[2]').text
    hotel_name1.append(title1)
    title2 = driver.find_element(By.XPATH, f'//*[@id="__next"]/div[2]/section[2]/div/div/div[{i}]/a/div/div[2]/div[1]').text
    # //*[@id="__next"]/div[2]/section[2]/div/div/div[75]/a/div[1]/div[2]/div[1]
    # //*[@id="__next"]/div[2]/section[2]/div/div/div[88]/a/div/div[2]/div[1]
    hotel_name2.append(title2)

hap_hotel_name = []
for i in range(150):
    if('1'<= hotel_name1[i][0] <='9'):
        hap_hotel_name.append(hotel_name2[i])
    else:
        hap_hotel_name.append(hotel_name1[i])
print(len(hap_hotel_name))

df = pd.DataFrame({'names': hap_hotel_name})
df.to_csv('./crawling_data/hap_hotel_names_jeonra.csv', index=False)
print(len(hap_hotel_name))

review_url = []
for i in list_review_url:
    add = i.replace('www.yanolja.com/hotel','place-site.yanolja.com/places')
    review_url.append(add)
print(len(review_url))

reviews = []
names = []
for idx, url in enumerate(review_url):
    driver.get(url)
    time.sleep(0.5)
    review = ''
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(1, document.documentElement.scrollHeight);")
    time.sleep(0.5)
    for i in range(6):
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(0.5)
    for i in range(1, 21):
        try:
            review_one_xpath = '//*[@id="__next"]/div/div/main/div/div[4]/div/div[{}]/div/div/div[2]/div[1]'.format(i)
            review = review + ' ' + driver.find_element(By.XPATH, review_one_xpath).text
            time.sleep(0.5)
        except:
            print('초기 인덱스 에러', i)
    for j in range(2, 6):
        for k in range(1, 21):
            try:
                review_other_xpath = f'//*[@id="__next"]/div/div/main/div/div[4]/div[{j}]/div[{k}]/div/div/div[2]'
                review = review + ' ' + driver.find_element(By.XPATH, review_other_xpath).text
            except NoSuchElementException:
                try:
                    review_another_xpath = f'//*[@id="__next"]/div/div/main/div/div[4]/div[{j}]/div[{k}]/div/div/div[2]/div[1]'
                    review = review + ' ' + driver.find_element(By.XPATH, review_another_xpath).text
                except:
                    print('review error', idx, j, k)
    reviews.append(review)
    names.append(hap_hotel_name[idx])

    if (idx+1) % 30 == 0:
        print(idx)
        df = pd.DataFrame({'names': names, 'reviews': reviews})
        df.to_csv('./crawling_data/reviews_jeonra{}.csv'.format(idx), index=False)
        names = []
        reviews = []
        # for i in range(5):
        #     df = pd.DataFrame({'names': hap_hotel_name[i*30:i*30+30], 'reviews': reviews})
        #     df.to_csv('./crawling_data/reviews_seoul{}.csv'.format(idx), index=False)

print(len(reviews))
# df = pd.DataFrame({'names': hap_hotel_name, 'reviews': reviews})
# df.to_csv('./crawling_data/reviews_gangwon.csv', index=False)