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
!! uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

# ROUTES
'''
public endpoint GET /drinks: returns status code 200 and
json {"success": True, "drinks": drinks} where drinks is the list of drinks
'''
@app.route('/drinks', methods=['GET'])
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
def get_drinks_detail(payload):
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
def create_drink(payload):
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
endpoint PATCH /drinks/<id>
updates the corresponding row for <id>
returns status code 200 and json {"success": True, "drinks": drink}
where drink an array containing only the updated drink
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    drink = Drink.query.get(id)
    if not drink:
        abort(404)
    body = request.get_json()

    try:
        if body.get('title'):
            drink.title = body.get('title')
        if body.get('recipe'):
            drink.recipe = json.dumps(body.get('recipe'))
        # else:
        #     raise ValidationError('Recipe is required.')
        drink.update()
    except (ValidationError, AttributeError) as ve:
        abort(422, description=ve)
    except Exception as e:
        abort(422, description=e)

    return jsonify({
            'success': True,
            'drinks': [drink.long()]
    })

'''
endpoint DELETE /drinks/<id>
delete the corresponding row for <id>
returns status code 200 and json {"success": True, "delete": id}
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    drink = Drink.query.get(id)
    if not drink:
        abort(404)
    try:
        drink.delete()
    except Exception as e:
        abort(422, description=e)
    else:
        json_obj = jsonify({
            'success': True,
            'delete': id
        })
    return json_obj

# Error Handling

'''Example error handling for unprocessable entity'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
    }), 422

'''Error handling for resource not found'''
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404

'''Error handling for bad request'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400

'''Error handling for unauthorized'''
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'unauthorized'
    }), 401

'''Error handling for Authentication Error'''
@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'success': False,
        'error': 403,
        'message:': 'forbidden permission required'
    }), 403

'''Error handling for AuthError'''
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error
    }), error.status_code


if __name__ == "__main__":
    app.debug = True
    app.run()