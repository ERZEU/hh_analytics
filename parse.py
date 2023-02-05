import json
import requests
# from fake_useragent import UserAgent
import re
from currency import get_currency




def get_data_from_hh(name, page = 0, area = 113): #113 - rus
    """Подключение к серверу и получение json объекта"""

    #ua = UserAgent()
    url = 'https://api.hh.ru/vacancies'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.2.807 Yowser/2.5 Safari/537.36'#ua.random
    }

    params = {
        'text': f'NAME:{name}', # Текст фильтра. В имени должно быть слово 
        'area': area, # Поиск ощуществляется по вакансиям 
        'page': page, # Индекс страницы поиска на HH
        'per_page': 100, # Кол-во вакансий на 1 странице
        'only_with_salary': False
    }

    req = requests.get(url=url, headers=headers, timeout=5, params=params)
    data = req.content.decode() # Декодируем его ответ, чтобы Кириллица отображалась корректно

    req.close()
    det = json.loads(data)

    return det
    

def prepare_salary(name, area):
    """Парсинг и формирование датасета"""

    req = requests.get('https://api.hh.ru/dictionaries')
    data = req.content.decode() # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    det = json.loads(data)

    det = det['currency']
    real_currency_rate = get_currency()
    check_size = get_data_from_hh(name=name, area=area)

    if check_size.get('found') != None:
        mas = []
        mas_req = []
        for page in range(0, check_size.get('pages')):
            data = get_data_from_hh(name, page, area)
            if data.get('items'):
                for vacancy in data.get('items'):
                    if vacancy['salary']:
                        mas.append([vacancy['name'], vacancy['alternate_url'],
                                    vacancy['area']['name'], vacancy['published_at'][:10], 
                                    str(vacancy['salary']['from'] or ""), 
                                    str(vacancy['salary']['to'] or ""),
                                    str(vacancy['salary']['currency'] or "")]) # изменение
                        if mas[len(mas)-1][4] and mas[len(mas)-1][6]:
                            mas[len(mas)-1][4] = str(int(round(int(mas[len(mas)-1][4]) / real_currency_rate[mas[len(mas)-1][6]])))
                        if mas[len(mas)-1][5] and mas[len(mas)-1][6]:
                            mas[len(mas)-1][5] = str(int(round(int(mas[len(mas)-1][5]) / real_currency_rate[mas[len(mas)-1][6]])))
                    else:
                        mas.append([vacancy['name'], vacancy['alternate_url'],
                                    vacancy['area']['name'], vacancy['published_at'][:10],
                                    "",
                                    ""]) 
                    mas_req.append(vacancy['snippet']['requirement'])
        return mas, mas_req

    
def get_area(name_area):
    """Сопоставление региона или города поиска с его id"""

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.2.807 Yowser/2.5 Safari/537.36'
    }
    url = 'https://api.hh.ru/areas'
 
    req = requests.get(url=url, headers=headers, timeout=5)

    
    areas = json.loads(req.content.decode())
    req.close()
    for region in areas[0]['areas']: #поиск по регионам России
        if re.search(name_area, region['name'], re.IGNORECASE):
            return region['id']
        for city in region['areas']: 
            if re.search(name_area, city['name'], re.IGNORECASE):
                return city['id']
