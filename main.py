# Project: API Get information about download pdf for KITEI
# Date: 30-01-2023
# Author: Silverio Leite Jr
# pip install -r requirements.txt

import uvicorn
from fastapi import Depends, FastAPI, status, Request
from fastapi.security import OAuth2PasswordBearer

import pymysql
from typing import Union
from pydantic import BaseModel
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv()

SERVER_APP_URL = '127.0.0.1'
SERVER_APP_PORT = 8000
DB_SERVER = os.getenv('DB_SERVER')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PWD = os.getenv('DB_PWD')
DB_NAME = os.getenv('DB_NAME')


TIME_STAMP = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
data = TIME_STAMP
acordo = 1
codigo = '20'
cedente = 'PAG'
cpf = '111.111.111-11'
parcela = 1
url = 'https://kitei.com.br'


class Download(BaseModel):
    dt_download: str
    id_acordo: int
    cd_cedente: str
    nm_cedente: str
    tx_cpf: str
    id_parcela: int
    tx_url: str


def open_connection():
    result = pymysql.connect(
        host=DB_SERVER,
        user=DB_USER,
        password=DB_PWD,
        database=DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    return result


conn = open_connection()

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get('/')
def get_downloads(token: str = Depends(oauth2_scheme)):
    dbcon = open_connection()
    cursor = dbcon.cursor()
    cmd = 'SELECT id, dt_download, id_acordo, cd_cedente, nm_cedente, tx_cpf, id_parcela, tx_url ' \
          'FROM kiteiboleto.download ' \
          'ORDER BY dt_download , cd_cedente , id_acordo'
    cursor.execute(cmd)
    result = cursor.fetchall()
    print(result)
    cursor.close()
    #return {"message": result}
    return {"token": token}


@app.post('/items/', status_code=status.HTTP_201_CREATED)
def create_download(item: Download, request: Request):
    client_host = request.client.host
    client_url = request.url.path

    item_dict = item.dict()
    data = item.dt_download
    acordo = item.id_acordo
    codigo = item.cd_cedente
    cedente = item.nm_cedente
    cpf = item.tx_cpf
    parcela = item.id_parcela
    url = item.tx_url

    dbcon = open_connection()
    cursor = dbcon.cursor()
    cmd = 'INSERT INTO kiteiboleto.download '\
          '(dt_download,id_acordo,cd_cedente,nm_cedente,tx_cpf,id_parcela,tx_url,client_host,client_url) ' \
          f'VALUES ("{data}",{acordo},"{codigo}","{cedente}","{cpf}",{parcela},"{url}","{client_host}","{client_url}")'
    cursor.execute(cmd)
    cursor.close()
    return {"message": "create download item"}


@app.patch('/{downloadId}')
def update_download(downloadId: str):
    return {"message": f"update download item with id {downloadId}"}


@app.get('/{downloadId}')
def get_download(downloadId: str):
    return {"message": f"get download item with id {downloadId}"}


@app.delete('/{downloadId}')
def delete_download(downloadId: str):
    return {"message": f"delete download item with id {downloadId}"}


@app.get("/download/healthchecker")
def root():
    return {"message": "Welcome to KITEI - Get Download Boleto info"}


if __name__ == '__main__':
    uvicorn.run(app=app, host=SERVER_APP_URL, port=SERVER_APP_PORT)
