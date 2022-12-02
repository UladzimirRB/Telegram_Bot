import requests
import json
from config import keys

class ConvertionException (Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price (quote:str, base:str,amount:str):

        if type(quote) == str and type(base) == str:
            if quote == base:
                raise ConvertionException (f"Вы ввели одинаковые валюты ({quote})! ")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException (f"не удалось обработать валюту {quote}")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f"не удалось обработать валюту {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"не удалось обработать количество {amount}, введите цифры")

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        summ = float(total_base)*float(amount)
        summ = round(summ,2)

        return summ