from flask import Flask, request, Response, json, render_template, redirect, jsonify
from qms import User, save_user, get_steps, enqueue_job, success_q_to_res, signup, login_helper, job_q_to_qms, check_result, hvi_users, get_fraud_transactions, save_transaction
from fraud.query_checker import checker
from datetime import date
import threading
from werkzeug.datastructures import ImmutableMultiDict
from mobile import check_otp, generate_otp, send_whatsapp

app = Flask(__name__)

# routes
@app.route('/', methods=['GET'])
def welcome():
    try:
        return render_template('landing.html')
    except Exception as e:
        return render_template('error.html', error = str(e))


# auth endpoints
@app.route('/signup', methods=['GET','POST'])
def register():
    try:
        if request.method == 'GET':
            return render_template('signup.html', request = request)
        elif request.method == 'POST':
            res = request.form
            print(res)
            name, e_id, mobile, role = res['name'], res['e_id'], res['mobile'], res['role']
            result = signup(name, e_id, role)
            if result is not 'success':
                raise Exception('Cant register user: ' + str(result))
            return render_template('login.html', request = request)
    except Exception as e:
        return render_template('error.html', error = str(e))


@app.route('/login', methods=['GET','POST'])
def login():
    try:
        if request.method == 'GET':
            return render_template('login.html', request = request)
        elif request.method == 'POST':
            r = request.form
            name, e_id, role = r['name'], r['e_id'], r['role']
            token = login_helper(name, e_id)
            if token is not 'success_token':
                raise Exception('User not registered: ' + str(token))
            hvi = hvi_users()
            transactions = get_fraud_transactions()
            return render_template('dashboard.html', user = {'hvi': hvi, 'transactions': transactions, 'name': name, 'role': role})
    except Exception as e:
        return render_template('error.html', error = str(e))


@app.route('/logout', methods=['GET'])
def logout():
    try:
        return redirect('http://192.168.43.50:5000/login', code=302)
    except Exception as e:
        return render_template('error.html', error = str(e))


# business logic endpoints
@app.route('/poll', methods=['POST'])
def poller():
    try:
        r = request.get_json()
        uid = r['uid']
        result = check_result(uid)
        if result['msg'] == 'changed':
            return Response(response=json.dumps(result['res'], status=200, mimetype="application/json"))
        return Response(response=json.dumps('unchanged'), status=200)
    except Exception as e:
        print(str(e))
        return Response('{"error":"' + str(e) + '"}', status=400)


@app.route('/fn/<string:uid>', methods=['POST'])
def handle_fn(uid):
    try:
        r = request.get_json()
        status = save_user(uid, r['purpose'], r['priority'])
        if status is not 'success':
            raise Exception('User not saved')
        steps = get_steps(r['purpose'])
        return Response(response=json.dumps(steps), status=200, mimetype="application/json")
    except Exception as e:
        print(str(e))
        return Response('{"error":"' + str(e) + '"}', status=400)


@app.route('/done/<string:uid>', methods=['POST'])
def handle_done(uid):
    try:
        r = request.get_json()
        user = User(uid, r['purpose'], r['priority'])
        enqueue_job(user)
        result = success_q_to_res(uid)
        if not result:
            raise Exception('No response from logic')
        return Response(response=json.dumps(result), status=200, mimetype="application/json")
    except Exception as e:
        return Response('{"error":"' + str(e) + '"}', status=400)


# fraud endpoint
@app.route('/checker', methods=['POST'])
def check_query():
    query_data = request.form
    query_data = query_data.to_dict(flat=False)
    print(query_data)
    role = int(query_data['role'][0])
    query = query_data['query'][0].split(',')
    for index in range(0, len(query)):
        query[index] = int(query[index])
    query = [0] + query
    user = 0
    timestamp = date.today()
    transaction = [role, user, timestamp, query]
    result = checker(transaction)
    transaction.append(result)
    save_transaction(transaction)
    print(transaction)
    return jsonify({'response' : result})


# mobile endpoints
@app.route('/otp', methods=['POST'])
def handle_otp():
    try:
        r = request.get_json()
        result = generate_otp(r['contact'])
        if result is not 'success':
            raise Exception('Exception. ' + str(result))
        return Response(response=json.dumps(result), status=200, mimetype="application/json")
    except Exception as e:
        print(str(e))
        return Response('{"error":"' + str(e) + '"}', status=400)


@app.route('/check', methods=['POST'])
def handle_check():
    try:
        r = request.get_json()
        result = check_otp(r['contact'], r['otp'])
        return Response(response=json.dumps(result), status=200, mimetype="application/json")
    except Exception as e:
        return Response('{"error":"' + str(e) + '"}', status=400)


@app.route('/wa', methods=['POST'])
def handle_whatsapp():
    try:
        r = request.get_json()
        result = send_whatsapp(r['message'])
        print(result)
        return Response(response=json.dumps(result), status=200, mimetype="application/json")
    except Exception as e:
        return Response('{"error":"' + str(e) + '"}', status=400)


# serve app
if __name__ == '__main__':
    job = threading.Thread(target=job_q_to_qms, args=())
    job.daemon = True
    job.start()
    app.run(host='192.168.43.50', port='5000', debug=True)