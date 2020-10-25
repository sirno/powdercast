"""Scrape wepowder snow forcast for powdercast."""
import re
import requests
from bs4 import BeautifulSoup


async def get_snow_heights():
    URL = "https://wepowder.com/en/andermatt"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    daily_content = soup.find_all(class_="tab-content")[-1]
    daily_left = daily_content.find_all(class_="table-holder left")
    dates = [date_head.tr.th.string for date_head in daily_left[0].find_all("thead")]
    daily_right = daily_content.find_all(class_="table-holder right")
    daily_weather = daily_right[0].find_all(class_="daily-weather")
    data = {}
    for day, day_weather in zip(dates, daily_weather):
        totals_row = day_weather.tbody.find_all("tr")[-1]
        data[day] = totals_row.find_all(string=re.compile("-|([0-9]{1,3}\.[0-9]cm)"))
    return data
