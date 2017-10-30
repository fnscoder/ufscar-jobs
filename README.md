# [ufscar-jobs](https://ufscar-jobs.herokuapp.com/)

## Desenvolvimento de Projetos e Sistemas 2

### Integrantes do Grupo 01
- FELIPE NOGUEIRA DE SOUZA 581038
- JOAO PAULO FRANCELINO MONTEIRO 545767
- Luis Fernando Molina 481866
- VITOR LEMES PAIZAM 544868
- WESLEY SILVA PEREIRA SALES 581100

Desenvolvido utilizando a linguagem Python e o framework web Flask.

Para executar o projeto é necessário:
- Python 3.6
- (Preferencialmente) Instalar o virtualenv e virtualenv-wrapper, criar um ambiente virtual e ativá-lo
- [Instalar WeasyPrint](http://weasyprint.readthedocs.io/en/latest/install.html#linux)
- Instalar o requirements.txt com o comando: <br />
$ pip install -r requirements.txt

O projeto está configurado para rodar com o banco de dados PostgreSQL remoto hospedado no Heroku.
Para usar o PostgreSQL Local
Instalar o sgbd PostgreSQL, criar um database e uma conexão e alterar as configurações de conexão no arquivo config.py:
- database: ufscar-jobs
- servidor: localhost
- user: postgres
- senha: 123456

Se for rodar o projeto com banco local é necessário rodar os seguintes comandos para preparar o DB
Preparar o DB com os comandos: <br />
$ python run.py db init <br />
$ python run.py db migrate <br />
$ python run.py db upgrade <br />

Rodar o projeto: <br />
$ python run.py runserver

O projeto estará rodando em:
http://127.0.0.1:5000/

Projeto hospedado no Heroku rodando em:
https://ufscar-jobs.herokuapp.com/
