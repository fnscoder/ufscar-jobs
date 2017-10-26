DEBUG = True

#  Configuração para conexão com o sgbd postgres heroku
SQLALCHEMY_DATABASE_URI = 'postgresql://xhvgkkinbyiubk:0f12410f53faa42e58b39437be255ef20b45191f2e2d259fa9caa5a13e988466@ec2-23-23-227-188.compute-1.amazonaws.com/df07ntgqekh8o6'
#  Configuração para conexão com o sgbd postgres local
#SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@localhost/ufscarjobs'

SQLALCHEMY_TRACK_MODIFICATIONS = True

# chave secreta para os formulários
SECRET_KEY = 'pJMlGrhStBPmGhJlRs4BL'
