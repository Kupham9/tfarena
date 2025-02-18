import requests as req
from bs4 import BeautifulSoup as bs
import json
import csv
import numpy as np
import pandas as pd

'''
    Creating a module for scraping and working with data pulled from TrendsTF
'''


def get_player_https_request(ID):
    http_request = req.get(f'https://trends.tf/player/{ID.strip()}/totals')

    if http_request.status_code == 404:
        print(f'Invalid ID: {ID}')
        return()
    else:
        return(http_request)
    

def extract_table_data(soup, heading):
    table = soup.find('h3', string=heading).find_next('table')
    data = {}
    for row in table.find_all('tr'):
        if 'header' in row.get('class', []):
            continue
        cells = row.find_all('td')
        if len(cells) >= 2:
            key = cells[0].get_text(strip=True)
            value = cells[1].get_text(strip=True)
            data[key] = value
    return data


def parse_player_data(http_request, ID):
    parsed_html = bs(http_request.text, 'html.parser')
    totals_data = extract_table_data(parsed_html, 'Totals')
    averages_data = extract_table_data(parsed_html, 'Averages')

    username = parsed_html.find('h1').get_text(strip=True)
    url = f'https://steamcommunity.com/profiles/{ID}'

    totals_list = list(totals_data.values())
    average_list = list(averages_data.values())

    return [username, ID , url] + totals_list + average_list


# def create_dataframe(header_filename):
#     return (pd.read_csv(header_filename, nrows=0))






