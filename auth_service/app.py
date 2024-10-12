from flask import Flask, request, jsonify
import requests
import jwt
import datetime

USER_SERVICE_URL = 'http://user_service:5000/users/'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')

    response = requests.get(USER_SERVICE_URL + username)
    if response.status_code != 200:
        return jsonify({"error": "User not registered"}), 403

    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
    }, app.config['SECRET_KEY'],
        algorithm="HS256")

    return jsonify({"token": token})


@app.route('/verify/<username>', methods=['POST'])
def verify_jwt(username):
    try:
        jwt.decode(request.headers.get('token'),
                   app.config['SECRET_KEY'],
                   algorithms=["HS256"])
    except:
        return jsonify({"error": "Token is not valid"}), 403

    return '', 200


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
