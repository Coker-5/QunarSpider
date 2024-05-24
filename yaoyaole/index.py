import datetime
import json

from flask import Flask, render_template, jsonify, request
from threading import Timer
import random
import time

last_timestamp = None
counter = 0
#client = redis.Redis(host="127.0.0.1", port=6379, db=5)

app = Flask(__name__, static_folder='liabrary')
app.config['SECRET_KEY'] = '8025431'
history = []
person_set = 0

# 初始化开奖数字和倒计时时间
current_number = None
countdown_time = 50


# 开奖随机数
def generate_random_number():
    global current_number
    global person_set
    if person_set != 0:
        print(person_set)
        current_number = str(person_set)
        person_set = 0
        history_data(current_number)
    else:
        current_number = str(random.randint(1, 100)).zfill(4)
        history_data(current_number)

# 将秒转换成分秒


def convert_seconds_to_minutes(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02d}"


# 每秒更新
def update_countdown():
    global countdown_time
    countdown_time -= 1
    if countdown_time <= 0:
        generate_random_number()
        countdown_time = 50
    timer = Timer(1, update_countdown)
    timer.start()


# 历史记录
def history_data(data):
    global history
    old_time = datetime.datetime.now()
    now_time = old_time.strftime("%m月%d日%H:%M")
    num_id = generate_unique_id()
    if len(history) == 15:
        history.pop(0)
        history.append({'id': num_id, 'time': now_time, 'result': data})
    else:
        history.append({'id': num_id, 'time': now_time, 'result': data})
    #json_data = json.dumps({'id': num_id, 'time': now_time, 'result': data})
    #client.set(num_id,json_data)


def generate_unique_id():
    global last_timestamp, counter

    current_timestamp = int(time.time())
    counter = counter+1
    unique_id = str(current_timestamp) + str(counter).zfill(3)
    return unique_id


# 自定义抽奖结果
def set_person(pwd, new_num):
    global person_set
    if pwd == 'sto0816.':
        person_set = new_num
        return True
    else:
        return False


@app.route('/')
def index():
    convert_seconds_to_minutes(countdown_time)
    return render_template('index.html')


@app.route('/get_data')
def get_data():
    str_time = convert_seconds_to_minutes(countdown_time)
    return jsonify({'number': current_number, 'countdown': str_time, 'history': history})


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/test')
def test():
    return render_template('战狼28预测.html')


@app.route('/person_num', methods=['POST'])
def person_num():
    data = request.get_json()
    pwd = data.get("pwd")
    num_by_person = data.get('person_num')
    print(pwd, num_by_person)
    result = set_person(pwd, num_by_person)
    if result:
        return jsonify({'status': 'OK', 'code': 0, 'msg': '设置成功'})
    else:
        return jsonify({'status': 'Fail', 'code': -1, 'msg': '密码错误，设置失败'})


