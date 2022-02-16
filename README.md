# 🌶️ Jalapiño  API Reference

_Welcome to Jalapiño, a platform created to enable restaurants and customers to come together for a feast of foods in a delivery bonanza._

## Intro

This documentation aims to be a comprehensive aid in using the Jalapino API endpoints. The API follows RESTful design principles & best practices, e.g. nouns as resource identifiers as well as accepting and returning data in JSON format.


// Base URL
```
https://jalapino-api.herokuapp.com
```

---

## Authentication & Authorization

#### ⚠️ Registration is currently closed.

Test accounts are provided for each of the two distinct user **roles**  
(Under each role listed are their scope aka permissions)  

**customer** - _Jalapino customer placing delivery orders_  
`create:customer`
`read:customer`
`update:customer`
`delete:customer`
`create:order`
`read:order`  

**restaurant** - _Restaurant offering foods and drinks to Jalapino customers_  
`create:restaurant`
`update:restaurant`
`delete:restaurant`
`create:category`
`update:category`
`delete:category`
`create:item`
`update:item`
`delete:item`
`read:order`

#### There are two ways to authenticate, you can use either one
#### 🔐 1) Use the provided JWTs directly. To add them to your environment variables, run the following command:
```bash
source env.sh
$CUSTOMER_TOKEN
$RESTAURANT_TOKEN
```

ℹ️ _These tokens have ownership of the preloaded resources in the DB, meaning that any pre-existing data in the DB can only be modified or deleted with these JWTs where the endpoint specifies "Requires ownership of the resource"_

---

#### 🔐 2) Login with the credentials using the login prompt on the main page. Upon successful login the user will be redirected to a page that displays the newly generated JWT for the account.

ℹ️ _Make sure to generate a new token this way if the existing one(s) don't work and update the **$CUSTOMER_TOKEN** and **$RESTAURANT_TOKEN** environment variables accordingly_

```
https://jalapino-api.herokuapp.com
```
<details>
<summary><h3>🔐 Reveal Credentials</h3></summary>

##### Test Customer #0 *($CUSTOMER_TOKEN)*
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkJGV2Frc1dVRmlQRmpLd25fakotUSJ9.eyJpc3MiOiJodHRwczovL251bGxmYW1lLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MWY4NDkxNmJmMWRmOTAwNzEzN2QzNDciLCJhdWQiOiJqYWxhcGlubyIsImlhdCI6MTY0NDk2MDMzMiwiZXhwIjoxNjQ1MDQ2NzMyLCJhenAiOiJRdFkxVnBYdjhWbUlYUjRxSDVYNUVWYk9kMnoyU042NSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmN1c3RvbWVyIiwiY3JlYXRlOm9yZGVyIiwiZGVsZXRlOmN1c3RvbWVyIiwicmVhZDpjdXN0b21lciIsInJlYWQ6b3JkZXIiLCJ1cGRhdGU6Y3VzdG9tZXIiXX0.ok225364i_xczyDOlJHoGrkBEqGs9AWHiydv0NYghaDruCbj3gE4tSl90Hj-rtjT3bofnhxaDvCd7w4dI45flJLtGORS51BwLEYeD99MmFE0UyIYZ_gDiihu3NTG-g0zf6EelzKLfQF0zrd21uFaTOkh7eo3z3cLAQBYzqXnZRjiF5iYnhaXRoKn9DaDLbXiFKgyZ0o5Bs1DxL2ZKJcbETQqhxSSmajUsHCAtkP3M0ik1PG0P_L6Hhu_bSp37BDxD-zWZgcm2CG79iy4634PtPC6QBCIcxuj-P4M3I9XVLxgdUS0Nwx1tpHJUM0pTo2Sw2RUWcwzPyuLpJH36kVDHg
```
##### Test Customer #1 *(Username & Password)*
```
jalapino.test+customer1@gmail.com
Test+Customer123
```
##### Test Customer #2 *(Username & Password)*
```
jalapino.test+customer2@gmail.com
Test+Customer123
```
##### Test Restaurant #0 *($RESTAURANT_TOKEN)*
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkJGV2Frc1dVRmlQRmpLd25fakotUSJ9.eyJpc3MiOiJodHRwczovL251bGxmYW1lLmV1LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MWY4NDhkMTkwYjYwZjAwNzBmMmYyOTQiLCJhdWQiOiJqYWxhcGlubyIsImlhdCI6MTY0NDk2MDM5OSwiZXhwIjoxNjQ1MDQ2Nzk5LCJhenAiOiJRdFkxVnBYdjhWbUlYUjRxSDVYNUVWYk9kMnoyU042NSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmNhdGVnb3J5IiwiY3JlYXRlOml0ZW0iLCJjcmVhdGU6cmVzdGF1cmFudCIsImRlbGV0ZTpjYXRlZ29yeSIsImRlbGV0ZTppdGVtIiwiZGVsZXRlOnJlc3RhdXJhbnQiLCJyZWFkOm9yZGVyIiwidXBkYXRlOmNhdGVnb3J5IiwidXBkYXRlOml0ZW0iLCJ1cGRhdGU6cmVzdGF1cmFudCJdfQ.thvmO0kpsuGmp-GGchzNHmC8MqRQWSOlazIPeUsRy_NpyB1YNQOAy4QtigEJHRxIkJ5WSBH-ivfbQ-gU08PZ5NLZOEUS_MPRM6RpYiC1e5m7Br0KZsySVQTouZAPv66iXhNrLg86RXtQ3-Ho_7_21FT5D8Rgs-6IiWgoLucNxQZWyxDNBccu05Mb6JN4kXlNpPWf9r4foV9JK59cBAJwsYhzJQNneUnozLgLSK9U0YOndQLQ1Jxr5KC6Kjnv1eSzpYbhXQN65uc-QzgvS5xqF8PbcTV8Us0N-IZPpH7IC10fcTY0YM2OIHvm852u2de-fV1Gqard8S_hNhU6-FhS0Q
```
##### Test Restaurant #1 *(Username & Password)*
```
jalapino.test+restaurant1@gmail.com
Test+Restaurant123
```
##### Test Restaurant #2 *(Username & Password)*
```
jalapino.test+restaurant2@gmail.com
Test+Restaurant123
```

