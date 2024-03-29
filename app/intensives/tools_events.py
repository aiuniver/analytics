import pickle
import time
import pandas
import pandas as pd
import gspread
import re
from datetime import datetime, timedelta
from config import DATA_FOLDER
from pathlib import Path
from pandas import Timestamp


def format_percent(x):
    return '{:.2%}'.format(x)


# Получение оплат
def get_payment(date_from: str) -> pd.DataFrame:
    # Авторизация по сервисному аккаунту
    gc = gspread.service_account(filename='app/intensives/intensives-394715-16cd73454d4f.json')
    # Открытие таблицы
    table_main = gc.open('Аналитика по оплатам')
    # Получение первого листа (worksheet)
    worksheet = table_main.get_worksheet(0)
    data = worksheet.get_all_values()
    # Заворачиваем в dataframe
    df = pd.DataFrame(data[1:], columns=data[0])
    # оставляем все строки и только нужные столбцы
    df = df[["Почта", "Сумма выручки", "Дата оплаты", "Месяц / Доплата"]]
    # Переименовываем столбцы и передаем словарь с новыми именами
    new_column_name = ['email', 'price', 'date', 'type']
    df = df.rename(columns=dict(zip(df.columns, new_column_name)))
    # Преобразуем данные в datatime
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
    # Заменить все неразрывные пробелы '\xa0' на обычные пробелы
    df['price'] = df['price'].str.replace('\xa0', ' ')
    # Удалить все символы, кроме цифр и пробелов
    df['price'] = df['price'].str.replace(r'[^\d\s]', '', regex=True)
    df['price'] = df['price'].str.replace(' ', '')
    df['price'] = df['price'].astype(int)
    df['email'] = df['email'].str.lower()
    # Делаем выборку данных
    selected_data = df[(df['date'] >= pd.to_datetime(date_from)) & (df['type'] != 'доплата')]
    # Фрейм диапазона для обработки в функции просмотра таблиц мероприятий
    explore_frame = selected_data.loc[:, ['email', 'price', 'date']]
    return explore_frame


# Получение БД из pkl
def data_preparation(start_event: str, end_event: str, select_event: list) -> pd.DataFrame:
    start = datetime.strptime(start_event, '%Y-%m-%d')
    end = datetime.strptime(end_event, '%Y-%m-%d')

    file_preorders = Path(DATA_FOLDER) / 'week' / 'intensives_preorders.pkl'
    file_registrations = Path(DATA_FOLDER) / 'week' / 'intensives_registrations.pkl'
    file_members = Path(DATA_FOLDER) / 'week' / 'intensives_members.pkl'

    # Чтение данных из файла .pkl
    data_preorders = pandas.read_pickle(file_preorders)
    data_registrations = pandas.read_pickle(file_registrations)
    data_members = pandas.read_pickle(file_members)

    # Подготовка таблиц
    preorders: pandas.DataFrame = data_preorders
    preorders.insert(0, 'type', 'Предзаказы', False)

    registrations: pandas.DataFrame = data_registrations
    registrations.insert(0, 'type', 'Регистрации', False)
    registrations.loc[registrations['course'] == 'Акции', 'type'] = 'Предзаказы'

    members: pandas.DataFrame = data_members
    members.insert(0, 'type', 'Участники', False)

    # Сборка единого frame
    full_frame = pd.concat([preorders, registrations, members], ignore_index=True)
    full_frame['date'] = pd.to_datetime(full_frame['date'])
    full_frame['email'] = full_frame['email'].str.lower()
    # Выбор данных из диапазона
    filtered_frame = full_frame[(full_frame['date'] >= start) & (full_frame['date'] <= end)]
    # Фильтруем выбранные мероприятия
    if select_event[0] == 'Все':
        return filtered_frame
    else:
        filtered_frame = filtered_frame[filtered_frame['course'].isin(select_event)]
    return filtered_frame


