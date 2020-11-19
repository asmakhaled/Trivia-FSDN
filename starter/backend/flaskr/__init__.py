import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# General Instructions for Questions 
def paginate_questions(request, selection):
  # request the page number, 1 is the default
  page = request.args.get('page', 1, type=int)                     
  start = (page-1) * QUESTIONS_PER_PAGE 
  end = start + QUESTIONS_PER_PAGE 

  # get all the questions and format it
  questions = [question.format() for question in selection]

  # current questions based on  page number
  current_questions = questions[start:end]                         

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs ^^DONE^^
  '''
  CORS(app, resources={'/': {'origins': '*'}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow ^^DONE^^
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories') 
  def get_categories():
    # get all categories
    all_categories = Category.query.all()                  
    
    Categories_list = {}
    # add the categories in the list id=type
    for category in all_categories:
      Categories_list[category.id] = category.type        

    # resource not found error (if the list is empty)
    if len (Categories_list) == 0:
      abort(404)

    # No error, return success true and Categories list
    return jsonify({
      'success': True,
      'categories': Categories_list
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions ^^DONE^^, 
  including pagination (every 10 questions) ^^DONE^^. 
  This endpoint should return a list of questions , 
  number of total questions, current category, categories . ^^DONE^^

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions') 
  def all_questions():
    # get all questions
    all_questions = Question.query.all()                             

    # paginate the questions 
    current_questions = paginate_questions(request, all_questions)  

    # get all categories
    all_categories = Category.query.all()                            
    
    Categories_list = {}
    # add the categories in the list id=type
    for category in all_categories:
      Categories_list[category.id] = category.type                  

    # resource not found error (if the list is empty)
    if len(current_questions) == 0:
      abort(404)

    total = len(all_questions)

    # No error, return success true and (questions, questions number, Categories list)
    return jsonify({
      'success': True,
      'questions': current_questions,
      'totalQuestions': total,
      'categories': Categories_list,
      'currentCategory': None 
    })


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. ^^DONE^^

  TEST: When you click the trash icon next to a question, the question will be removed. 
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE']) 
  def delete_question(question_id):
    try:
      # get the question
      question = Question.query.filter_by(id = question_id).one_or_none()       

      # resource not found error (no question found with this id)
      if question is None:
        abort(404)
      
      question.delete()

      return jsonify ({
        'success': True,
        'deleted': question_id
      })

    except:
      # unprocessable error
      abort(422)  

  '''
  @TODO: 
  Create an endpoint to POST a new question, ^^DONE^^
  which will require the question and answer text, 
  category, and difficulty score. ^^DONE^^

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST']) 
  def add_question():
    body = request.get_json()

    # get all the user's inputs 
    new_question = body.get('question',None)
    new_answer = body.get('answer',None)
    new_difficulty = body.get('difficulty',None)
    new_category = body.get('category',None)

    # check the user's inputs 
    if new_question == '' or new_answer == '' or new_difficulty =='' or new_category == '':
      # unprocessable error
      abort(422) 

    try:
      question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
      question.insert()

      
      total = len(Question.query.all())       

      return jsonify ({
        'success': True,
        'created': question.id,
        'totalQuestions': total
      })
    
    except:
      # unprocessable error
      abort(422)   

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. ^^DONE^^

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods=['POST'])
  def search_question():
    body = request.get_json()

    # get the user's inputs 
    search = body.get('searchTerm',None)

    # check the user's input
    if search == '':
      # unprocessable error
      abort(422) 

    try:
      result = Question.query.filter(Question.question.ilike(f'%{search}%')).all()

      if len(result)==0:
        # resource not found error
        abort(404)  
      
      # paginate the result
      current_questions = paginate_questions(request, result) 

      total = len(Question.query.all()) 

      return jsonify ({
        'success': True,
        'questions': current_questions,
        'totalQuestions': total
      })
    
    except:
      # unprocessable error
      abort(422)   

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. ^^DONE^^

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def quetion_by_category(category_id):
    # get the selected category 
    category = Category.query.filter_by(id=category_id).one_or_none() 

    if category is None:
      # resource not found error
      abort(404) 
    
    # get all the question with the matched category
    all_questions = Question.query.filter_by(category=category_id).all() 
    
    if len(all_questions)==0:
      # resource not found error
      abort(404) 

    # paginate the matched questions 
    current_questions = paginate_questions(request, all_questions)

    total = len(all_questions)

    return jsonify ({
        'success': True,
        'category': category.type,
        'questions': current_questions,
        'totalQuestions': total
      })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz_questions():
    body = request.get_json()

    # get the category and previous Questions
    category = body.get('quiz_category',None)
    previousQuestions = body.get('previous_questions',None)

    if((previousQuestions is None) or (category is None)):
      # resource not found error
      abort(400) 

    # if the category is "All"
    if category['id'] == 0:
      all_questions = Question.query.all()
    else:
      all_questions = Question.query.filter_by(category=category['id']).all()
    
    # select random questuon from the all_questions list 
    def get_random():
      return all_questions[random.randint(0, len(all_questions)-1)]

    next=True

    while next == True:
      #select random question
      new_question = get_random()
      # if the selected question is viewed before, then next=true, next iteration of the loop will get another random question
      if new_question.id in previousQuestions:
        # if all the questions are viewed then show the final score 
        if (len(all_questions) == len(previousQuestions)):
          formated_quesiton = None
          return jsonify({
            'success': True,
            'question': formated_quesiton
          })
        # not all questions are viewed then loop again and fetch new question
        else:
          next=True
      # view the new question 
      else:
        formated_quesiton = new_question.format()
        return jsonify({
          'success': True,
          'question': formated_quesiton
        })

    formated_quesiton = new_question.format()

    return jsonify({
      'success': True,
      'question': formated_quesiton
    })

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
    }),404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
    }),422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
    }),400

  @app.errorhandler(405)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "method not found"
    }),405


  return app

    