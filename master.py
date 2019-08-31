import pickle

job_q = list()
success_q = list()


# Models
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


# helpers
def enqueue_job(user_object):
    job_q.append(user_object)


def qms_to_success_q(user_object, counter, row):
    success_q.append(tuple(user_object, counter, row))


def success_q_to_res(uid):
    while True:
        if success_q[0][0]['uid'] is uid:
            return success_q.pop(0)


def save_user(uid, purpose, priority):
    try:
        if priority is 0:
            notify_HVI(User(uid, purpose, priority))

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
            steps.push(step_dict)

        purpose_object = Purpose(purpose, steps)

        u_dict = dict()
        u_dict[str(uid)] = purpose_object
        with open('user_purpose.pkl', 'wb') as u_purpose:
            pickle.dump(u_dict, u_purpose)

        return 'success'
    except Exception as e:
        return str(e)


def notify_HVI(user):
    pass


# data helpers
def init_data():
    func = dict()
    func['A'] = ['x', 'b', 'z']
    func['B'] = ['a', 'z', 'x']
    func['C'] = ['a', 'b', 'c']

    with open('function.pkl', 'wb') as func_store:
        pickle.dump(func, func_store)

    steps = dict()
    steps['x'] = Step('x', 3, [[],[],[]])
    steps['z'] = Step('z', 4, [[],[],[],[]])
    steps['a'] = Step('a', 2, [[],[]])
    steps['b'] = Step('b', 3, [[],[],[]])
    steps['c'] = Step('c', 4, [[],[],[],[]])

    with open('steps.pkl', 'wb') as step_store:
        pickle.dump(steps, step_store)


def get_steps(purpose):
    step_list = []
    with open('function.pkl', 'wb') as func_store:
        func = pickle.load(func_store)
        step_list = func[str(purpose)]

    return step_list


# q logic
def queue_manager(user):
    try:
        u_dict = {}
        with open('user_purpose.pkl', 'rb') as u_purpose:
            u_dict = pickle.load(u_purpose)

        purpose_object = u_dict[str(uid)]
        counter_name, prev_idx = '', -1

        # extract last visited from user state
        for i in range(len(purpose_object['steps'])-1):
            step_list = purpose_object['steps']
            if step_list[i]['visited'] is True and step_list[i+1]['visited'] is False:
                counter_name = step_list[i]['data']
                prev_idx = step_list[i]['q_index']
                break

        # remove from and set counter state
        steps = {}
        with open('steps.pkl', 'rb') as step_store:
            steps = pickle.load(step_store)

        step_object = steps[str(counter_name)]
        if step_object['counters'][idx][0]['uid'] is not user['uid']:
            return 'ghost customer'

        step_object['counters'][idx].pop(0)
        steps[str(counter_name)] = step_object

        with open('steps.pkl', 'wb') as step_store:
            pickle.dump(steps, step_store)

        # extract not visited from user state
        for step in purpose_object['steps']:
            if step['visited'] is False:
                counter_name = step['data']
                break

        # calculate and set in counter state
        steps = {}
        with open('steps.pkl', 'rb') as step_store:
            steps = pickle.load(step_store)

        step_object = steps[str(counter_name)]
        size, idx = 1000, -1
        for i in range(len(step_object['counters'])):
            if len(step_object['counters'][i]) <= size:
                size, idx = len(step_object['counters'][i]), i

        step_object['counters'][idx].append(user)
        steps[str(counter_name)] = step_object

        with open('steps.pkl', 'wb') as step_store:
            pickle.dump(steps, step_store)

        # save user state
        for step in purpose_object['steps']:
            if step['visited'] is False:
                step['visited'] = True
                step['q_index'] = idx
                break

        u_dict[str(uid)] = purpose_object
        with open('user_purpose.pkl', 'wb') as u_purpose:
            pickle.dump(u_dict, u_purpose)

        #push to success_q
        qms_to_success_q(user, counter_name, idx)
        return 'success'

    except Exception as e:
        return str(e)


init_data()
