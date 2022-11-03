from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import re
import MySQLdb
from scraping import bring_data
from weatherapi import get_weather

conn = MySQLdb.connect(
    user="aib15",
    passwd="gudrl123",
    host="127.0.0.1",
    db="searching_volume",
)

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS searching")
cursor.execute("DROP TABLE IF EXISTS weather")


cursor.execute("""CREATE TABLE weather (
    date int NOT NULL PRIMARY KEY, avgTa float, sumRn float, sumSsHr float)""")
cursor.execute("""CREATE TABLE searching (
    id int NOT NULL PRIMARY KEY, 
    ranking int, 
    attraction varchar(30), 
    cities varchar(10), 
    category varchar(30), 
    subcategory varchar(30), 
    volume int, 
    date int,
    FOREIGN KEY (date) REFERENCES weather (date))""")

index = 1


weather_date, avgTa, sumRn, sumSsHr = get_weather()

for i in range(len(weather_date)):
    cursor.execute(
        f"""INSERT INTO weather VALUES({weather_date[i]},\"{avgTa[i]}\",\"{sumRn[i]}\",\"{sumSsHr[i]}\")"""
    ) 

ranking, attraction, cities, division_category, subcategory, date, search_volume = bring_data()

for i in range(len(ranking)):
    cursor.execute(
        f"""INSERT INTO searching VALUES({index},\"{ranking[i]}\",\"{attraction[i]}\",
        \"{cities[i]}\",\"{division_category[i]}\",\"{subcategory[i]}\",\"{search_volume[i]}\",\"{date[i]}\")"""
    )
    index += 1



conn.commit()
conn.close()