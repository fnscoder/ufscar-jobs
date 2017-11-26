import requests
from bs4 import BeautifulSoup
'''
Métodos para realização da busca em sites externos
Implementada busca no site infojobs.com.br
'''


def vg_get_http(search):
    '''
    Recebe um termo para buscar e realiza retorna o html
    '''
    search = search.replace(' ', '-')
    url = 'https://www.vagas.com.br/vagas-de-{}?'.format(search)
    return requests.get(url)


def vg_get_jobs(content):
    '''
    Recebe o html e o parseia utilizando lxml
    Depois percorre o html buscando as informações das vagas (jobs)
    Retorna uma lista com os links para as vagas encontradas
    '''
    soup = BeautifulSoup(content, 'lxml')

    jobs = soup.find_all('article')

    d = []

    for job in jobs:
        url = job.a.get('href')
        title = job.a['title']
        company = job.h2.next_sibling.next_sibling.text.replace('\n', '')
        salary = 'Não informado'
        local = job.h2.span.text.replace('\n', '')
        
        j = {
            'url': url,
            'title': title,
            'company': company,
            'salary': salary,
            'local': local
        }

        d.append(j)

    return d
