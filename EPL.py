from bs4 import BeautifulSoup
import requests
from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

def scrape(url):
  res = requests.get(url)
  soup = BeautifulSoup(res.text, 'html.parser')
  tbody = soup.find('div', class_="Table__TableWrapper-r2czfk-3 hezlIo")
  thead = soup.find('thead')
  headers = [th.text.strip() for th in thead.find_all('th')]
  for tr in tbody.find_all('tr', class_="Table__TableRow-r2czfk-8 dwCAtX"):
    row_data = [td.text.strip() for td in tr.find_all('td')]
  return row_data

def mongodb_Connection():
  client = MongoClient('mongodb://localhost:27017/')
  db = client['EPL_League']
  collection = db['standings']
  return collection
def insert_Data(data):
  table_Data = connect_to_mongodb()
  table_Data.insert_many(data)
def fetch_Data():
  table_Data = connect_to_mongodb()
  final_Data = list(table_Data.find({}, {'_id': 0}))
  return final_Data

@app.route('/api/leagueStandings/db', methods=['GET'])
def db_API():
  url = "https://www.sportinglife.com/football/league-tables/english-premier-league/1"
  league_Table = scrape(url)
  print(league_Table)
  insert_Data(league_Table)
  fetched_Data = fetch_Data()
  return jsonify(fetched_Data)

if __name__ == "__main__":
  app.run(port=80, debug=True)
