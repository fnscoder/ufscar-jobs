import requests
from bs4 import BeautifulSoup
import json


def get_http(search):
    url = 'https://www.infojobs.com.br/empregos.aspx?Palabra=%r' % search

    return requests.get(url)


def get_jobs(content):
    soup = BeautifulSoup(content, 'lxml')

    jobs = soup.find_all('div', {'class': 'vaga'})

    jobs_list = []

    for job in jobs:
        jobs_list.append(job.a.get('href'))

    return jobs_list


def get_page_job(jobs_list):
    d = {}
    jobs = []

    for job in jobs_list:
        r = requests.get(job)

        d = parse_page_vaga(r.text, job)
        jobs.append(d.copy())

    return jobs


def parse_page_vaga(content, job_url):
    soup = BeautifulSoup(content, 'lxml')

    title = soup.find('span', {
        'id': 'ctl00_phMasterPage_cVacancySummary_litVacancyTitle'}).string
    company = soup.find('div', {
        'class': 'txtCompany'}).string
    salary = soup.find('span', {
        'id': 'ctl00_phMasterPage_cVacancySummary_litSalary'}).string
    local = soup.find('span', {
        'id': 'ctl00_phMasterPage_cVacancySummary_litLocation'}).string

    d = {
        'url': job_url,
        'title': title,
        'company': company,
        'salary': salary,
        'local': local
    }

    return d
