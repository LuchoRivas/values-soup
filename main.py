from bs4 import BeautifulSoup
import requests
import time
import pymongo
from datetime import datetime
from bson.objectid import ObjectId
from consts import MONGO_URI
from bson.json_util import dumps
import locale

locale.setlocale(locale.LC_ALL, 'es_AR.utf8')
client = pymongo.MongoClient(MONGO_URI)
collection = client.db.values
types_collection = client.db.types


def __eq__(self, other):
    return ((self["blue"]["buy"] == other["blue"]["buy"]) and (self["blue"]["sell"] == other["blue"]["sell"]))

# main


def getValues():
    url = "https://www.dolarhoy.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    prices = soup.find_all('span', class_='price')
    precio_compra_oficial = prices[0].text.strip()
    precio_venta_oficial = prices[1].text
    precio_compra_blue = prices[2].text
    precio_venta_blue = prices[3].text
    precio_compra_bolsa = prices[4].text
    precio_venta_bolsa = prices[5].text
    precio_compra_liqui = prices[6].text
    precio_venta_liqui = prices[7].text
    precio_venta_solidario = prices[8].text

    newValues = {
        "oficial": {
            "buy": locale.atof(precio_compra_oficial.strip("$")),
            "sell": locale.atof(precio_venta_oficial.strip("$")),
            "date": datetime.now()
        },
        "blue": {
            "buy":  locale.atof(precio_compra_blue.strip("$")),
            "sell": locale.atof(precio_venta_blue.strip("$")),
            "date": datetime.now()
        },
        "bolsa": {
            "buy": locale.atof(precio_compra_bolsa.strip("$")),
            "sell": locale.atof(precio_venta_bolsa.strip("$")),
            "date": datetime.now()
        },
        "liqui": {
            "buy": locale.atof(precio_compra_liqui.strip("$")),
            "sell": locale.atof(precio_venta_liqui.strip("$")),
            "date": datetime.now()
        },
        "solidario": {
            "sell": locale.atof(precio_venta_solidario.strip("$")),
            "date": datetime.now()
        },
        "creationDate": datetime.now()
    }

    # last registry from mongo db
    dbValues = getDbValues()

    if(dbValues == None):
        values_to_save = addTypes(newValues)
        saveValues(values_to_save)

    else:
        # compare mongo db with newValues, if __eq__ is false save a new values
        equals = __eq__(dbValues, newValues)
        if(equals):
            return
        else:
            values_to_save = addTypes(newValues)
            saveValues(values_to_save)

# types of values relationship


def addTypes(values):
    types_db = types_collection.find({})
    types = list(types_db)

    for value in values:
        if(value == "blue"):
            blue = values["blue"]
            blue["name"] = types[0]["name"]
            blue["_id"] = types[0]["_id"]
            values["blue"] = blue
        if(value == "bolsa"):
            bolsa = values["bolsa"]
            bolsa["name"] = types[1]["name"]
            bolsa["_id"] = types[1]["_id"]
            values["bolsa"] = bolsa
        if(value == "oficial"):
            oficial = values["oficial"]
            oficial["name"] = types[2]["name"]
            oficial["_id"] = types[2]["_id"]
            values["oficial"] = oficial
        if(value == "liqui"):
            liqui = values["liqui"]
            liqui["name"] = types[3]["name"]
            liqui["_id"] = types[3]["_id"]
            values["liqui"] = liqui
        if(value == "solidario"):
            solidario = values["solidario"]
            solidario["name"] = types[4]["name"]
            solidario["_id"] = types[4]["_id"]
            values["solidario"] = solidario

    return values

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
        cursor = collection.find_one({}, {'_id': 0, 'creationDate': 0}, sort=[
                                     ('_id', pymongo.DESCENDING)])
        return cursor

    except Exception as e:
        print('an error occurred trying get values from db >>', e)


def execute():
    getValues()
    time.sleep(60)


while True:
    execute()
