# -*- coding: utf-8 -*-

from .utils import float2string

import asyncio
import urllib.parse

import ed25519
import requests


class Exchanger(object):
    PREFIX_URL = "https://picostocks.com/api/v1/"

    def __init__(self, private_key, user_id):
        self.private_key = private_key
        self.user_id = user_id

        self.signing_key = ed25519.SigningKey(self.private_key, encoding='hex')

        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'picostocks/python'})

    async def _get_order_request_data(self, sign_key, stock_id, price_id, quantity, price):
        nonce_resp = await self.get_nonce()

        sign_message = ":".join([
            sign_key,
            str(self.user_id),
            str(stock_id),
            float2string(quantity),
            str(price_id),
            float2string(price),
            str(nonce_resp['nonce'])
        ])

        return {
            'user_id': self.user_id,
            'stock_id': stock_id,
            'quantity': quantity,
            'price_id': price_id,
            'price': price,
            'signature': self.signing_key.sign(sign_message.encode(), encoding='hex')
        }

    async def _get(self, rel_url, params=None):
        loop = asyncio.get_event_loop()
        url = urllib.parse.urljoin(self.PREFIX_URL, rel_url)
        return await loop.run_in_executor(
            None, lambda: self.session.get(url, params=params))

    async def _post(self, rel_url, data=None, params=None):
        loop = asyncio.get_event_loop()
        url = urllib.parse.urljoin(self.PREFIX_URL, rel_url)
        return await loop.run_in_executor(
            None, lambda: self.session.post(url, data=data, params=params))

    async def get_nonce(self):
        response = await self._get("account/nonce/%s/" % self.user_id)
        return response.json()

    async def get_order_book(self, stock_id, price_id, limit=100):
        params = {'stock_id': stock_id, 'price_id': price_id}
        response = await self._get("market/orderbook/", params=params)
        return response.json()

    async def get_assets_balance(self, user_id=None):
        if user_id is None:
            user_id = self.user_id

        response = await self._get("account/balance/%s/" % user_id)
        return response.json()

    async def get_open_orders(self, stock_id, price_id, user_id=None, limit=100):
        if user_id is None:
            user_id = self.user_id

        params = {
            'stock_id': stock_id,
            'price_id': price_id,
            'user_id':user_id
        }

        response = await self._get("market/orderbook/", params=params)
        return response.json()

    async def get_historical_orders(self, stock_id):
        response = await self._get(
            'account/%s/%s/' % (self.user_id, stock_id))
        return response.json()

    async def get_transfers_internal(self, stock_id):
        response = await self._get(
            'account/transfers/internal/%s/%s/' % (self.user_id, stock_id))
        return response.json()

    async def get_transfers_external(self, stock_id):
        response = await self._get(
            'account/transfers/internal/%s/%s/' % (self.user_id, stock_id))
        return response.json()

    async def put_ask(self, stock_id, price_id, quantity, price):
        request_data = await self._get_order_request_data("ASK", stock_id, price_id, quantity, price)
        response = await self._post("trader/ask/put/", request_data)
        return response.json()

    async def cancel_ask(self, stock_id, price_id, quantity, price):
        request_data = await self._get_order_request_data("CANCELASK", stock_id, price_id, quantity, price)
        response = await self._post("trader/ask/cancel/", request_data)
        return response.json()

    async def put_bid(self, stock_id, price_id, quantity, price):
        request_data = await self._get_order_request_data("BID", stock_id, price_id, quantity, price)
        response = await self._post("trader/bid/put/", request_data)
        return response.json()

    async def cancel_bid(self, stock_id, price_id, quantity, price):
        request_data = await self._get_order_request_data("CANCELBID", stock_id, price_id, quantity, price)
        response = await self._post("trader/bid/cancel/", request_data)
        return response.json()

    async def get_stocks(self):
        response = await self._get("market/stocks/")
        return response.json()


if __name__ == '__main__':
    # Example usage
    exchanger = Exchanger(private_key=b'<private_key>', user_id='<user_id>')
    loop = asyncio.get_event_loop()
    open_orders_resp = loop.run_until_complete(exchanger.get_stocks())
    print(open_orders_resp)
