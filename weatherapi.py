import requests
import json
import pandas as pd

def get_weather():
    API_KEY = 'IkTKGUYn60f25hD+K5Z75ZTJHmaNxmI8Cu//RStYlo94E66fPlIq7x+sNeHFN4CpxNEfroyeDY1zvyQ5S845+g=='

    url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
    params = {'serviceKey' : API_KEY, 'pageNo' : '1', 'numOfRows' : '100', 'dataType' : 'JSON', 'dataCd' : 'ASOS', 'dateCd' : 'DAY', 'startDt' : '20211101', 'endDt' : '20211130', 'stnIds' : '184' }

    response = requests.get(url, params=params)
    content = json.loads(response.text)

    date = []
    avgTa = []
    sumRn = []
    sumSsHr = []


    for i in range(30):
        element = content['response']['body']['items']['item'][i]
        date.append(int(element['tm'].replace('-','')))
        avgTa.append(element['avgTa'])
        sumRn.append(element['sumRn'])
        sumSsHr.append(element['sumSsHr'])
    
    for i in range(len(sumRn)):
        if sumRn[i] == '':
            sumRn[i]=sumRn[i].zfill(1)
        else:
            sumRn[i] = sumRn[i]
    
    return date, avgTa, sumRn, sumSsHr
