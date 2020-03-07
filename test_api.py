from flask import Flask, json, request, jsonify

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


@app.route('/login', methods=['post'])
def login():
    res = dict()
    data = json.loads(request.get_data())
    user = data['user']
    pwd = data['pwd']
    if user == 'admin' and pwd == '123456':
        res['code'] = '10000'
        res['msg'] = '验证通过'
    elif user == '':
        res['code'] = '10001'
        res['msg'] = '用户名为空'
    elif user == 'admin' and pwd != '123456':
        res['code'] = '10002'
        res['msg'] = '密码错误'
    elif user != 'admin':
        res['code'] = '10003'
        res['msg'] = '用户名不存在'
    return jsonify(res)


@app.route('/user/query', methods=['get'])
def query_user():
    res = dict()
    user_id = request.args.get('uid')
    print(f"{user_id=}")
    # user_id = data['uid']
    if user_id:
        res['code'] = '10000'
        res['msg'] = f'返回用户id为{user_id}的数据'
    else:
        res['code'] = '10001'
        res['msg'] = '参数不正确'
    return jsonify(res)



@app.route('/user/insert', methods=['post'])
def insert_user():
    res = dict()
    data = json.loads(request.get_data())
    user_name = data['user']
    user_sex = data['sex']
    if user_name and user_sex:
        res['code'] = '10000'
        res['msg'] = f'新增成功'
    else:
        res['code'] = '10001'
        res['msg'] = '参数不正确'
    return jsonify(res)


@app.route('/user/update', methods=['post'])
def update_user():
    pass


if __name__ == "__main__":
    app.run(debug=True)
