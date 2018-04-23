# Welcome to python-picostocks-api - Public Rest API for Picostocks

This is an official Python wrapper for the Picostocks exchange REST API.

# General API Information
* The base endpoint is: **https://picostocks.com**
* All endpoints return either a JSON object or array.
* HTTP `4XX` return codes are used for for malformed requests;
  the issue is on the sender's side.
* HTTP `5XX` return codes are used for internal errors; the issue is on
  Picostocks' side.
* HTTP `504` return code is used when the API successfully sent the message
but did not get a response within the timeout period.
It is important to **NOT** treat this as a failure; the execution status is
**UNKNOWN** and could have been a success.

* For `GET` endpoints, parameters must be sent as a `query string`.
* `GET` endpoints take optional `query string` parameter named `limit`.
You can use it to limit number of results retrieved from an endpoint. It will round up specified value of `limit` to whole hundreds. Maximum value for `limit` is 300.
* For `POST`, `PUT`, and `DELETE` endpoints, the parameters must be sent in the `request body` with content type
  `application/json` or `application/x-www-form-urlencoded`. You may mix parameters between both the
  `query string` and `request body` if you wish to do so.
* Parameters may be sent in any order.

* All `price`, `quantity` and `fee` values are representation of decimal numbers with max 56 digits and precision of 18 digits after decimal place, casted to a string.



# Endpoint security type
* API-keys and secret-keys **are case sensitive**.
* All `/trader` endpoints are signed endpoints.

# SIGNED Endpoint security
* `SIGNED` endpoints require an additional parameter, `signature`, to be
  sent in the `request body`.
