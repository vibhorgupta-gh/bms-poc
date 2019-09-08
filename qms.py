import pickle, time, os

job_q = list()
success_q = list()
waiting_q = list()
high_value_user_list = list()
fraud_list = list()
customer_limit = 1
counter = 0

def make_global():
    global job_q
    global success_q
    global waiting_q
    global customer_limit
    global high_value_user_list
    global fraud_list
    global counter

make_global()

# Models
class Employee(object):
    def __init__(self, name, e_id, role):
        self.name=name
        self.e_id=e_id
        self.role=role

class User(object):
    def __init__(self, uid, purpose, priority):
        self.uid=uid
        self.purpose=purpose
        self.priority=priority

class Step(object):
    def __init__(self, name, q_num, counters):
        self.name=name
        self.q_num=q_num
        self.counters=counters

class Purpose(object):
    def __init__(self, name, steps):
        self.name=name
        self.steps=steps


# auth helpers
def signup(name, e_id, role):
    try:
        employee_dict = {}
        with open('employee.pkl', 'rb') as employees:
            employee_dict = pickle.load(employees)

        for el in employee_dict:
            if employee_dict[str(el)].e_id == e_id:
                return 'success'
        employee_dict[str(e_id)] = Employee(name, e_id, role)
        with open('employee.pkl', 'wb') as employees:
            pickle.dump(employee_dict, employees)

        return 'success'
    except Exception as e:
        return str(e)


def login_helper(name, e_id):
    try:
        employee_dict = {}
        with open('employee.pkl', 'rb') as employees:
            employee_dict = pickle.load(employees)

        for el in employee_dict:
            if employee_dict[str(el)].e_id == e_id:
                return 'success_token'

        return 'failure_token'
    except Exception as e:
        return str(e)


# helpers
def customer_in_waiting_q(wait_object):
    waiting_q.append(wait_object)


def dequeue_wait(wait_object):
    waiting_q.remove(wait_object)


def enqueue_job(user_object):
    job_q.append(user_object)


def qms_to_success_q(user_object, counter, row):
    success_q.append((user_object, counter, row))


def success_q_to_res(uid):
    while True:
        if len(success_q) == 0:
            time.sleep(0.5)
            continue
        elif success_q[0][0].uid is uid:
            response = [success_q[0][0].uid, success_q[0][1], success_q[0][2]]
            save_result(response)
            success_q.pop(0)
            return response


def save_result(response):
    try:
        res_dict = dict()
        res_dict[str(response[0])] = response
        print(response)
        with open('poller_response.pkl', 'wb') as poller_response:
            pickle.dump(res_dict, poller_response)
    except Exception as e:
        print(str(e))


def check_result(uid):
    try:
        res_dict = dict()
        result = list()
        if os.path.getsize('poller_response.pkl') > 0:
            with open('poller_response.pkl', 'rb') as poller_response:
                res_dict = pickle.load(poller_response)
            result = res_dict[str(uid)]

        return result
    except Exception as e:
        return {
            'msg': str(e)
        }


def save_user(uid, purpose, priority):
    try:
        global counter
        if counter >= 1:
            return 'success'

        elif priority is 0:
            high_value_user_list.append(User(uid, purpose, priority))

        step_list = []
        with open('function.pkl', 'rb') as func_store:
            func = pickle.load(func_store)
            step_list = func[str(purpose)]

        steps = list()
        for step in step_list:
            step_dict  = {
                'data': step,
                'visited': False,
                'q_index': -1
            }
            steps.append(step_dict)

        purpose_object = Purpose(purpose, steps)

        u_dict = dict()
        u_dict[str(uid)] = purpose_object
        with open('user_purpose.pkl', 'wb') as u_purpose:
            pickle.dump(u_dict, u_purpose)

        counter = counter + 1
        return 'success'
    except Exception as e:
        return str(e)


def hvi_users():
    return high_value_user_list

def get_fraud_transactions():
    return fraud_list

