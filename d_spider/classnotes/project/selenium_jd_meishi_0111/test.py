from selenium import webdriver
import pymongo
# browser = webdriver.Chrome()
# browser.get('https://www.jd.com/')

client = pymongo.MongoClient('localhost', 27017)
db = client.pachong

collection = db.jd_meishi

a = collection.find({'img_url': 'https:/123'})
b = collection.delete_many({'img_url': 'https:/123'})

print(collection.delete_many({'img_url': 'https:/123'}))
