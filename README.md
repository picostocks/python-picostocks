# Welcome to python-picostocks-api - Public Rest API for Picostocks

This is an official Python wrapper for the Picostocks exchange REST API.

# General API information
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
* Any endpoint can retun an ERROR; the error payload is as follows:
```JSON
{
  "detail": "ERROR: error message goes here"
}
```

* For `GET` endpoints, parameters must be sent as a `query string`.
* For `POST`, `PUT`, and `DELETE` endpoints, the parameters must be sent in the `request body` with content type
  `application/json`.
* Parameters may be sent in any order.

* All `price`, `quantity` and `fee` values are representation of decimal numbers with max 56 digits and precision of 18 digits after decimal place, casted to a string.
* Some of `GET` endpoints take optional `limit` query parameter. You can use it to limit number of results retrieved from an endpoint.
It is always rounded up to the nearest hundreds. Default 100, Max 300. Look for **Parameters** tables next to each endpoint to see if it is available.

# SIGNED endpoint security
* PRIVATE_KEY **is case sensitive**.
* All `/trader` endpoints are signed endpoints.
* `SIGNED` endpoints require an additional parameter, `signature`, to be sent in the `request body`.
* Endpoints use [`Ed25519`](https://en.wikipedia.org/wiki/EdDSA#Ed25519) signatures. The `Ed25519` is the EdDSA signature scheme using SHA-512/256 and Curve25519.

# Public API endpoints
## Terminology
* `stock_id` refers to the asset that is the `quantity` of a symbol.
* `unit_id` refers to the asset that is the `price` of a symbol.
* `quantity` refers to shares amount for specific order.
* `price` refers to price per share.
* `signature` refers to the [digital signature](https://en.wikipedia.org/wiki/Digital_signature).
Read more how to generate a message signature for picostocks exchange in
[SIGNED Endpoint security](#signed-endpoint-security) section.
* `sync` refers to combination of Date and Time in UTC (ISO 8601) format.

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
GET /v1/account/nonce/<user_id>/
```
Get nonce for the `user_id`.

**Parameters:**
NONE

**Response:**
```JSON
{
    "nonce": 45
}
```
Attribute | Type |  Value
----------|------|-------
nonce | INT | an arbitrary number that can only be used once ([read more](https://en.wikipedia.org/wiki/Cryptographic_nonce))

### Balance
```
GET /v1/account/balance/<user_id>/
```
Get information about user's balance.

**Parameters:**
NONE

**Response:**
```JSON
[
    {
        "stock_id": 2,
        "locked": "0.001230000000000000",
        "free": "0.012300000000000000"
    }
]
```
Attribute | Type
----------|------
stock_id | STRING
locked | STRING
free | STRING

## Market data endpoints
### Stocks info
```
GET /v1/market/stocks/
```
Get detailed information about all available stocks on picostocks exchange.

**Parameters:**

Name | Type | Mandatory
---- | ---- | ---------
limit | INT | NO

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
    }
]
```
### Order book
```
GET /v1/market/orderbook/
```
Get information about all recorded orders.

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
user_id | INT | NO | if no `user_id` is specified, response will return order book for all users
unit_id | INT | NO | if no `unit_id` is specified, response will return order book for all `quote assets`
stock_id | INT | NO | if no `stock_id` is specified, response will return order book for all `base assets`
limit | INT | NO

**Response:**
```JSON
{
    "asks": [
        {
            "quantity": "0.000000000000069356",
            "price": "0.010000000000000000",
            "unit_id": 3,
            "stock_id": 2,
            "sync": "2018-04-23T12:54:37.020322Z"
        }
    ],
    "bids": [
        {
            "quantity": "1.200000000000000000",
            "price": "0.010000000004740000",
            "unit_id": 1,
            "stock_id": 2,
            "sync": "2018-04-23T12:54:16.999887Z"
        },
        {
            "quantity": "0.000000000079130000",
            "price": "0.010002000000004100",
            "unit_id": 4,
            "stock_id": 52,
            "sync": "2018-04-23T12:53:30.220241Z"
        }
    ]
}
```
Attribute | Type
----------|------
quantity | STRING
price | STRING
unit_id | INT
stock_id | INT
sync | TIMESTAMP

### Internal transactions
```
POST /v1/account/transfers/internal/<user_id>/<stock_id>/
```
Get information about internal transfers (executed entirely inside picostocks exchange).

**Parameters:**
NONE

**Response:**
```JSON
[
    {
        "stock_id": 2,
        "quantity": "0.000200000000000000",
        "from_user": 123,
        "to_user": 321,
        "memo": "adadsasd",
        "sync": "2018-04-23T08:11:03.585205Z"
    }
]
```
Attribute | Type | Description
----------|------|------
id | INT | transfer ID number
stock_id | INT
quantity | STRING
from_user | INT | ID of user who initiated the order
to_user | INT | ID of user who is the recipient of the order
sync | TIMESTAMP

### External transactions
```
POST /v1/account/transfers/external/<user_id>/<stock_id>/
```
Get information about external transfers (involving 3rd party users in the process).

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
        }
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
Attribute | Type | Description
----------|------|------
quantity | STRING
status | ENUM | one of [ASSET STATUS](#enum-definitions) values
address | STRING | wallet address. For deposits it is always empty string
txid | STRING | transaction ID
memo | STRING | message associated with specific order
fee | STRING | fee associated with specific order. For deposits it is always "0"

### Recent trades list
```
GET /v1/account/order/history/<user_id>/<stock_id>/
```
Get asks & bids history for specific `user_id` and `stock_id`

**Parameters:**

Name | Type | Mandatory
---- | ---- | ---------
limit | INT | NO

**Response:**
```JSON
{
    "bids": [
        {
            "stock_id": 2,
            "quantity": "1.000000000000000000",
            "unit_id": 3,
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
            "unit_id": 3,
            "price": "0.100000000000000000",
            "bid_user": 8504937597712,
            "ask_user": 1384975617398,
            "sync": "2018-04-23T12:50:45.666215Z"
        }
    ]
}
```
Attribute | Type
----------|------
stock_id | INT
quantity | STRING
unit_id | INT
price | STRING
bid_user | INT
ask_user | INT
sync | TIMESTAMP

## Trading endpoints
### New ask order
```
POST /v1/trader/ask/put/
```
Create a new ask order.

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
user_id | INT | YES | ID of user who is making ask
stock_id | INT | YES
quantity | STRING | YES
unit_id | INT | YES
price | STRING | YES
signature | STRING | YES | signature of `"ASK:<user_id>:<stock_id>:<quantity>:<unit_id>:<price>:<nonce>"` in hex encoding.

**Response:**
```JSON
{
	"user_id": 19,
	"stock_id": 3,
	"quantity": "0.035000000000000000",
	"unit_id": 2,
	"price": "1000000000.000000000000000000",
	"signature": "129999b1d69f32cc0290e8e420344c4eab0d6eafed10d8f9960e20256be95fd16e5036a81edaaeab1228b1f9c5b73f5d1c67047a360540c8dca143c486203b05",
	"response": "b'ASK 0.035000000000000000 shares at 1000000000.000000000000000000; '"
}
```

### New bid order
```
POST /v1/trader/bid/put/
```
Create a new bid order.

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
user_id | INT | YES | ID of user who is making bid
stock_id | INT | YES
quantity | STRING | YES
unit_id | INT | YES
price | STRING | YES
signature | STRING | YES | signature of `"BID:<user_id>:<stock_id>:<quantity>:<unit_id>:<price>:<nonce>"` in hex encoding.

**Response:**
```JSON
{
	"user_id": 19,
	"stock_id": 3,
	"quantity": "311312380.220172400000000000",
	"unit_id": 2,
	"price": "0.000000001000000000",
	"signature": "171674b5a04ee11f266296c6815c36040cd29317d1e6683cdfaa18c1610fd378a4db9be4d913b5975ea5903fffc13a0b4b2c91c54559fc1c4b2b6f859e6ae002",
	"response": "b'BID 311312380.220172400000000000 shares at 0.000000001000000000; '"
}
```

### Cancel ask order
```
POST /v1/trader/ask/cancel/
```
Cancel ask order.

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
user_id | INT | YES | ID of user who is cancelling the order
stock_id | INT | YES
quantity | STRING | YES
unit_id | INT | YES
price | STRING | YES
signature | STRING | YES | signature of `"CANCELASK:<user_id>:<stock_id>:<quantity>:<unit_id>:<price>:<nonce>"` in hex encoding.

**Response:**
```JSON
{
	"user_id": 1,
	"stock_id": 3,
	"quantity": "0.035000000000000000",
	"unit_id": 2,
	"price": "1000000000.000000000000000000",
	"signature": "ceaa646d184155890c71224897e7bbf72b4cbd49092c799086cfd969de1e10fa448564ba9b46f5e02828d858882514ef4e99e0cf91f5d594504848920f56f802",
	"response": "0.035000000000000000"
}
```

### Cancel bid order
```
POST /v1/trader/bid/cancel/
```
Cancel bid order.

**Parameters:**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
user_id | INT | YES | ID of user who is canceling the bid
stock_id | INT | YES
quantity | STRING | YES
unit_id | INT | YES
price | STRING | YES
signature | STRING | YES | signature of `"CANCELBID:<user_id>:<stock_id>:<quantity>:<unit_id>:<price>:<nonce>"` in hex encoding.

**Response:**
```JSON
{
	"user_id": 1,
	"stock_id": 3,
	"quantity": "311312380.220172400000000000",
	"unit_id": 2,
	"price": "0.000000001000000000",
	"signature": "83c20663ac2b6bd77312ed7707d122f9b5da11404665b36cb47a845718f9b1eccd22ab40c7f6724485d37e871e7d26269b636a6beed051b5c6a904b473b7bc00",
	"response": "311312380.220172400000000000"
}
```
