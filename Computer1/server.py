from flask import Flask, render_template, request
import json
import time

#
# constant value
#
APP = Flask(__name__)
DEFAULT_WAITING_TIME_WHOLE = 20
DEFAULT_WAITING_TIME_DISH = 10
CONSUMER_DISPLAY = 4

#
# table: information of all tables in the restaurant
#       id: the id of table
#       finished: the precent of dish finished 0~100
#       dish: number of dish finished
#       time_left: time left for eating the dish
#       status: whether the table is empty, 0 = empty, 1 = occupy
#       order: how many dishes ordered
#
table = [{'id': 0, 'finished': 0, 'dish': 0, 'time_left': 0, 'status': 1, 'order': 2}, {'id': 1, 'finished': 0, 'dish': 0, 'time_left': 0, 'status': 1, 'order': 2}]

waiting_queue = [{'id': 1, 'wait': 0}, {'id': 2, 'wait': 0}, {'id': 3, 'wait': 1}, {'id': 4, 'wait': 0}, {'id': 5, 'wait': 0}]

@APP.route('/screen1')
def screen1():
    global waiting_queue, table
    time_left = []
    for t in table:
        if t['status']:
            time_left.append(t['time_left'] + (t['order'] - t['dish'] - 1) * DEFAULT_WAITING_TIME_DISH)
        else:
            time_left.append(0)
    for i in range(CONSUMER_DISPLAY - len(table)):
        time_left.append(time_left[i] + DEFAULT_WAITING_TIME_WHOLE)
    time_left.sort()
    
    for tl, wq in zip(time_left, waiting_queue):
        wq['wait'] = tl
     
    return render_template('screen1.html', waiting_queue = waiting_queue[:min(len(waiting_queue), CONSUMER_DISPLAY)])

@APP.route('/frompie')
def frompie():
    global table
    args = request.args
    id_ = int(args.get('id'))
    table[id_]['status'] = int(args.get('status'))
    if table[id_]['status']:
        table[id_]['finished'] = int(args.get('finished'))
        table[id_]['dish'] = int(args.get('dish'))
        table[id_]['time_left'] = int(args.get('time_left'))
        table[id_]['order'] = int(args.get('order'))
    return 'from pie ok'

@APP.route('/queue')
def queue():
    global waiting_queue
    waiting_queue.append({'id': waiting_queue[-1]['id'] + 1, 'wait': 0})
    return 'queue ok'

@APP.route('/dequeue')
def dequeue():
    global waiting_queue
    waiting_queue.pop(0)
    return 'dequeue ok'

if __name__ == "__main__":
    APP.run(host = '0.0.0.0', port = 35000)
