# 1. Необходимо парсить страницу со свежими вакансиями с поиском по "Python" и городами "Москва" и "Санкт-Петербург". Эти параметры задаются по ссылке
# 2. Нужно выбрать те вакансии, у которых в описании есть ключевые слова "Django" и "Flask".
# 3. Записать в json информацию о каждой вакансии - ссылка, вилка зп, название компании, город.


import json
import requests
from fake_headers import Headers
from bs4 import BeautifulSoup

# функция для получения заголовков
def get_headers():
    return Headers(browser='firefox', os='win').generate()

# 2. функция для извлечения данных о вакансиях
def extract_vacancies(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        bs = BeautifulSoup(response.text, 'lxml')
        articles_list = bs.find_all(class_='vacancy-serp-item__layout')
        vacancies = []
        for article in articles_list:
            link = article.find('a')['href']
            salary_element = article.find('span', class_='bloko-header-section-2')
            salary = salary_element.text.strip() if salary_element else None
            company = article.find('a', class_='bloko-link bloko-link_kind-tertiary').text.strip()
            city_element = article.find('div',{'data-qa':'vacancy-serp__vacancy-address'})
            city = city_element.text.strip() if city_element else None
            vacancies.append({
                'Зарплата': salary,
                'Компания': company,
                'Город': city,
                'Ссылка': link
            })
        return vacancies
    else:
        print(f"Ошибка при получении страницы: {response.status_code}")
        return []

# 3. сохраняем данные в json
def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# далее сама программа
HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
HEADERS = get_headers()

vacancies_data = extract_vacancies(HOST, HEADERS)

# сохраняем данные о вакансиях в JSON-файл
save_to_json(vacancies_data, 'vacancies.json')

