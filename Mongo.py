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
def db_Data(data,coll_name):
  client = MongoClient('mongodb://localhost:27017/')
  db = client['bookstore']
  collection = db[coll_name]
  collection.insert_many(data)
if __name__ == "__main__":
  url = "https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"
  fantasy_books = scrape_books(url)
  collection.insert_many(books)
  db_Data(Books,'fantasyBooks')