* Endpoints use [`Ed25519`](https://en.wikipedia.org/wiki/EdDSA#Ed25519) signatures. The `Ed25519` is the EdDSA signature scheme using SHA-512/256 and Curve25519.

## SIGNED Endpoint Examples for POST /api/v1/trader/ask/put
Here is a step-by-step example of how to send a vaild signed payload from the Python program using
[requests](https://pypi.org/project/requests/) and [ed25519](https://pypi.org/project/ed25519/)

Key | Value
------------ | ------------
PRIVATE_KEY | NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j


Parameter | Value
------------ | ------------
sign_key | "ASK"
user_id | "3175734150517431"
stock_id | "2"
quantity | "1"
price_id | "3"
price | "0.1"
nonce | "1"

* **Code example:**

    ```python
    import asyncio

    import ed25519
    import requests

    signing_key = ed25519.SigningKey(self.private_key, encoding='hex')
    message = ":".join([sign_key, user_id, stock_id, quantity, price_id, price, nonce])
    signature = signing_key.sign(message.encode(), encoding='hex')

    requests_data = {
        "user_id": user_id,
        "stock_id": stock_id,
        "quantity": quantity,
        "price_id": price_id,
        "price": price,
        "signature": signature
    }

    session = requests.Session()
    # for example:
    # {'User-Agent': 'mypythonpicostocksapi/1.0 https://github.com/johndoe/my-python-picostocks-api'}
    session.headers.update({'User-Agent': '<product>/<product_version> <comments>'})
    loop = asyncio.get_event_loop()
    url = 'https://picostocks.com/api/v1/trader/ask/put/'
    return await loop.run_in_executor(None, lambda: session.post(url, data=requests_data))
    ```

# Public API Endpoints
## Terminology
* `base asset` refers to the asset that is the `quantity` of a symbol.
* `quote asset` refers to the asset that is the `price` of a symbol.

## ENUM definitions
**ASSET STATUS:**
* "init"
* "queued"
* "accepted"
* "confirmed"
* "busy"
* "done"
* "canceled"
* "error"
* "ignore"

## General endpoints
### Security
```
GET /api/v1/account/nonce/<user_id>/
```
Get nonce for the `user_id`.

**Parameters:**
NONE

**Response:**
```JSON
{
    "id": 1,
    "nonce": 45
}
```
Attribute | Type |  Value
----------|------|-------
id | INT | user_id for which nonce was requested
nonce | INT | an arbitrary number that can only be used once ([read more](https://en.wikipedia.org/wiki/Cryptographic_nonce))

## Market Data endpoints
### Stocks info
```
GET /api/v1/market/stocks/
```
Get information about all recorded stocks.

**Parameters:**
NONE

**Response:**
```JSON
[
    {
    	"id": 15,
    	"stock_rank": 0,
    	"code": "pico",
    	"name": "PicoStocks Inc.",
    	"stock_type": "asset",
    	"email": "contact@picostocks.com",
    	"www": "www.picostocks.com",
    	"about": "Picostocks facilitates valuation and fundraising for high tech startup projects and companies and offers valuable services and benefits for both bitcoin investors and entrepreneurs",
    	"quantity": "1000000.000000000000000000",
    	"traded": "162656.995004000000000000",
    	"status": "traded",
    	"doc_id": 45,
    	"transaction_id": 0,
    	"ipo_user_id": 19,
    	"ipo_max_quantity": "200000.000000000000000000",
    	"ipo_min_price": "0.050000000000000000",
    	"ipo_rec_price": "0.000000000000000000",
    	"ipo_price": "0.050000000000000000",
    	"ipo_balance": "50.000000000000000000",
    	"btc_address": "1N4Kh4QSwTQe657VVCVTgohDzpy7CgkuKu",
    	"eth_address": null,
    	"eth_decimals": 0,
    	"min_fee": "0.000100000000000000",
    	"per_fee": "0.0050",
    	"time_init": "2012-12-21T19:11:04Z",
    	"time_ipo": "2013-01-05T00:22:21Z",
    	"time_wait": "2013-01-05T00:24:22Z",
    	"sync": "2018-03-01T00:03:02Z"
    },
    ...
]
```
### Order book
```
GET /api/v1/market/orderbook/
```
Get information about all recorded orders.

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
user_id | INT | NO | If no `user_id` is specified, response will return order book for all users
price_id | INT | NO | If no `price_id` is specified, response will return order book for all `quote assets`
stock_id | INT | NO | If no `stock_id` is specified, response will return order book for all `base assets`

**Response:**
```JSON
{
    "asks": [
        {
            "quantity": "0.000000000000069356",
            "price": "0.010000000000000000",
            "price_id": 3,
            "stock_id": 2,
            "sync": "2018-04-23T12:54:37.020322Z"
        }
    ],
    "bids": [
        {
            "quantity": "1.200000000000000000",
            "price": "0.010000000004740000",
            "price_id": 1,
            "stock_id": 2,
            "sync": "2018-04-23T12:54:16.999887Z"
        },
        {
            "quantity": "0.000000000079130000",
            "price": "0.010002000000004100",
            "price_id": 4,
            "stock_id": 52,
            "sync": "2018-04-23T12:53:30.220241Z"
        }
    ]
}
```
Attribute | Type | Value
----------|------|------
quantity | STRING | shares amount for specific order
price | STRING | price per share
price_id | INT | ID of quote asset
stock_id | INT | ID of base asset
sync | TIMESTAMP | Combined Date and Time in UTC (ISO 8601)

### Internal transactions
```
POST /api/v1/account/transfers/internal/<user_id>/<stock_id>/
```
Get information about internal transfers (inside picostocks exchange).

**Parameters:**
NONE

**Response:**
```JSON
[
    {
        "id": 6,
        "stock_id": 2,
        "quantity": "0.000200000000000000",
        "from_user": 123,
        "to_user": 321,
        "memo": "adadsasd",
        "sync": "2018-04-23T08:11:03.585205Z"
    },
    ...
]
```
Attribute | Type | Value
----------|------|------
id | INT | transfer ID number
stock_id | INT | ID of base asset
quantity | STRING | shares amount for specific order
from_user | INT | ID of user who initiated the order
to_user | INT | ID of user who is the recipient of the order
sync | TIMESTAMP | Combined Date and Time in UTC (ISO 8601)

### External transactions
```
POST /api/v1/account/transfers/external/<user_id>/<stock_id>/
```
Get information about external transfers (involving 3rd party users).

**Parameters:**
NONE

**Response:**
```JSON
{
    "withdrawals": [
        {
            "quantity": "0.002000000000000000",
            "status": "init",
            "address": "jr31031me0d9rf910",
            "txid": "md3189u4edm0q9139j",
            "memo": "memo message goes here",
            "fee": "0.001000000000000000"
        },
        ...
    ],
    "deposits": [
        {
            "quantity": "0.002000000000000000",
            "status": "init",
            "address": "",
            "txid": "dami30189jrmqd03rmq",
            "memo": "memo message goes here",
            "fee": "0"
        }
    ]
}
```
Attribute | Type | Value
----------|------|------
quantity | STRING | shares amount for specific order
status | ENUM | One of ASSET STATUS values
address | STRING | wallet address. For deposits it is always empty string.
txid | STRING | transaction ID
memo | STRING | message associated with specific order
fee | STRING | fee associated with specific order

### Recent trades list
```
GET /api/v1/account/order/history/<user_id>/<stock_id>/
```
Get asks & bids history for specific `user_id` and `stock_id`

**Parameters:**
NONE

**Response:**
```JSON
{
    "bids": [
        {
            "stock_id": 2,
            "quantity": "1.000000000000000000",
            "price_id": 3,
            "price": "0.100000000000000000",
            "bid_user": 1384975617398,
            "ask_user": 8504937597712,
            "sync": "2018-04-23T12:50:28.623358Z"
        }
    ],
    "asks": [
        {
            "stock_id": 2,
            "quantity": "1.000000000000000000",
            "price_id": 3,
            "price": "0.100000000000000000",
            "bid_user": 8504937597712,
            "ask_user": 1384975617398,
            "sync": "2018-04-23T12:50:45.666215Z"
        }
    ]
}
```
Attribute | Type | Value
----------|------|------
stock_id | INT | ID of base asset
quantity | STRING | shares amount for specific order
price_id | INT | ID of quote asset
price | STRING | price per share
bid_user | INT | ID of bidding user
ask_user | INT | ID of asking user
sync | TIMESTAMP | Combined Date and Time in UTC (ISO 8601)

## Trading endpoints
### New ask order
```
POST /api/v1/trader/ask/put/
```
Create a new ask order.

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
user_id | INT | YES | ID of user who is making ask
stock_id | INT | YES | ID of base asset
quantity | STRING | YES | shares amount for specific order
price_id | INT | YES | ID of quote asset
price | STRING | YES | price per share
signature | STRING | YES | Read more about signature in [SIGNED Endpoint security](#signed-endpoint-security)

**Response:**
```JSON
{
    "results": {}, status: 201
}
```

### New bid order
```
POST /api/v1/trader/bid/put/
```
Create a new bid order.

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
user_id | INT | YES | ID of user who is making bid
stock_id | INT | YES | ID of base asset
quantity | STRING | YES | shares amount for specific order
price_id | INT | YES | ID of quote asset
price | STRING | YES | price per share
signature | STRING | YES | Read more about signature in [SIGNED Endpoint security](#signed-endpoint-security)

**Response:**
```JSON
{
    "results": {}, status: 201
}
```
### Cancel ask order
```
POST /api/v1/trader/ask/cancel/
```
Cancel ask order.

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
user_id | INT | YES | ID of user who is cancelling the order
stock_id | INT | YES | ID of base asset
quantity | STRING | YES | shares amount for specific order
price_id | INT | YES | ID of quote asset
price | STRING | YES | price per share
signature | STRING | YES | Read more about signature in [SIGNED Endpoint security](#signed-endpoint-security)

**Response:**
```JSON
{
    "results": {}, status: 201
}
```

### Cancel bid order
```
POST /api/v1/trader/bid/cancel/
```
Cancel bid order.

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
user_id | INT | YES | ID of user who is canceling the bid
stock_id | INT | YES | ID of base asset
quantity | STRING | YES | shares amount for specific order
price_id | INT | YES | ID of quote asset
price | STRING | YES | price per share
signature | STRING | YES | Read more about signature in [SIGNED Endpoint security](#signed-endpoint-security)

**Response:**
```JSON
{
    "results": {}, status: 201
}
```
