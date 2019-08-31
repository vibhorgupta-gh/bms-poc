import redis
import time

r = redis.Redis(host=u'localhost',port=6379)
job_q = list()
success_q = list()

def make_global():
    global job_q
    global success_q

make_global()


# Models
class User(object):
    def __init_(self, uid, purpose, priority):
        self.uid=uid
        self.purpose=purpose
        self.priority=priority

class Step(object):
    def __init_(self, name, q_num, counters):
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


def job_q_to_qms():
    while True:
        time.sleep(1)
        while len(job_q):
            user = job_q.pop(0)
            status = queue_manager(user)
            if status is not 'success':
                enqueue_job(user)


def qms_to_success_q(user_object):
    success_q.append(user_object)


def success_q_to_res(uid):
    while True:
        if success_q[0]['uid'] is uid:
            return success_q.pop(0)


def save_user(uid, purpose, priority):
    try:
        if priority is 0:
            notify_HVI(User(uid, purpose, priority))

        step_list = r.get(str(purpose))
        steps = list()
        for step in step_list:
            step_dict  = {
                'data': step,
                'visited': False,
                'q_index': -1
            }
            steps.push(step_dict)

        purpose_object = Purpose(purpose, steps)
        r.set(uid, purpose_object)
        return 'success'
    except Exception as e:
        return str(e)


def notify_HVI(user):
    pass


# data helpers
def init_data():
    r.set('A', ['x', 'b', 'z'])
    r.set('B', ['a', 'z', 'x'])
    r.set('C', ['a', 'b', 'c'])

    r.set('x', Step('x', 3, [[],[],[]]))
    r.set('z', Step('z', 4, [[],[],[],[]]))
    r.set('a', Step('a', 2, [[],[]]))
    r.set('b', Step('b', 3, [[],[],[]]))
    r.set('c', Step('c', 4, [[],[],[],[]]))


def get_steps(purpose):
    steps = r.get(str(purpose))
    return steps


# q logic
def queue_manager(user):
    try:
        purpose_object = r.get(str(user['uid']))
        counter_name, prev_idx = '', -1

        # extract last visited from user state
        for i in range(len(purpose_object['steps'])-1):
            step_list = purpose_object['steps']
            if step_list[i]['visited'] is True and step_list[i+1]['visited'] is False:
                counter_name = step_list[i]['data']
                prev_idx = step_list[i]['q_index']
                break

        # remove from and set counter state
        step_object = r.get(str(counter_name))
        counters_list = step_object['counters']
        if counters_list[idx][0]['uid'] is not user['uid']:
            return 'ghost customer'

        counters_list[idx].pop(0)
        r.set(counter_name, step_object)

        # extract not visited from user state
        for step in purpose_object['steps']:
            if step['visited'] is False:
                counter_name = step['data']
                break

        # calculate and set in counter state
        step_object = r.get(str(counter_name))
        counters_list = step_object['counters']
        size, idx = 1000, -1
        for i in range(len(counters_list)):
            if len(counters_list[i]) <= size:
                size, idx = len(counters_list[i]), i

        counters_list[idx].append(user)
        r.set(counter_name, step_object)

        # save user state
        for step in purpose_object['steps']:
            if step['visited'] is False:
                step['visited'] = True
                step['q_index'] = idx
                break

        r.set(user['uid'], purpose_object)

        #push to success_q
        qms_to_success_q(user)
        return 'success'

    except Exception as e:
        return str(e)


init_data()
job_q_to_qms()
