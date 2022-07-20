import pymongo
from datetime import datetime
from consts import MONGO_URI
from enums import VALUE_TYPES, VALUE_ACTIONS
import re

client = pymongo.MongoClient(MONGO_URI)
types_collection = client.db.types

defaultConstantValues = {
    "oficial": {
        "buy": 0,
        "sell": 0,
        "date": datetime.now(),
        "name": "",
        "_id": ""
    },
    "blue": {
        "buy": 0,
        "sell": 0,
        "date": datetime.now(),
        "name": "",
        "_id": ""
    },
    "bolsa": {
        "buy": 0,
        "sell": 0,
        "date": datetime.now(),
        "name": "",
        "_id": ""
    },
    "liqui": {
        "buy": 0,
        "sell": 0,
        "date": datetime.now(),
        "name": "",
        "_id": ""
    },
    "solidario": {
        "sell": 0,
        "date": datetime.now(),
        "name": "",
        "_id": ""
    },
    "cripto": {
        "buy": 0,
        "sell": 0,
        "date": datetime.now(),
        "name": "",
        "_id": ""
    },
    "creationDate": datetime.now()
}

# Return a shallow copy
# NOTE(hotfix): something strange is happening, default values are changing in the lifecyle

def setupDefaultValues():
    defaultValues = defaultConstantValues.copy()

    return defaultValues



# A function that parse soup elements to 'newValues' object


def soupResponseParser(soupValuesElements):
    valuesTypes = getTypesFromDbToList()
    newValues = setupDefaultValues()
    for soupValueElement in soupValuesElements:
        if soupValueElement:
            title = soupValueElement.previous
            contents = soupValueElement.contents
            for content in contents:
                if content.text != '':
                    extractIntegerFromText = re.findall(
                        r"[-+]?(?:\d*\.\d+|\d+)", content.text
                    )
                    finalPrice = float(extractIntegerFromText[0])

                    if title == VALUE_TYPES.TYPE_BLUE.value:
                        if content.text.startswith(VALUE_ACTIONS.ACTION_BUY.value):
                            newValues["blue"]["buy"] = finalPrice
                        if content.text.startswith(VALUE_ACTIONS.ACTION_SELL.value):
                            newValues["blue"]["sell"] = finalPrice

                        newValues["blue"]["name"] = valuesTypes[0]["name"]
                        newValues["blue"]["_id"] = valuesTypes[0]["_id"]

                    if title == VALUE_TYPES.TYPE_OFICIAL.value:
                        if content.text.startswith(VALUE_ACTIONS.ACTION_BUY.value):
                            newValues["oficial"]["buy"] = finalPrice
                        if content.text.startswith(VALUE_ACTIONS.ACTION_SELL.value):
                            newValues["oficial"]["sell"] = finalPrice

                        newValues["oficial"]["name"] = valuesTypes[2]["name"]
                        newValues["oficial"]["_id"] = valuesTypes[2]["_id"]

                    if title == VALUE_TYPES.TYPE_BOLSA.value:
                        if content.text.startswith(VALUE_ACTIONS.ACTION_BUY.value):
                            newValues["bolsa"]["buy"] = finalPrice
                        if content.text.startswith(VALUE_ACTIONS.ACTION_SELL.value):
                            newValues["bolsa"]["sell"] = finalPrice

                        newValues["bolsa"]["name"] = valuesTypes[1]["name"]
                        newValues["bolsa"]["_id"] = valuesTypes[1]["_id"]

                    if title == VALUE_TYPES.TYPE_LIQUI.value:
                        if content.text.startswith(VALUE_ACTIONS.ACTION_BUY.value):
                            newValues["liqui"]["buy"] = finalPrice
                        if content.text.startswith(VALUE_ACTIONS.ACTION_SELL.value):
                            newValues["liqui"]["sell"] = finalPrice

                        newValues["liqui"]["name"] = valuesTypes[3]["name"]
                        newValues["liqui"]["_id"] = valuesTypes[3]["_id"]

                    if title == VALUE_TYPES.TYPE_CRYPTO.value:
                        if content.text.startswith(VALUE_ACTIONS.ACTION_BUY.value):
                            newValues["cripto"]["buy"] = finalPrice
                        if content.text.startswith(VALUE_ACTIONS.ACTION_SELL.value):
                            newValues["cripto"]["sell"] = finalPrice

                        newValues["cripto"]["name"] = valuesTypes[5]["name"]
                        newValues["cripto"]["_id"] = valuesTypes[5]["_id"]

                    if title == VALUE_TYPES.TYPE_CRYPTO.value:
                        if content.text.startswith(VALUE_ACTIONS.ACTION_BUY.value):
                            newValues["solidario"]["buy"] = finalPrice
                        if content.text.startswith(VALUE_ACTIONS.ACTION_SELL.value):
                            newValues["solidario"]["sell"] = finalPrice

                        newValues["solidario"]["name"] = valuesTypes[4]["name"]
                        newValues["solidario"]["_id"] = valuesTypes[4]["_id"]

    newValues["creationDate"] = datetime.now()

    return newValues

# types of values relationship


def getTypesFromDbToList():
    types_db = types_collection.find({})
    return list(types_db)
