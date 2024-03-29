import requests
from pprint import pprint
from config import config
import datetime
import json
import os
from config import RESULTS_FOLDER


def get_trafficologists_expenses():
    base_url = "https://cloud.roistat.com/api/v1/"
    api_key = config["roistat"]["api_key"]
    project_id = config["roistat"]["project_id"]
    auth_ = f"?key={api_key}&project={project_id}"

    start_date = datetime.date(2021, 3, 1)
    end_date = datetime.date.today()
    delta = datetime.timedelta(days=1)

    expenses = []

    while start_date <= end_date:
        cur_day_start = start_date.strftime("%Y-%m-%d") + "T00:00:00+0300"
        cur_day_end = start_date.strftime("%Y-%m-%d") + "T23:59:59+0300"
        params = {
            "dimensions": ["marker_level_1"],
            "metrics": ["marketing_cost", "visitsCost"],
            "period": {"from": cur_day_start, "to": cur_day_end},
        }

        url = f"{base_url}project/analytics/data{auth_}"
        response = requests.post(url=url, json=params)
        channels = response.json()["data"][0]["items"]
        channels_dict = {}
        for channel in channels:
            channel_name = channel["dimensions"]["marker_level_1"]["title"].replace(
                "\xa0", " "
            )
            channel_expense = channel["metrics"][0]["value"]
            channels_dict.update({channel_name: channel_expense})

        expenses.append(
            {"dateFrom": cur_day_start, "dateTo": cur_day_end, "items": channels_dict}
        )
        start_date += delta

    return expenses


def get_trafficologists_expenses_levels():
    base_url = "https://cloud.roistat.com/api/v1/"
    api_key = config["roistat"]["api_key"]
    project_id = config["roistat"]["project_id"]
    auth_ = f"?key={api_key}&project={project_id}"

    start_date = datetime.date(2021, 3, 1)
    end_date = datetime.date.today()
    delta = datetime.timedelta(days=1)

    expenses = []

    while start_date <= end_date:
        cur_day_start = start_date.strftime("%Y-%m-%d") + "T00:00:00+0300"
        cur_day_end = start_date.strftime("%Y-%m-%d") + "T23:59:59+0300"
        params = {
            "dimensions": ["marker_level_1", "marker_level_3"],
            "metrics": ["visitsCost"],
            "period": {"from": cur_day_start, "to": cur_day_end},
        }

        url = f"{base_url}project/analytics/data{auth_}"
        response = requests.post(url=url, json=params)
        channels = {}
        for channel in response.json().get("data", [{}])[0].get("items", []):
            level1 = channel.get("dimensions", {}).get("marker_level_1", {})
            level3 = channel.get("dimensions", {}).get("marker_level_3", {})
            level1_title = level1.get("title").replace("\xa0", " ")
            level3_title = level3.get("title").replace("\xa0", " ")
            if level1_title not in channels.keys():
                channels[level1_title] = {"channels": {}}
            metrics = channel.get("metrics", [])
            for metric in metrics:
                if metric.get("metric_name") == "visitsCost" and metric.get("value"):
                    channels[level1_title]["channels"][level3_title] = metric.get(
                        "value"
                    )
        for channel in channels.values():
            channel.update(
                {
                    "total": sum(
                        list(map(lambda item: item, channel.get("channels").values()))
                    )
                }
            )

        expenses.append(
            {"dateFrom": cur_day_start, "dateTo": cur_day_end, "items": channels}
        )
        start_date += delta

    return expenses


if __name__ == "__main__":
    # expenses = get_trafficologists_expenses()
    # with open(os.path.join(RESULTS_FOLDER, 'expenses.json'), 'w') as f:
    #     json.dump(expenses, f)
    # with open(os.path.join(RESULTS_FOLDER, 'expenses.json'), 'r', encoding='cp1251') as f:
    #     expenses = json.load(f)
    # pprint(expenses)

    start_date = datetime.date(2022, 6, 1)
    end_date = datetime.date(2022, 6, 12)
    # end_date = datetime.date.today()
    delta = datetime.timedelta(days=1)
    cur_day_start = start_date.strftime("%Y-%m-%d") + "T00:00:00+0300"
    cur_day_end = end_date.strftime("%Y-%m-%d") + "T23:59:59+0300"

    print(start_date, end_date, cur_day_start, cur_day_end)

    base_url = "https://cloud.roistat.com/api/v1/"
    api_key = config["roistat"]["api_key"]
    project_id = config["roistat"]["project_id"]
    auth_ = f"?key={api_key}&project={project_id}"
    params = {
        "dimensions": ["marker_level_1"],
        "metrics": ["marketing_cost", "visitsCost"],
        "period": {"from": cur_day_start, "to": cur_day_end},
    }
    url = f"{base_url}project/analytics/data{auth_}"
    # url = f'{base_url}{dimensions}{auth_}'
    response = requests.post(url=url, json=params)
    print(response.status_code)
    channels = response.json()
    with open("test_expenses.json", "w") as f:
        json.dump(channels, f)
    pprint(channels)
