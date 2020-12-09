# Simple Book Store

This is a simple book renting cost api. It calculates the amount you owe for books rented based on number of days.
BASE_URL = `https://lori-bookstore.herokuapp.com`

## Using the API

This section will demonstrate making api calls using `httpie`, you may need to install it.

### Basic Auth

This api uses OAuth2.0 Client Credentials flow for basic authentication.

#### Register User

To register a user make a `POST` `request` to `{BASE_URL}/auth/register`:

```
http POST {BASE_URL}/auth/register username=flake8 email=flake8@eg.com password=lorem

{
    "access_token": ACCESS_TOKEN,
    "customer_id": 1,
    "refresh_token": REFRESH_TOKEN,
    "user": {
        "active": true,
        "email": "flake8@eg.com",
        "id": 5,
        "role": customer,
        "username": "flake8"
    }
}
```
You may need the access token on some endpoints.

#### Login User
To login a user make a `POST` `request` to `{BASE_URL}/auth/login`:

```
http POST https://lori-bookstore.herokuapp.com/auth/login username=flake8 password=lorem

{
    "access_token": ACCESS_TOKEN,
    "refresh_token": REFRESH_TOKEN
}

```


### List Books
To list all rentable books, make a `GET` `request` to `{BASE_URL}/api/v1/all-books`:

```
http GET https://lori-bookstore.herokuapp.com/api/v1/all-books

{
    "next": "/api/v1/all-books?page=1&per_page=50",
    "pages": 0,
    "prev": "/api/v1/all-books?page=1&per_page=50",
    "results": [LIST OF BOOKS],
    "total": 0
}
```


### Add Books To Cart
Once you see books you may want to calculate the cost you add to cart first, make a `POST` `request` to 
`{BASE_URL}/api/v1/cart-items`: USE the ACCESS_TOKEN you got after sign-up in headers to make the request

```
SAMPLE BODY
{
    'items' :[
              {'book_id': 1, 'due_at': 'Fri, 11 Dec 2020 16:19:24 GMT'}, 
              {'book_id': 2, 'due_at': 'Sun, 13 Dec 2020 16:19:24 GMT'},
              {'book_id': 3, 'due_at': 'Mon, 14 Dec 2020 16:19:24 GMT'}
    ]
}

SAMPLE RESP
{
    'data': {
            'cart': 
                 {'id': 1, 'created_at': '2020-12-09T16:19:24.123033'},
                  'cart_items': [{'id': 1, 'created_at': '2020-12-09T16:19:24.126874'},
                                 {'id': 2, 'created_at': '2020-12-09T16:19:24.126874'},
                                 {'id': 3, 'created_at': '2020-12-09T16:19:24.126874'}],
                    'rentals': [
                                {'status': 'PENDING', 'due_at': '2020-12-11T16:19:24', 'id': 1, 
                                 'created_at': '2020-12-09T16:19:24.138433'}, 
                                {'status': 'PENDING', 'due_at': '2020-12-13T16:19:24', 'id': 2,
                                 'created_at': '2020-12-09T16:19:24.138433'},
                                {'status': 'PENDING', 'due_at': '2020-12-14T16:19:24', 'id': 3,
                                 'created_at': '2020-12-09T16:19:24.138433'}]}}
```

### GET Cart cost
After Adding the books you want to your cart, you will notice that a `Cart` object that has an `id` is returned, 
use that  `id` to make a `GET` request to `{BASE_URL}/api/v1/cart/<id>/order-price`:

```
http GET https://lori-bookstore.herokuapp.com/api/v1/carts/1/order-price 'Authorization:Bearer ACCESS_TOKEN'

{
    'cost_usd': 21
}
```

