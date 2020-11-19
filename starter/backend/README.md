# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. ^^DONE^^
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. ^^DONE^^
3. Create an endpoint to handle GET requests for all available categories. ^^DONE^^
4. Create an endpoint to DELETE question using a question ID. ^^DONE^^
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. ^^DONE^^
6. Create a POST endpoint to get questions based on category. ^^DONE^^
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. ^^DONE^^
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. ^^DONE^^
9. Create error handlers for all expected errors including 400, 404, 422 and 500. ^^DONE^^

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET '/questions'
DELETE '/questions/<int:question_id>'
POST '/questions'
POST '/questions/search'
GET '/categories/<int:category_id>/questions'
POST '/quizzes'


```

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: 1- Categories_list object that contains category id and category type. 2- Success is true
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}

```

GET '/questions'
- Fetches a dictionary of questions and paginate them in (def paginate_questions) 
- Request Arguments: None
- Returns: 1- Categories_list object that contains category id and category type. 2- Current Category .  3- Success is true . 4- questions object that contains (answer,category,difficulty,id,question). 5- Number of Questions
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "currentCategory": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    },
    .
    .
    .
    ], 
  "success": true, 
  "totalQuestions": 26
}

```

DELETE '/questions/<int:question_id>'
- Delete a question 
- Request Arguments: question_id
- Returns: 1- Success is True. 2- deleted question id
{
    'success': True,
    'deleted': 10
}

```

POST '/questions'
- Fetches the user's input (question,answer,difficulty,category), add the new question to the database 
- Request Arguments: None
- Returns: 1- Success is True. 2- created question id
{
    'success': True,
    'created': 27
}

```

POST '/questions/search'
- Fetches the question that matched the search term 
- Request Arguments: None
- Returns: 1- Success is True. 2- current_questions object contains questions that matched the search term. 3- Number of Questions

{
    'success': True,
    'questions': {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    },
    'totalQuestions': 26
}

```

GET '/categories/<int:category_id>/questions'
- Fetches questions filtered by certain category 
- Request Arguments: category_id
- Returns: 1- Success is True. 2- category type. 3- current_questions object contains questions filtered by certain category. 4- Number of Questions 
{
  "category": "Art", 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "success": true, 
  "totalQuestions": 4
}

```

POST '/quizzes'
- Fetches the questions based on the chosen category, then randomly choose one of the question, take the answer from the user and check whether the answer is correct or not
- Request Arguments: None 
- Returns: 1- Success is True. 2- the formated question


```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

test_get_paginated_questions (curl http://127.0.0.1:5000/questions?page=2)

test_404_invalid_page (curl http://127.0.0.1:5000/questions?page=1000)

test_delete_question (curl -X DELETE http://127.0.0.1:5000/questions/5)

test_404_delete_unavailable_question (curl -X DELETE http://127.0.0.1:5000/questions/1000)

test_add_question (curl -X POST -H "Content-Type: application/json" -d '{"question": "New Question Test","answer": "New Answer Test","difficulty": "3","category": "3"}' http://127.0.0.1:5000/questions)

test_422_add_question_failed (curl -X POST -H "Content-Type: application/json" -d '{"question": "","answer": "","difficulty": "3","category": "3"}' http://127.0.0.1:5000/questions)

test_get_question_by_category (curl http://127.0.0.1:5000/categories/1/questions)

test_404_get_question_by_category (curl http://127.0.0.1:5000/categories/20/questions)

test_search_for_question (curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "name"}' http://127.0.0.1:5000/questions/search)

test_422_search_for_question_failed (curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": ""}' http://127.0.0.1:5000/questions/search)

test_get_categories (curl http://127.0.0.1:5000/categories)

test_404_get_categories_failed (curl http://127.0.0.1:5000/categories/1000)

test_quiz (curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"type": "Sports", "id": "6"}}' http://127.0.0.1:5000/quizzes)

test_400_quiz_failed (
curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": []}' http://127.0.0.1:5000/quizzes)