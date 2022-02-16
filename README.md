# 🌶️ Jalapino API Reference

## Intro

This documentation aims to be a comprehensive aid in using the Jalapino API endpoints.  
The API follows RESTful design principles & best practices, e.g. nouns as resource identifiers as well as accepting and returning data in JSON format.


// Base URL
```
https://jalapino-api.herokuapp.com
```

---

## Authentication

⚠️ Registration is currently closed.

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

ℹ️ There are two ways to authenticate:  
1) Use the provided JWTs directly
2) Login with the credentials using the login prompt on the main page. Upon successful login the user will be redirected to a page that displays the newly generated JWT for the account.

⚠️ Make sure to generate a new token if the existing one(s) don't work. In case of running the tests with pytest, the new token must be updated in config.py

```
https://jalapino-api.herokuapp.com
```

##### Test Customer #0 *(JWT as in config.py)*
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
##### Test Restaurant #0 *(JWT as in config.py)*
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
```javascript
// Sample response
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

---

### GET /restaurants

ℹ️ Return a list of all restaurants paginated. The default number of items per page is 10.<br>
⚠️ If the ?page query parameter is beyond the number of available pages, a 404 error will be returned.

```bash
# Sample request
curl -X GET 'https://jalapino-api.herokuapp.com/restaurants?page=1'
```
```jsonc
// Sample response
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

---

#### GET /categories/:id/questions


ℹ️ Returns all questions filtered by category id & paginated, in the specified format. The number of returned items per page is set to 10.<br>
⚠️ If the ?page query parameter is beyond the number of available pages, an empty list of questions is returned.

```bash
# Sample request
curl -X GET 'localhost:5000/categories/1/questions'
```
```javascript
// Sample response
{
  "current_category": {
    "1": "Science"
  }, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    // 4 questions removed for brevity in this preview
    {
      "answer": "Jupiter", 
      "category": 1, 
      "difficulty": 1, 
      "id": 26, 
      "question": "What is largest planet in our solar system?"
    }
  ], 
  "total_questions": 6
}
```

---

#### POST /questions  

*Create a new question*

ℹ️ Creates a new question in the database. Returns the questions produced by `GET /questions`

```bash
# Sample request
curl -X POST 'localhost:5000/questions' \
-H "Content-Type: application/json" \
-d '{"question": "Q", "answer": "A", "category": "1", "difficulty": 1}'
```
```javascript
// Sample response
// See above under GET /questions
```

---

#### POST /questions  

*Search questions by title*

ℹ️ Case-insensitive search in question titles. Partial search terms supported. Returns questions in the same format as `GET /questions`.

```bash
# Sample request
curl -X POST 'localhost:5000/questions' -H "Content-Type: application/json" -d '{"searchTerm": "title"}'
```
```javascript
// Sample response
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "total_questions": 1
}
```

---

#### POST /quiz  

ℹ️ Play the trivia quiz. Returns a single random question either from a specific or a random category. The endpoint requires a list of `previous_questions` containing as elements the database IDs of previously displayed questions in the current quiz game. The request must also specify the `quiz_category` in the following format: {"id": "1", "type": "Science"}.  
⚠️ If no category is selected, the ID should be set to "0".

```bash
# Sample request
curl -X POST 'localhost:5000/quiz' \
-H "Content-Type: application/json" \
-d '{"previous_questions": [], "quiz_category": {"id": "1", "type": "Science"}}'
```
```javascript
// Sample response
{
  "question": {
    "answer": "The Liver", 
    "category": 1, 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the heaviest organ in the human body?"
  }
}
```

---

#### DELETE /questions/:id

ℹ️ Delete a question from the database. On successful deletion, returns the questions as defined by `GET /questions` + the requested ID as "deleted_id".

```bash
# Sample request
curl -X DELETE 'localhost:5000/questions/1'
```
```javascript
// Sample response
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "deleted_id": 1, 
  "questions": [...],
  "total_questions": 20
}
```

---

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

To run the backend locally:
```bash
# Set up the environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Create and populate db
createdb jalapino
psql jalapino < jalapino.sql

# Export environment variables
source .env

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