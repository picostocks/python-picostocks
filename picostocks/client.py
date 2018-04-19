# -*- coding: utf-8 -*-

from picostocks.utils import decimal2string

import asyncio
import urllib.parse

import ed25519
import requests


class Exchanger(object):
    PREFIX_URL = "http://localhost:8000/api/"

    def __init__(self, private_key, user_id):
        self.private_key = private_key
        self.user_id = user_id
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'picostocks/python'})
        self.signing_key = ed25519.SigningKey(self.private_key,
                                              encoding='hex')

    async def _get_order_request_data(self, sign_key, order_obj):
        stock_id, price_id = order_obj.stock_id, order_obj.price_id
        nonce = await self._get_nonce()

        sign_message = ":".join([
            sign_key,
            str(self.user_id),
            str(stock_id),
            decimal2string(order_obj.quantity),
            str(price_id),
            decimal2string(order_obj.price),
            str(nonce)
        ])

        return {
            'user_id': self.user_id,
            'stock_id': stock_id,
            'shares': order_obj.quantity,
            'price_id': price_id,
            'price': order_obj.price,
            'signature': self.signing_key.sign(sign_message.encode(),
                                               encoding='hex')
        }

    async def _get(self, rel_url, params=None, prefix_url=None):
        loop = asyncio.get_event_loop()
        url = urllib.parse.urljoin(prefix_url or self.PREFIX_URL, rel_url)
        return await loop.run_in_executor(
            None, lambda: self.session.get(url, params=params))

    async def _post(self, rel_url, data=None, params=None, prefix_url=None):
        loop = asyncio.get_event_loop()
        url = urllib.parse.urljoin(prefix_url or self.PREFIX_URL, rel_url)
        return await loop.run_in_executor(
            None, lambda: self.session.post(url, data=data, params=params))

    async def get_nonce(self):
        response = await self._get("account/nonce/%s/" % self.user_id)
        return response.json()

    async def get_order_book(self, stock_id, price_id, limit=100):
        params = {'stock_id': stock_id, 'price_id': price_id}
        response = await self._get("market/orderbook/", params=params)
        return response.json()

    async def get_assets_balance(self):
        response = await self._get(
            "account/balance/%s/" % self.user_id)
        return response.json()

    async def get_open_orders(self, stock_id, price_id, limit=100):
        params = {
            'stock_id': stock_id,
            'price_id': price_id,
            'user_id': self.user_id
        }
        response = await self._get("market/orderbook/", params=params)
        return response.json()

    async def put_ask(self, ask_obj):
        request_data = await self._get_order_request_data("ASK", ask_obj)
        response = await self._post("trader/ask/put/", request_data)
        return response.json()

    async def cancel_ask(self, cancel_ask_obj):
        request_data = await self._get_order_request_data("CANCELASK",
                                                          cancel_ask_obj)
        response = await self._post("trader/ask/cancel/", request_data)
        return response.json()

    async def put_bid(self, bid_obj):
        request_data = await self._get_order_request_data("BID", bid_obj)
        response = await self._post("trader/bid/put/", request_data)
        return response.json()

    async def cancel_bid(self, bid_obj):
        request_data = await self._get_order_request_data("CANCELBID", bid_obj)
        response = await self._post("trader/bid/cancel/", request_data)
        return response.json()

    async def get_stocks(self):
        response = await self._get("account/transfers/external/123/52/")
        return response.json()

if __name__ == '__main__':
    # Example usage
    exchanger = Exchanger(private_key=b'1246b84985e1ab5f83f4ec2bdf271114666fd3d9e24d12981a3c861b9ed523c6',
                          user_id='1231231231')
    loop = asyncio.get_event_loop()
    open_orders_resp = loop.run_until_complete(
        exchanger.get_stocks())
    print(open_orders_resp)


