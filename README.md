# ufscar-jobs

## Desenvolvimento de Projetos e Sistemas 1

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
- Instalar o requirements.txt com o comando: <br />
$ pip install -r requirements.txt

Instalar o sgbd MySQL, criar uma conexão:
- servidor: localhost
- user: root
- senha: root

Preparar o DB com os comandos: <br />
$ python run.py db init <br />
$ python run.py db migrate <br />
$ python run.py db upgrade <br />

Rodar o projeto: <br />
$ gunicorn app:app

O projeto estará rodando em:
http://127.0.0.1:8000/
