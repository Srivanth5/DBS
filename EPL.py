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
    headers.append(th.text.strip())

  rows = []
  for tr in tbody.find_all('tr', class_="Table__TableRow-r2czfk-8 dwCAtX"):
    row_data = []
    for td in tr.find_all('td'):
      row_data.append(td.text.strip())
      rows.append(dict(zip(headers, row_data)))
  return rows

def mongodb_Connection():
  client = MongoClient('mongodb://localhost:27017/')
  db = client['EPLLeague']
  collection = db['standings']
  return collection
def insert_Data(data):
  table = mongodb_Connection()
  table.insert_many(data)
def fetch_Data():
  table_Data = mongodb_Connection()
  final_Data = list(table_Data.find({}, {'_id': 0}))
  return final_Data
def create_and_populate_db():
  url = "https://www.sportinglife.com/football/league-tables/english-premier-league/1"
  league_Table = scrape(url)
  insert_Data(league_Table)

create_and_populate_db()

app = Flask(__name__)

@app.route('/api/leagueStandings/db', methods=['GET'])

def db_API():
  fetched_Data = fetch_Data()
  return jsonify(fetched_Data)

if __name__ == "__main__":
  app.run(port=8080, debug=True, use_reloader=False)
