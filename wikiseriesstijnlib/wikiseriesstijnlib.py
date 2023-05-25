#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: wikiseriesstijnlib.py
#
# Copyright 2023 Stijn Daniels
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Main code for wikiseriesstijnlib.

.. _Google Python Style Guide:
   https://google.github.io/styleguide/pyguide.html

"""

import logging
import requests
from bs4 import BeautifulSoup as Bfs
from pprint import pprint

__author__ = '''Stijn Daniels <stijn.githubemail@gmail.com>'''
__docformat__ = '''google'''
__date__ = '''25-05-2023'''
__copyright__ = '''Copyright 2023, Stijn Daniels'''
__credits__ = ["Stijn Daniels"]
__license__ = '''MIT'''
__maintainer__ = '''Stijn Daniels'''
__email__ = '''<stijn.githubemail@gmail.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


# This is the main prefix used for logging
LOGGER_BASENAME = '''wikiseriesstijnlib'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

series_overview = []
name = input('what series do you want to search? ')
api_url = 'https://en.wikipedia.org/w/api.php'
limit = 10
term = f'List_of_{name}_episodes'
parameters = {'action': 'opensearch',
              'format': 'json',
              'formatversion': '1',
              'namespace': '0',
              'limit': limit,
              'search': term}
response = requests.get(api_url, params=parameters, timeout=5)
url = response.json()[3][0]
series_response = requests.get(url, timeout=5)
soup = Bfs(series_response.text, features="html.parser")
tables = soup.find_all('table', {'class': 'wikitable'})[0]
try:
    seasons = [entry.text for entry in tables.find_all('span', {'class': 'nowrap'})]
except Exception as e:
    print(e)
episodetables = soup.find_all('table', {'class': 'wikiepisodetable'})
for season, episodetable in enumerate(episodetables):
    try:
        episodelist = [episode.text.split('"')[1] for episode in episodetable.find_all('td', {'class': 'summary'})]
        insert = {'season_name': seasons[season], 'season_episodes': episodelist}
        series_overview.append(insert)
    except Exception as e:
        print(f'something went wrong, error {e}, season = {season}, table = {episodetable}')

pprint(series_overview)