# Формирование отчета
def get_funnel_payment(start_event: str, end_event: str, start_pay: str, end_pay: str,
                       select_event: list) -> pd.DataFrame:
    # Это значение нужно для того, чтобы понимать на сколько дней сдвигать динамический фильтр массива оплат
    start_date = datetime.strptime(start_pay, "%Y-%m-%d")
    end_date = datetime.strptime(end_pay, "%Y-%m-%d")
    date_difference = end_date - start_date
    # Преобразование разницы в количество дней (целое число)
    date_difference_in_days = date_difference.days
    # Получаем данные из БД
    dataset = data_preparation(start_event, end_event, select_event).fillna('empty').drop_duplicates()
    # Получаем df оплат
    payments = get_payment(start_pay)
    # Результирующий dataframe
    result_dataframe = pd.DataFrame(
        columns=['date', 'event', 'full_price', 'reg_price', 'peop_price', 'so_price', 'email'])
    # Логика работает от почты из набора документов
    for items in dataset.itertuples():
        # заходим в документ оплат и ищем там почту
        for row in payments.itertuples():
            if items[4] == row[1] and pd.Timestamp(items[3]) <= row[3] <= pd.Timestamp(
                    items[3] + timedelta(days=date_difference_in_days)):
                price_reg = row[2] if items[1] == 'Регистрации' else 0
                price_mem = row[2] if items[1] == 'Участники' else 0
                price_pre = row[2] if items[1] == 'Предзаказы' else 0
                rows = [items[3], items[2], row[2], price_reg, price_mem, price_pre,items[4]]
                result_dataframe.loc[len(result_dataframe)] = rows
    # Собираем финальный df
    int_columns = ['full_price', 'reg_price', 'peop_price', 'so_price']
    result_dataframe[int_columns] = result_dataframe[int_columns].astype(int)
    result_dataframe = result_dataframe.groupby(['date', 'event', 'email']).agg(
        {'full_price': 'max', 'reg_price': 'max', 'peop_price': 'max', 'so_price': 'max'}).reset_index()
    grouped = result_dataframe.groupby(['date', 'event']).agg(
        {'full_price': 'sum', 'reg_price': 'sum', 'peop_price': 'sum', 'so_price': 'sum'}).reset_index()
    grouped['%reg'] = grouped['reg_price'] / grouped['full_price']
    grouped['%peop'] = grouped['peop_price'] / grouped['full_price']
    grouped['%so'] = grouped['so_price'] / grouped['full_price']
    # Применяем форматирование вывода
    grouped['%reg'] = grouped['%reg'].apply(format_percent)
    grouped['%peop'] = grouped['%peop'].apply(format_percent)
    grouped['%so'] = grouped['%so'].apply(format_percent)
    grouped = grouped.rename(columns={'date': 'Дата', 'event': 'Мероприятие', 'full_price': 'Оборот общий',
                                      'reg_price': 'Оборот с регистраций', 'peop_price': 'Оборот с участников',
                                      'so_price': 'Оборот с SO',
                                      '%reg': '% с регистраций', '%peop': '% с участников', '%so': '% с предзаказов'})
    return grouped


def get_report(start_event: str, end_event: str, custom_period: str, select_checkbox: list,
               select_event: list) -> pd.DataFrame:
    # Фильтры
    event_from = start_event
    event_to = end_event
    filter_event = select_event

    # Возвращаемая таблица
    result_table = pd.DataFrame()

    # Работа с фильтрами
    if custom_period:
        start_date_custom, end_date_custom = custom_period.split(' - ')
        start_date_pay = start_date_custom
        end_date_pay = end_date_custom
        result_table = get_funnel_payment(event_from, event_to, start_date_pay, end_date_pay, filter_event)

    elif select_checkbox:
        checkbox_values = {
            '1week': 7,
            '2week': 14,
            '4week': 28,
            '8week': 56
        }
        if len(select_checkbox) == 1:
            start_date_pay = event_from
            end_date_pay = (datetime.strptime(event_from, '%Y-%m-%d') + timedelta(
                days=checkbox_values.get(select_checkbox[0]))).strftime('%Y-%m-%d')
            result_table = get_funnel_payment(event_from, event_to, start_date_pay, end_date_pay, filter_event)
        else:
            final_table = pd.DataFrame()
            for select in select_checkbox:
                start_date_pay = event_from
                end_date_pay = (datetime.strptime(event_from, '%Y-%m-%d') + timedelta(
                    days=checkbox_values.get(select))).strftime('%Y-%m-%d')

                table = get_funnel_payment(event_from, event_to, start_date_pay, end_date_pay, filter_event)
                # Data-frame шапка
                title_df = pd.DataFrame([[select]], columns=['Срез'])
                # Преобразование всей таблицы в строковый тип
                table = table.astype(str)
                # Объедините данные: title_df + данные из table
                combined_table = pd.concat([title_df, table], ignore_index=True)
                # Замена NaN на пустую строку
                combined_table = combined_table.fillna('')
                # Добавление текущей combined_table к final_table
                final_table = pd.concat([final_table, combined_table], ignore_index=True)
            result_table = final_table
    return result_table
