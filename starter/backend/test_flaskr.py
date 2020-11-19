import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}@{}/{}".format('postgres:1234','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # new question for test_add_question
        self.new_question = {
            'question': 'New Question Test',
            'answer': 'New Answer Test',
            'difficulty': 3,
            'category': 3
        }

        # wrong question for test_422_add_question_failed
        self.wrong_question = {
            'question': '',
            'answer': '',
            'difficulty': 3,
            'category': 3
        }

        # search term for test_search_for_question
        self.search_term = {'searchTerm': 'name'}

        # wrong search term for test_422_search_for_question_failed
        self.wrong_search_term = {'searchTerm':''}

        # valid quiz for test_quiz 
        self.vaild_quiz = {'previous_questions': [], 'quiz_category': {'type': 'Sports', 'id': 6}}

        # invalid quiz for test_400_quiz_failed
        self.invalid_quiz = {'previous_questions': []}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors. ^^DONE^^
    """
    # test the get questions 
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['categories'])
        self.assertEqual(data['currentCategory'], None) 

    # test if the requested page does not exists 
    def test_404_invalid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # test delete a question
    def test_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 5)

    # test if we want to delete a question that does not exists 
    def test_404_delete_unavailable_question(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unprocessable')

    # test add question
    def test_add_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['totalQuestions'])

    # test if the add question failed  
    def test_422_add_question_failed(self):
        res = self.client().post('/questions', json=self.wrong_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unprocessable')


    # test get questions of a certain category
    def test_get_question_by_category(self): 
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['category'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])

    # test get questions of a certain category that does not exists 
    def test_404_get_question_by_category(self): 
        res = self.client().get('/categories/20/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # test search question
    def test_search_for_question(self):    
        res = self.client().post('/questions/search', json=self.search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
    

    # test search question failed         
    def test_422_search_for_question_failed(self):
        res = self.client().post('/questions/search', json=self.wrong_search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'unprocessable')

    
    # test get categories  
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
    
    # test test get categories failed, category 1000 does not exists      
    def test_404_get_categories_failed(self):
        res = self.client().get('/categories/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')     


    # test quiz  
    def test_quiz(self):
        res = self.client().post('/quizzes', json=self.vaild_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    # test quiz failed, missing quiz category            
    def test_400_quiz_failed(self):
        res = self.client().post('/quizzes',  json=self.invalid_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request') 

    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()