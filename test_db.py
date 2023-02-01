import pymysql

from datetime import datetime

TIME_STAMP = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
MYSQL_DATABASE_URL = "mysql+mysqldb://kiteiboleto:Ogun153412#@kiteiboleto.mysql.dbaas.com.br/kiteiboleto"
SERVER_APP_URL = '127.0.0.1'
SERVER_APP_PORT = 8000
DB_SERVER = 'kiteiboleto.mysql.dbaas.com.br'
DB_PORT = 3306
DB_USER = 'kiteiboleto'
DB_PWD = 'Ogun153412#'
DB_NAME = 'kiteiboleto'

conn = pymysql.connect(
    host=DB_SERVER,
    user=DB_USER,
    password=DB_PWD,
    database=DB_NAME,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)



#CREATE
dt_download = TIME_STAMP
id_acordo = 1
cd_cedente = '20'
nm_cedente = 'PAG'
tx_cpf = '111.111.111-11'
id_parcela = 1
tx_url = 'https://kitei.com.br'

cursor = conn.cursor()
cmd = 'INSERT INTO kiteiboleto.download(dt_download, id_acordo, cd_cedente, nm_cedente, tx_cpf, id_parcela, tx_url) ' \
      f'VALUES ( "{dt_download}",{id_acordo},"{cd_cedente}","{nm_cedente}" , "{tx_cpf}", {id_parcela}, "{tx_url}" )'
cursor.execute(cmd)
cursor.close()


#READ
cursor = conn.cursor()
cmd = 'SELECT id, dt_download, id_acordo, cd_cedente, nm_cedente, tx_cpf, id_parcela, tx_url ' \
      'FROM kiteiboleto.download ' \
      'ORDER BY dt_download , cd_cedente , id_acordo'
cursor.execute(cmd)
result = cursor.fetchall()
print(result)
cursor.close()