def save_transaction(transaction):
    transaction_object = {
        'role': 'Admin' if str(transaction[0]) == '0' else 'Employee',
        'user': transaction[1],
        'timestamp': transaction[2],
        'query': transaction[3],
        'status': 'Malicious' if str(transaction[4]) == '0' else 'Safe'
    }
    fraud_list.append(transaction_object)


# data helpers
def init_data():
    func = dict()
    func['Locker'] = ['x', 'b', 'z']
    func['B'] = ['a', 'z', 'x']
    func['C'] = ['a', 'b', 'c']

    steps = dict()
    steps['x'] = Step('x', 3, [[],[],[]])
    steps['z'] = Step('z', 4, [[],[],[],[]])
    steps['a'] = Step('a', 2, [[],[]])
    steps['b'] = Step('b', 3, [[],[],[]])
    steps['c'] = Step('c', 4, [[],[],[],[]])

    employee_dict = dict()
    employee_dict['666'] = Employee('John Doe', '666', '1')

    with open('function.pkl', 'wb') as func_store:
        pickle.dump(func, func_store)

    with open('steps.pkl', 'wb') as step_store:
        pickle.dump(steps, step_store)

    with open('employee.pkl', 'wb') as employees:
        pickle.dump(employee_dict, employees)


def get_steps(purpose):
    step_list = []
    with open('function.pkl', 'rb') as func_store:
        func = pickle.load(func_store)
        step_list = func[str(purpose)]

    return step_list


# q logic
def queue_manager(user):
    try:
        u_dict = {}
        with open('user_purpose.pkl', 'rb') as u_purpose:
            u_dict = pickle.load(u_purpose)

        purpose_object = u_dict[str(user.uid)]
        counter_name, prev_idx, all_visited = '', -1, True

        # extract last visited from user state
        for i in range(len(purpose_object.steps)-1):
            step_list = purpose_object.steps
            if step_list[i]['visited'] is True and step_list[i+1]['visited'] is False:
                counter_name = step_list[i]['data']
                prev_idx = step_list[i]['q_index']
                break

        # remove from and set counter state
        if prev_idx != -1:
            steps = {}
            with open('steps.pkl', 'rb') as step_store:
                steps = pickle.load(step_store)

            step_object = steps[str(counter_name)]
            if step_object.counters[prev_idx][0].uid != user.uid:
                return 'ghost customer'

            step_object.counters[prev_idx].pop(0)
            steps[str(counter_name)] = step_object

            with open('steps.pkl', 'wb') as step_store:
                pickle.dump(steps, step_store)

        # extract not visited from user state
        for step in purpose_object.steps:
            if step['visited'] is False:
                all_visited = False
                counter_name = step['data']
                break

        if all_visited is True:
            if user.priority == 0:
                for u in high_value_user_list:
                    if u.uid == user.uid:
                        high_value_user_list.remove(u)
            # qms_to_success_q(user, 'Purpose fulfilled', -1)
            return 'Purpose fulfilled'

        # calculate and set in counter state
        steps = {}
        with open('steps.pkl', 'rb') as step_store:
            steps = pickle.load(step_store)

        step_object = steps[str(counter_name)]
        size, idx = 1000, -1
        for i in range(len(step_object.counters)):
            if len(step_object.counters[i]) <= size:
                size, idx = len(step_object.counters[i]), i

        step_object.counters[idx].append(user)
        steps[str(counter_name)] = step_object

        with open('steps.pkl', 'wb') as step_store:
            pickle.dump(steps, step_store)

        # save user state
        for step in purpose_object.steps:
            if step['visited'] is False:
                step['visited'] = True
                step['q_index'] = idx
                break

        u_dict[str(user.uid)] = purpose_object
        with open('user_purpose.pkl', 'wb') as u_purpose:
            pickle.dump(u_dict, u_purpose)

        #push to success_q
        qms_to_success_q(user, counter_name, idx)
        return 'success'

    except Exception as e:
        return str(e)


def job_q_to_qms():
    while True:
        time.sleep(1)
        while len(job_q):
            user = job_q.pop(0)
            status = queue_manager(user)
            print(status)
            if status != 'success':
                enqueue_job(user)


init_data()
