from bs4 import BeautifulSoup
import requests
from flask import Flask, jsonify
from pymongo import MongoClient

def scrape(url):
  res = requests.get(url)
  soup = BeautifulSoup(res.text, 'html.parser')
  tbody = soup.find('div', class_="Table__TableWrapper-r2czfk-3 hezlIo")
  thead = soup.find('thead')
  headers = []
  for th in thead.find_all('th'):
    header_text = th.text.strip().replace(' ', '_').lower()
    headers.append(header_text)

  rows = []
  for tr in tbody.find_all('tr', class_="Table__TableRow-r2czfk-8 dwCAtX"):
    row_data = []
    for td in tr.find_all('td'):
      data_text = td.text.strip().replace(',', '')
      try:
          data_text = float(data_text)
      except ValueError:
          pass
      row_data.append(data_text)
    rows.append(dict(zip(headers, row_data)))
  return rows

def connect():
  client = MongoClient('mongodb://localhost:27017/')
  db = client['EPLLeague']
  collection = db['standings']
  return collection
def insert(data):
  table = connect()
  table.insert_many(data)
def get():
  table_Data = connect()
  final_Data = list(table_Data.find({}, {'_id': 0}))
  return final_Data
def scraped_data():
  url = "https://www.sportinglife.com/football/league-tables/english-premier-league/1"
  league_Table = scrape(url)
  insert(league_Table)

scraped_data()

app = Flask(__name__)

@app.route('/api/leagueStandings/db', methods=['GET'])

def db_API():
  fetched_Data = get()
  return jsonify(fetched_Data)


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)