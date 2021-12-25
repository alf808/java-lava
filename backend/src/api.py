import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

class ValidationError(Exception):
    '''Inherit exception class to use for validation error'''
    pass

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''
db_drop_and_create_all()

# ROUTES
'''
public endpoint GET /drinks: returns status code 200 and
json {"success": True, "drinks": drinks} where drinks is the list of drinks
'''
@app.route('/drinks', methods=['GET','OPTIONS'])
def get_drinks():
    query = Drink.query.all()

    if not query:
        abort(404)
    return jsonify({
        'success': True,
        'drinks': [drink.short() for drink in query]
    })

'''
GET /drinks-detail endpoint:
    require the 'get:drinks-detail' permission
    returns status code 200 and json {"success": True, "drinks": drinks}
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    query = Drink.query.all()
    if not query:
        abort(404)
    return jsonify({
        'success': True,
        'drinks': [drink.long() for drink in query]
    })

'''
endpoint POST /drinks create a new row in the drinks table
returns status code 200 and json {"success": True, "drinks": drink}
where drink an array containing only the newly created drink
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    body = request.get_json()

    try:
        title = body.get('title', 'Generic')
        recipe = body.get('recipe', None)
        if not any(body.values()) or not recipe:
            raise ValidationError('Recipe is required')

        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()
    except (ValidationError, AttributeError) as ve:
        abort(422, description=ve)
    except Exception as e:
        abort(422, description=e)

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    drink = Drink.query.get(id)
    if not drink:
        abort(404)
        
    try:
        body = request.get_json()
        if body.get('title'):
            drink.title = body.get('title')
        if body.get('recipe'):
            drink.recipe = json.dumps(body.get('recipe'))
        else:
            raise ValidationError('Recipe is required.')
#        drink.update()
    except ValidationError as ve:
        abort(422, description=ve)
    # except Exception as e:
    #     abort(422, description=e)
    else:
        json_obj = jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    finally:
        print(body)
    return json_obj

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

# Error Handling
'''
Example error handling for unprocessable entity
'''

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''

if __name__ == "__main__":
    app.debug = True
    app.run()
