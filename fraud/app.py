from flask import Flask
from query_checker import *
from flask import request
from datetime import date
from flask import jsonify
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/checker', methods=['POST'])
def check_query():
    query_data = request.json
    print(query_data)
    role = int(query_data['role'])
    query = query_data['query'].split(',')
    for index in range(0, len(query)):
        query[index] = int(query[index])
    query = [0] + query
    user = int(query_data['user'])
    timestamp = date.today()
    transaction = [role, user, timestamp, query]
    print(transaction)
    return jsonify({'response' : checker(transaction)})


if __name__ == '__main__':
    app.run(debug=True)
