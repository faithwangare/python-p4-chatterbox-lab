from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

#get and post
@app.route('/messages', methods=["GET","POST"])
def messages():
    if request.method == 'GET':
        messages = []
        for message in Message.query.all():
            message_dict=message.to_dict()
            messages.append(message_dict)
        response = make_response(
            jsonify(messages),
            200
        )    
        return response
    elif request.method == 'POST':
        new_message = Message(
            body=request.get_json().get("body"),
            username=request.get_json().get("username")
            
        )

        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()

        response = make_response(
            jsonify(message_dict),
            201
        )

        return response
        

#patch and delete
@app.route('/messages/<int:id>', methods=['GET','PATCH','DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if message == None:
        response_body = {
            "message":"this message doesn't exist in the database"
        }
        response = make_response(jsonify(response_body),404)
        return response
    else:
        if request.method == "GET":
            message_dict = message.to_dict()
            response = make_response(jsonify(message_dict),200)
            return response
        elif request.method == 'PATCH':
           for attr in request.get_json():
              if attr == 'body':
               message.body = request.get_json().get('body')
              elif attr == 'username':
               message.username = request.get_json().get('username')

           db.session.commit()
           message_dict = message.to_dict()
           response = make_response(
               jsonify(message_dict),
               200
           )

           return response

        elif request.method == 'DELETE':
            db.session.delete(message)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Review deleted."    
            }

            response = make_response(
                jsonify(response_body),
                200
            )

            return response

        


if __name__ == '__main__':
    app.run(port=5555)