</details>

---

## List of all endpoints

// API Info  
`GET /info`  

// Restaurants  
`GET /restaurants`  
`GET /restaurant/:id`  
`POST /restaurants`  
`PUT /restaurant/:id`  
`PATCH /restaurant/:id`  
`DELETE /restaurant/:id`

// Customers  
`GET /customers/:id`  
`POST /customers`  
`PATCH /customers/:id`  
`DELETE /customers/:id` 

// Categories  
`POST /restaurant/:id/categories`  
`PUT /categories/:id`  
`PATCH /categories/:id`  
`DELETE /categories/:id` 

// Items & Ingredients  
`GET /items/:id`  
`GET /ingredients/:id/items`  
`POST /items`  
`POST /categories/:id/items`  
`PUT /items/:id`  
`PATCH /items/:id`  
`DELETE /items/:id` 

---

## Endpoints in detail

*All endpoints include sample request & response examples*

### GET /info

ℹ️ Returns all quiz categories in the specified format.

```bash
# Sample request
curl -X GET 'https://jalapino-api.herokuapp.com/info'
```
```jsonc
// Sample response
200 OK
{
  "contact": {
    "email": "jalapino.test@gmail.com",
    "name": "David Pacsuta",
    "url": "https://github.com/ant1fact/jalapino"
  },
  "description": "Simplified food delivery platform where restaurants can post their items and customers can place orders.",
  "license": {
    "name": "MIT",
    "url": "https://spdx.org/licenses/MIT.html"
  },
  "title": "Jalapino - Final project for Udacity Fullstack Nanodegree",
  "version": 0.1
}
```

### GET /restaurants

ℹ️ Return a list of all restaurant objects paginated. The default number of items per page is 10<br>
⚠️ If the ?page query parameter is beyond the number of available pages, a 404 error will be returned

