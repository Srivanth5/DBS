from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
from flask import Flask

app=Flask(__name__)
def scrape_books(url):
  Res= requests.get(url)
  soup = BeautifulSoup(Res.text,'html.parser')
  books = []
  for book in soup.find_all('article', class_='product_pod'):
    title = book.find('h3').find('a')['title']
    price = book.find('p', class_='price_color').text.strip()
    books.append({
      'title':title,
      'price':price,
    })
  return books
@app.route('/api/books',methods=['GET'])
def db_Data(data,coll_name):
  client = MongoClient('mongodb://localhost:27017/')
  db = client['bookstore']
  collection = db[coll_name]
  collection.insert_many(data)
def flask_Api():
  url = "https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"
  fantasy_books = scrape_books(url)
  return fantasy_books
if __name__ == "__main__":
  #db_Data(fantasy_books,'fantasyBooks')
  app.run(debug=True)
