from flask import Flask, request, Response, json
from master import save_user, get_steps, enqueue_job, success_q_to_res

app = Flask(__name__)

# routes

@app.route('/', methods=['GET'])
def welcome():
    try:
        return Response('{"status":"success"}', status=200)
    except Exception as e:
        return Response('{"error":"' + str(e) + '"}', status=400)


@app.route('/fn/<string:uid>', methods=['POST'])
def handle_fn(uid):
    try:
        r = request.get_json()
        status = save_user(uid, r['purpose'], r['priority'])
        if status is not 'success':
            raise Exception('User not saved')
        steps = get_steps(r['purpose'])
        return Response(response=json.dumps(steps), status=200)
    except Exception as e:
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
        return Response(response=json.dumos(result), status=200)
    except Exception as e:
        return Response('{"error":"' + str(e) + '"}', status=400)


# serve app
if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)