```bash
# Sample request
curl -X GET 'https://jalapino-api.herokuapp.com/restaurants?page=1'
```
```jsonc
// Sample response
200 OK
[
  {
    "address": "8601 Lindbergh Blvd, 19153 Philadelphia, Pennsylvania",
    "categories": [
      {
        "id": 1,
        "items": [
          {
            "description": "A dip made from black cardamom and yellow pepper.",
            "id": 1,
            "ingredients": [
              { "id": 71, "name": "creme fraiche" },
              { "id": 141, "name": "cardamom" },
              { "id": 73, "name": "pepper" }
            ],
            "name": "Cardamom and pepper dip",
            "price": "1.49"
          },
          {
            // more items ...
          }
          {
            "description": "Toasted seaweed wrapped around sushi rice, filled with sweet pepper and freshly-caught salmon.",
            "id": 8,
            "ingredients": [
              { "id": 1, "name": "rice" },
              { "id": 134, "name": "rice vinegar" },
              { "id": 73, "name": "pepper" },
              { "id": 55, "name": "salmon" }
            ],
            "name": "Pepper and salmon maki",
            "price": "4.99"
          }
        ],
        "name": "Appetizers"
      },
      {
        // category #2 ...
      },
      {
        // category #3 ...
      },
      // An empty category
      { "id": 4, "items": [], "name": "Drinks" }
    ],
    "description": "It's not all sunshine and BBQ!",
    "email": "hello@nn-bbq.com",
    "id": 1,
    "logo_uri": "https://raw.githubusercontent.com/ant1fact/jalapino/main/static/images/food-g9be06d40f_640.jpg",
    "name": "Not Necessarily BBQ",
    "orders": [],
    "phone": "+1 202-918-2132",
    "website": "www.nn-bbq.com"
  },
  {
    // restaurant #2 ...
  },
  {
    // restaurant #3 ...
  }
]
```

### GET /restaurant/:id

ℹ️ Returns the requested restaurant object by its id or 404 if it is not found

```bash
# Sample request
curl -X GET 'https://jalapino-api.herokuapp.com/restaurants/1'
```
```jsonc
// Sample response
200 OK
{
  "description": "It's not all sunshine and BBQ!",
  "email": "hello@nn-bbq.com",
  "id": 1,
  "logo_uri": "https://raw.githubusercontent.com/ant1fact/jalapino/main/static/images/food-g9be06d40f_640.jpg",
  "name": "Not Necessarily BBQ",
  "phone": "+1 202-918-2132",
  "website": "www.nn-bbq.com",
  "categories": [...] // Same format as in GET /restaurants
}
```

### POST /restaurants

ℹ️ Create a new restaurant in the database. On successful creation, it returns the id of the new object with status code 201   
⚠️ The auth0 account used to create the new resource becomes the owner which will be required for any subsequent edits or deletion of the resource

Required data
```jsonc
"address"
"email"  
"name"  
"phone"  
```

```bash
# Sample request
TOKEN=$RESTAURANT_TOKEN
curl -X POST 'https://jalapino-api.herokuapp.com/restaurants' -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -d '{"name": "TEST_RESTAURANT", "email": "test-restaurant@test.com", "phone": "1-234-567890", "address": "111 Testreet, Testown"}'
```
```jsonc
// Sample response
201 CREATED
{"id": 1}
```

### PUT /restaurants/:id

ℹ️ Update the full representation of a restaurant resource  
⚠️ Requires ownership of the resource

Required data
```jsonc
"address"
"description"  
"email"  
"logo_uri"  
"name"  
"phone"  
"website"  
```

```bash
# Sample request
TOKEN=$RESTAURANT_TOKEN
curl -X PUT 'https://jalapino-api.herokuapp.com/restaurants/1' -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -d '{"name": "Renamed Restaurant", "email": "renamed-restaurant@test.com", "phone": "1-876-543210", "address": "42 Sesame St, Foodtown", "description": "The Sun shines on us again.", "logo_uri": "https://raw.githubusercontent.com/ant1fact/jalapino/main/static/images/food-g9be06d40f_640.jpg", "website": "www.nn-bbq.com"}'
```
```jsonc
// Sample response
200 OK
```
### PATCH /restaurants/:id

ℹ️ Partially update the representation of a restaurant resource  
⚠️ Requires ownership of the resource

