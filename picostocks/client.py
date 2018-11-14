# -*- coding: utf-8 -*-

import asyncio
import urllib.parse

import ed25519
import requests

from picostocks.utils import float2string


class Exchanger(object):
    PREFIX_URL = "https://api.picostocks.com/v1/"

    def __init__(self, private_key, user_id, session=None):
        self.user_id = user_id

        # Bytes of private key.
        self.private_key = private_key
        if isinstance(self.private_key, str):
            self.private_key = self.private_key.encode()

        self.signing_key = ed25519.SigningKey(self.private_key, encoding='hex')
        self.session = session
        if self.session is None:
            self.session = requests.Session()
            self.session.headers.update({'User-Agent': 'picostocks/python'})

    async def _get_order_request_data(self, sign_key, stock_id, unit_id, quantity,
                                      price):
        nonce_resp = await self.get_nonce()

        sign_message = ":".join([
            sign_key,
            str(self.user_id),
            str(stock_id),
            float2string(quantity),
            str(unit_id),
            float2string(price),
            str(nonce_resp['nonce'])
        ])

        return {
            'user_id': self.user_id,
            'stock_id': stock_id,
            'quantity': float2string(quantity),
            'unit_id': unit_id,
            'price': float2string(price),
            'signature': self.signing_key.sign(sign_message.encode()).hex()
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

    async def get_order_book(self, stock_id, unit_id, limit=100):
        params = {'stock_id': stock_id, 'unit_id': unit_id}
        response = await self._get("market/orderbook/", params=params)
        return response.json()

    async def get_assets_balance(self, user_id=None):
        if user_id is None:
            user_id = self.user_id

        response = await self._get("account/balance/%s/" % user_id)
        return response.json()

    async def get_open_orders(self, stock_id=None, unit_id=None, user_id=None, limit=100):
        if user_id is None:
            user_id = self.user_id

        params = dict(user_id = user_id)
        if stock_id is not None:
            params['stock_id'] = stock_id
        if unit_id is not None:
            params['unit_id'] = unit_id

        response = await self._get("market/orderbook/", params=params)
        return response.json()

    async def get_historical_orders(self, stock_id, user_id=None, unit_id=None):
        params = None
        if user_id is None:
            user_id = self.user_id
            
        if unit_id is not None:
            params = {'unit_id': unit_id}
            
        response = await self._get(
            'account/order/history/%s/%s/' % (user_id, stock_id),
            params=params)
        return response.json()

    async def get_all_historical_orders(self, stock_id, unit_id):
        response = await self._get(
            'account/order/history/stocks/%s/%s/' % (stock_id, unit_id))
        return response.json()

    async def get_transfers_internal(self, stock_id):
        response = await self._get(
            'account/transfers/internal/%s/%s/' % (self.user_id, stock_id))
        return response.json()

    async def get_transfers_external(self, stock_id):
        response = await self._get(
            'account/transfers/external/%s/%s/' % (self.user_id, stock_id))
        return response.json()

    async def put_ask(self, stock_id, unit_id, quantity, price):
        request_data = await self._get_order_request_data("ASK", stock_id, unit_id,
                                                          quantity, price)
        response = await self._post("trader/ask/put/", request_data)
        return response.json()

    async def cancel_ask(self, stock_id, unit_id, quantity, price):
        request_data = await self._get_order_request_data("CANCELASK", stock_id, unit_id,
                                                          quantity, price)
        response = await self._post("trader/ask/cancel/", request_data)
        return response.json()

    async def put_bid(self, stock_id, unit_id, quantity, price):
        request_data = await self._get_order_request_data("BID", stock_id, unit_id,
                                                          quantity, price)
        response = await self._post("trader/bid/put/", request_data)
        return response.json()

    async def cancel_bid(self, stock_id, unit_id, quantity, price):
        request_data = await self._get_order_request_data("CANCELBID", stock_id, unit_id,
                                                          quantity, price)
        response = await self._post("trader/bid/cancel/", request_data)
        return response.json()

    async def get_stocks(self, limit=100):
        response = await self._get("market/stocks/", params={'limit': limit})
        return response.json()


if __name__ == '__main__':
    # Example usage
    exchanger = Exchanger(private_key=b'<private_key>', user_id='<user_id>')
    loop = asyncio.get_event_loop()
    open_orders_resp = loop.run_until_complete(exchanger.get_stocks())
    print(open_orders_resp)
