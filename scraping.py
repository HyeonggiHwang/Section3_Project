from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import re

def bring_data():
    driver = webdriver.Chrome()

    driver.get('https://datalab.visitkorea.or.kr/datalab/portal/mbr/getMbrLoginForm.do')
    time.sleep(1)

    my_id = 'tbh03110@gmail.com'
    my_pw = 'Tkdlzl!@34'


    driver.find_element(By.ID,'mbrId').send_keys(my_id)
    driver.find_element(By.ID,'mbrPw').send_keys(my_pw)

    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    time.sleep(2)

    driver.get('https://datalab.visitkorea.or.kr/datalab/portal/bda/getTourVisitCnt.do')
    driver.find_element(By.ID,'srchAreaDate').send_keys('일간')
    time.sleep(2)

    daystart = driver.find_element(By.ID, "dayStart")
    dayend =  driver.find_element(By.ID, "dayEnd")

    daystart.clear()
    daystart.send_keys('20211101')
    time.sleep(1)

    dayend.clear()
    dayend.send_keys('20211101')
    time.sleep(2)

    element = driver.find_element(By.XPATH, "//*[@id='vmRegnWrap']/div[2]/a")
    driver.execute_script("arguments[0].click();", element)
    time.sleep(2)

    jeju_element = driver.find_element(By.XPATH, "//*[@id='srchNatCdList2']/a[9]")
    driver.execute_script("arguments[0].click();", jeju_element)

    jejusi_element = driver.find_element(By.XPATH, "//*[@id='srchSidoCdList1']/a[2]")
    driver.execute_script("arguments[0].click();", jejusi_element)
    time.sleep(2)

    driver.find_element(By.XPATH, "//*[@id='popup1']/div[3]/div/a[2]").click()
    time.sleep(1)
    con_button = driver.find_element(By.XPATH, "//*[@id='popup2']/div[3]/div/a[1]")
    con_button.click()
    time.sleep(1)


    # 데이터 수집할 리스트 생성

    ranking = []
    attraction = []
    cities = []
    division_category = []
    subcategory = []
    search_volume = []
    date = []

    search_button = driver.find_element(By.XPATH, "//*[@id='searchWrap']/div[2]/input")

    # 11월 날짜 리스트 생성

    days = []
    count = 20211101
    for i in range(31):
        days.append(count)
        count += 1
        if count == 20211131:
            break


# 데이터 수집


    for day in days:

        daystart.clear()
        daystart.send_keys(day)
        time.sleep(1)

        dayend.clear()
        dayend.send_keys(day)
        time.sleep(2)

        search_button.click()
        time.sleep(2)
        con_button.click()
        time.sleep(2)

        len_list_text = driver.find_element(By.XPATH, "//*[@id='PivotView']/div[5]/div[4]/span[2]").text
        len_list = int(re.sub("[()]","",len_list_text).split()[0])
        total_len = len(ranking)+len_list

        for i in range(999):
            time.sleep(2)

            for index in range(1, 13):
                try: 
                    row_element = driver.find_element(By.XPATH, f"//*[@id='PivotView_content_table']/tbody/tr[{index}]").text
                    row_list = row_element.split()
                    ranking.append(row_list[0])
                    attraction.append(row_list[1])
                    cities.append(row_list[3])
                    division_category.append(row_list[-3])
                    subcategory.append(row_list[-2])
                    date.append(day)
                    search_volume.append(int(row_list[-1].replace(',','')))
                except:
                    break
    
            if len(ranking) >= total_len:
                break

            time.sleep(1)
            next_page = driver.find_element(By.XPATH, "//*[@id='PivotView']/div[5]/div[3]/div[6]")
            next_page.click()
    
    driver.close()
    return ranking, attraction, cities, division_category, subcategory, date, search_volume

ranking, attraction, cities, division_category, subcategory, date, search_volume = bring_data()