```bash
# Sample request
TOKEN=$RESTAURANT_TOKEN
curl -X PATCH 'https://jalapino-api.herokuapp.com/restaurants/1' -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -d '{"name": "Doubly Renamed Restaurant"}'
```
```jsonc
// Sample response
200 OK
```

### DELETE /restaurants/:id

ℹ️ Delete restaurant resource by id  
⚠️ Requires ownership of the resource

```bash
# Sample request
TOKEN=$RESTAURANT_TOKEN
curl -X DELETE 'https://jalapino-api.herokuapp.com/restaurants/1' -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}"
```
```jsonc
// Sample response
200 OK
```

### GET /customers/:id

ℹ️ Returns the requested customer object by its id or 404 if it is not found  
⚠️ For data security reasons, this GET endpoint requires ownership of the resource

```bash
# Sample request
TOKEN=$CUSTOMER_TOKEN
curl -X GET 'https://jalapino-api.herokuapp.com/customers/1' -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}"
```
```jsonc
// Sample response
200 OK
{
  "id": 1,
  "name": "TEST_CUSTOMER",
  "address": "99 Some St., Town, State",
  "phone": "1-234-5678910",
  "email": "test@test.com",
  "orders": []
}
```

### POST /customers

ℹ️ Create a new customer profile in the database. On successful creation, it returns the id of the new object with status code 201   
⚠️ The auth0 account used to create the new resource becomes the owner which will be required for any subsequent edits or deletion of the resource

Required data
```jsonc
"name"  
"address"
"phone"  
"email"  
```

```bash
# Sample request
TOKEN=$CUSTOMER_TOKEN
curl -X POST 'https://jalapino-api.herokuapp.com/customers' -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -d '{"name": "TEST_CUSTOMER", "email": "test-customer@test.com", "phone": "1-151-15660850", "address": "111 Custom St, Customtown"}'
```
```jsonc
// Sample response
201 CREATED
{"id": 1}
```

### PATCH /customers/:id

ℹ️ Partially update the representation of a customer profile  
⚠️ Requires ownership of the resource

```bash
# Sample request
TOKEN=$CUSTOMER_TOKEN
curl -X PATCH 'https://jalapino-api.herokuapp.com/customers/1' -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}" -d '{"name": "Crusty Customer"}'
```
```jsonc
// Sample response
200 OK
```

### DELETE /customers/:id

ℹ️ Delete customer profile by id  
⚠️ Requires ownership of the resource

```bash
# Sample request
TOKEN=$CUSTOMER_TOKEN
curl -X DELETE 'https://jalapino-api.herokuapp.com/customers/1' -H "Content-Type: application/json" -H "Authorization: Bearer ${TOKEN}"
```
```jsonc
// Sample response
200 OK
```


## Error handling

ℹ️ All HTTP errors are returned as JSON using the below format.

```javascript
// Sample error
{
  "code": 405,
  "description": "The method is not allowed for the requested URL.",
  "name": "Method Not Allowed"
}
```
ℹ️ Auth errors are in the format provided by auth0

```javascript
// Sample error 401
{
    "code": "authorization_header_missing",
    "description": "Authorization header is expected"
}
```

## Contributing to the Jalapino API

All of the backend code is formatted using [Black](https://github.com/psf/black). Imports are sorted using the `Python Refactor: Sort Imports` command available as part of the Python extension for VSCode.

ℹ️ To run the backend locally
```bash
# Set up the environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Create and populate db
createdb jalapino
psql jalapino < jalapino.sql

# Export environment variables
source env.sh

# Run the tests (Optional)
python -m pytest

# Start the server
flask run
```

### Dependencies

`Python 3.8.10`  
```
Flask==2.0.2
Flask-Cors==3.0.10
Flask_Migrate==3.1.0
Flask_SQLAlchemy==2.5.1
python_jose==3.3.0
SQLAlchemy==1.4.31
psycopg2-binary==2.9.3
gunicorn==20.1.0
pytest==7.0.1
```


## Authors

David Pacsuta

## Acknowledgements

The Fullstack Nanodegree teaching staff, as well as mentors and reviewers at Udacity  
All the helpful people at knowledge.udacity.com and stackoverflow.com  
Maintainers of the Flask documentation  
Miguel Grinberg