from config import config
import pandas as pd
import pymysql
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from config import CREDENTIALS_FILE
from .preprocessing import preprocess_dataframe, preprocess_target_audience
from config import RESULTS_FOLDER
import os
import pickle as pkl

def load_sheet(spreadsheetId, sheetName, majorDimension, startRow=1, headers=True, additional_columns=0):
    """
        Read sheet by name from google spreadsheet
        input:
            spreadsheetId - id таблицы
            sheetName - имя листа
            majorDimension - размерность считывания (строки/столбцы)
            startRow - стартовая строка с данными
            headers - считывать 0-ю строку как заголовок
        output:
            df - датафрейм с данными из считанного листа таблицы
    """
    # Читаем ключи из файла
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'])

    httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API

    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId,
        range=sheetName,
        majorDimension=majorDimension
    ).execute()
    values = values['values']
    if headers:
        df = pd.DataFrame(values[startRow:], columns=values[0] + [''] * additional_columns)
    else:
        df = pd.DataFrame(values[startRow:], columns=None)
    return df

def write_sheet(spreadsheetId, startCell, endCell, majorDimension, values):
    # Читаем ключи из файла
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'])

    httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API
    results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
        "valueInputOption": "USER_ENTERED",
        # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": startCell + ':' + endCell,
            "majorDimension": majorDimension,  # Сначала заполнять строки, затем столбцы
            "values": values
            }
        ]
    }).execute()
    return None

def connect():
    connection = pymysql.connections.Connection(**config['database'])
    cursor = connection.cursor(pymysql.cursors.DictCursor)
    return connection, cursor

def get_leads_data():
    conn, cursor = connect()
    query = "SELECT * FROM leads WHERE traffic_channel NOT IN ('https://neural-university.ru/terra_ai_education_new',\
                                                               'https://neural-university.ru/python_new',\
                                                               'https://neural-university.ru/python_analysis_2',\
                                                               'https://neural-university.ru/python_data_analysis')"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    data = pd.DataFrame(data)
    with open(os.path.join(RESULTS_FOLDER, 'additional_leads.pkl'), 'rb') as f:
        additional_leads = pkl.load(f)
    data = pd.concat([data, additional_leads], axis=0)
    data = data.sort_values(by='created_at')
    data.fillna(0, inplace=True)
    df = preprocess_dataframe(data)
    df['channel_expense'].fillna(0, inplace=True)
    df['payment_amount'] = df['payment_amount'].astype(float)
    df['channel_expense'] = df['channel_expense'].astype(float)
    return df

def get_trafficologist_data():
    conn, cursor = connect()
    query = "SELECT label, title, name FROM trafficologists, accounts WHERE accounts.trafficologist_id=trafficologists.id LIMIT 1000"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    account = {d['label']: d['title'] for d in data}
    trafficologist = {d['label']: d['name'] for d in data}
    return account, trafficologist

def get_accounts():
    conn, cursor = connect()
    query = "SELECT accounts.id, label, title, name FROM trafficologists, accounts WHERE accounts.trafficologist_id=trafficologists.id"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    data = pd.DataFrame(data)
    return data

def get_trafficologists():
    conn, cursor = connect()
    query = "SELECT id, name FROM trafficologists"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return pd.DataFrame(data)

def add_trafficologist(name):
    conn, cursor = connect()
    query = "INSERT INTO trafficologists (name) VALUES (%s)"
    cursor.execute(query, (name,))
    conn.commit()
    conn.close()

def delete_trafficologist(id):
    conn, cursor = connect()
    query = "DELETE FROM trafficologists WHERE id=%s"
    cursor.execute(query, (id,))
    conn.commit()
    conn.close()

def add_account(title, label, trafficologist_id):
    conn, cursor = connect()
    query = "INSERT INTO accounts (title, label, trafficologist_id) VALUES (%s, %s, %s)"
    cursor.execute(query, (title, label, trafficologist_id))
    conn.commit()
    conn.close()

def delete_account(id):
    conn, cursor = connect()
    query = "DELETE FROM accounts WHERE id=%s"
    cursor.execute(query, (id,))
    conn.commit()
    conn.close()
    
def get_countries():
    conn, cursor = connect()
    query = "SELECT DISTINCT quiz_answers1 as country FROM leads"
    cursor.execute(query)
    data = cursor.fetchall()
    arr = [d['country'] for d in data]
    conn.close()
    return arr

def get_ages():
    conn, cursor = connect()
    query = "SELECT DISTINCT quiz_answers2 as age FROM leads"
    cursor.execute(query)
    data = cursor.fetchall()
    arr = [d['age'] for d in data]
    conn.close()
    return arr

def get_jobs():
    conn, cursor = connect()
    query = "SELECT DISTINCT quiz_answers3 as job FROM leads"
    cursor.execute(query)
    data = cursor.fetchall()
    arr = [d['job'] for d in data]
    conn.close()
    return arr

def get_earnings():
    conn, cursor = connect()
    query = "SELECT DISTINCT quiz_answers4 as earning FROM leads"
    cursor.execute(query)
    data = cursor.fetchall()
    arr = [d['earning'] for d in data]
    conn.close()
    return arr

def get_trainings():
    conn, cursor = connect()
    query = "SELECT DISTINCT quiz_answers5 as training FROM leads"
    cursor.execute(query)
    data = cursor.fetchall()
    arr = [d['training'] for d in data]
    conn.close()
    return arr

def get_times():
    conn, cursor = connect()
    query = "SELECT DISTINCT quiz_answers6 as time FROM leads"
    cursor.execute(query)
    data = cursor.fetchall()
    arr = [d['time'] for d in data]
    conn.close()
    return arr

# Подключаем библиотеки

def get_target_audience():
    spreadsheet_id = '1_kytD9tww-2ETFOp46Av75PndibaoFzgHKV46fxHEWY'
    # Читаем ключи из файла
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'])

    httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API

    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A1:A996',
        majorDimension='COLUMNS'
    ).execute()

    return preprocess_target_audience(values['values'][0])

def get_status():
    try:
        return pd.read_csv('data/status.csv')
    except FileNotFoundError:
        return pd.read_csv('dags/data/status.csv')

