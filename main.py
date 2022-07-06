from bs4 import BeautifulSoup
import requests
import time
import pymongo
from consts import MONGO_URI
from values import soupResponseParser

client = pymongo.MongoClient(MONGO_URI)
collection = client.db.values

# TODO: improve this...
def __eq__(self, other):
    return ((self["blue"]["buy"] == other["blue"]["buy"]) and (self["blue"]["sell"] == other["blue"]["sell"]))

# main


def getValues():
    url = "https://www.dolarhoy.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    foundElements = soup.find_all('div', class_='values')
    valuesToSave = soupResponseParser(foundElements)

    # last registry from mongo db
    dbValues = getDbValues()

    if(dbValues == None):
        saveValues(valuesToSave)

    else:
        # compare mongo db with valuesToSave, if __eq__ is false save a new values
        equals = __eq__(dbValues, valuesToSave)
        if(equals):
            return
        else:
            saveValues(valuesToSave)



# try to save values to mongo db


def saveValues(values):
    try:
        collection.insert_one(values)
        print(f'inserted values!')

    except Exception as e:
        print('an error occurred trying to save values >>', e)

# gets the last saved values to compare with newValues


def getDbValues():
    try:
        cursor = collection.find_one(
            {},
            {'_id': 0, 'creationDate': 0},
            sort=[('_id', pymongo.DESCENDING)])
        return cursor

    except Exception as e:
        print('an error occurred trying get values from db >>', e)


def execute():
    getValues()
    time.sleep(60)


while True:
    execute()
