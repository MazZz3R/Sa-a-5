from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

AUTH_SERVICE_URL = 'http://auth_service:5000/'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(400), nullable=False)


@app.route('/messages', methods=['POST'])
def post_message():
    username = request.json.get('username')
    content = request.json.get('content')

    if len(content) > 400:
        return jsonify({"error": "Message exceeds 400 characters"}), 400

    response = requests.post(AUTH_SERVICE_URL + 'verify/' + username,
                             headers={'token': request.headers.get('token')})
    if response.status_code != 200:
        return jsonify({"error": "User is not logged in"}), 403

    new_message = Message(username=username, content=content)
    db.session.add(new_message)
    db.session.commit()

    return jsonify({"message": "Message posted successfully"}), 201


@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.id.desc()).limit(10).all()
    return jsonify([{"username": msg.username, "content": msg.content} for msg in messages]), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, host='0.0.0.0')
