# constants
from enum import Enum

class VALUE_TYPES(Enum):
    TYPE_BLUE = 'Dólar blue'
    TYPE_OFICIAL = 'Dólar oficial promedio'
    TYPE_BOLSA = 'Dólar Bolsa'
    TYPE_LIQUI = 'Contado con liqui'
    TYPE_CRYPTO = 'Dólar cripto'
    TYPE_SOLIDARIO = 'Dólar solidario'

class VALUE_ACTIONS(Enum):
    ACTION_BUY = 'Compra'
    ACTION_SELL = 'Venta'