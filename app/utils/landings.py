import pandas as pd

from typing import Dict
from collections import defaultdict

from flask import current_app


def prepare(df, list_ca):
    all_dict = {
        "alias": {},
        "key": {},
        "base": defaultdict(
            lambda: {"indx": list(), "notCA": list(), "data": defaultdict(list)}
        ),
        "ca": defaultdict(list),
    }
    alias = all_dict["alias"]
    key = all_dict["key"]
    summ = all_dict["base"]
    ca_dict = all_dict["ca"]
    keys = ["Страна", "Возраст", "Профессия", "Доход", "Обучение", "Время"]
    for i in range(1, 7):
        alias[keys[i - 1]] = df.columns[i + 1]
    df["r2"] = [str(s).split("?")[0] for s in df["traffic_channel"]]
    r1all = df["r2"].unique().tolist()
    r1all.insert(0, "Все")
    all_dict["r1all"] = r1all
    for i in keys:
        _all = df[alias[i]].unique().tolist()
        not_ca_ages = list(set(_all) - set(list_ca))
        ca = list(set(_all) & set(list_ca))
        key[i] = ca
        sort_all = ca + not_ca_ages
        summ[i]["indx"] = sort_all
        summ[i]["notCA"] = not_ca_ages
        data = summ[i]["data"]
        inx = summ[i]["indx"]
        data["ЦА"] = [0] * len(r1all)
        for j in inx:
            for num, url in enumerate(r1all[1:]):
                amount = df[(df[alias[i]] == j) & (df["r2"] == url)].shape[0]
                data[j].append(amount)
                if j in ca:
                    data["ЦА"][num + 1] += amount
            data[j].insert(0, sum(data[j]))
        data["ЦА"][0] = sum(data["ЦА"][1:])
    for url in r1all[1:]:
        st = df[df["r2"] == url]
        st_col = st.shape[0]
        flag = True
        for ke in keys:
            st = st[st[alias[ke]].isin(list_ca)]
            st_new = st.shape[0]
            st_col = st_col - st_new
            if flag:
                ca_dict[url].append(st_col)
                flag = False
            ca_dict[url].append(st_new)
            st_col = st_new
    return all_dict


def color_ca(s):
    is_mos = s.index == "ЦА"
    return [
        "color: red; text-align: center" if v else "color: black; text-align: center"
        for v in is_mos
    ]


def landing(key, table, absolut=False):
    work = table["base"][key]
    df = pd.DataFrame(work["data"])
    df = df.T
    df.columns = table["r1all"]
    newind = table["key"][key] + ["ЦА"] + work["notCA"]
    df = df.reindex(newind)
    if absolut:
        for i in range(df.shape[0]):
            for j in range(1, df.shape[1]):
                df.iloc[i, j] = round((df.iloc[i, j] / df.iloc[i, 0]) * 100, 2)
        df.fillna(0, inplace=True)
        for i in range(df.shape[0]):
            for j in range(1, df.shape[1]):
                df.iloc[i, j] = str(df.iloc[i, j]) + "%"
        am = df["Все"].sum() - df.loc["ЦА", "Все"]
        df["Все"] = (100 * (df["Все"] / am)).round(2).astype(str) + "%"
    return df  # .style.apply(color_ca)


def fo_ca(base, table, absolut=False):
    df = pd.DataFrame(base["ca"], index=["0", "1", "2", "3", "4", "5", "6"])
    if absolut:
        for col in df.columns:
            s = table[table["r2"] == col].shape[0]
            for idx in df.index:
                df.loc[idx, col] = round(100 * (df.loc[idx, col] / s), 2)
                df.loc[idx, col] = str(df.loc[idx, col]) + "%"
    return df


def ca(base, table, absolut=False):
    new = {}
    bas = base["base"]
    for key in bas.keys():
        new[key] = bas[key]["data"]["ЦА"]
    df = pd.DataFrame(new, index=base["r1all"])
    df = df.T
    if absolut:
        for col in df.columns:
            s = table.shape[0]
            for idx in df.index:
                df.loc[idx, col] = round(100 * (df.loc[idx, col] / s), 2)
                df.loc[idx, col] = str(df.loc[idx, col]) + "%"
    return df


def calculate(tabl: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    pickle_app = current_app.app("pickle")

    target_audience = pickle_app.load("target_audience")

    dd = prepare(tabl, target_audience)
    result = {}
    for key in [*list(dd["alias"].keys()), "Попадание в ЦА", "ЦА по категориям"]:
        for ab in [True, False]:
            s = str(key) + " в процентах" if ab else key
            if key == "Попадание в ЦА":
                result[s] = fo_ca(dd, table=tabl, absolut=ab).T
            elif key == "ЦА по категориям":
                result[s] = ca(dd, table=tabl, absolut=ab).T
            else:
                result[s] = landing(key, table=dd, absolut=ab).T
    return result
