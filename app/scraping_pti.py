import requests
from bs4 import BeautifulSoup
'''
Métodos para realização da busca em sites externos
Implementada busca no site https://empregos.profissionaisti.com.br
'''


def pti_get_http(search):
    '''
    Recebe um termo para buscar e realiza retorna o html
    '''
    search = search.replace(' ', '+')
    url = 'https://empregos.profissionaisti.com.br/?s={}'.format(search)
    return requests.get(url)


def pti_get_jobs(content):
    '''
    Recebe o html e o parseia utilizando lxml
    Depois percorre o html buscando as informações das vagas (jobs)
    Retorna uma lista de dicionários python com as informações das
    vagas encontradas
    '''
    soup = BeautifulSoup(content, 'lxml')

    jobs = soup.find_all('div', {'class': 'job-list-content'})

    d = []

    for job in jobs:
        data = soup.find('div', {'class': 'job-icons'})
        j = {
            'url': job.a.get('href'),
            'title': job.h4.string,
            'company': data.a.text,
            'salary': 'Não divulgado',
            'local': data.a.next_sibling.text
        }

        d.append(j)

    return d
