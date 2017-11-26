import requests
from bs4 import BeautifulSoup
'''
Métodos para realização da busca em sites externos
Implementada busca no site infojobs.com.br
'''


def if_get_http(search):
    '''
    Recebe um termo para buscar e realiza retorna o html
    '''
    url = 'https://www.infojobs.com.br/empregos.aspx?Palabra=%r' % search
    return requests.get(url)


def if_get_jobs(content):
    '''
    Recebe o html e o parseia utilizando lxml
    Depois percorre o html buscando as informações das vagas (jobs)
    Retorna uma lista com os links para as vagas encontradas
    '''
    soup = BeautifulSoup(content, 'lxml')

    jobs = soup.find_all('div', {'class': 'vaga'})

    jobs_list = []

    for job in jobs:
        jobs_list.append(job.a.get('href'))

    return jobs_list


def if_get_page_job(jobs_list):
    '''
    Recebe a lista com os links das vagas e acessa link por link,
    Chama a função parse_page_vaga passando como parametros o html da página
    da vaga e sua url e armazena seu retorno em um dicionário
    '''
    d = {}
    jobs = []

    for job in jobs_list:
        r = requests.get(job)

        d = if_parse_page_vaga(r.text, job)
        jobs.append(d.copy())

    return jobs


def if_parse_page_vaga(content, job_url):
    '''
    Recebe o html da página da vaga e sua url e busca as informações desejadas
    como Titulo, Descrição, Empresa, Salário e local de trabalho
    Armazena em um dicionário e retorna o mesmo
    '''
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
