import os
import json
import requests

from flask import Flask, render_template, request

app = Flask(__name__)

log_path = '/opt/ml/final-project-level3-recsys-05/Model/Model-prototype-web/log'
log_file_name = 'log.json'

item_level = {

0	:"Unrated",
1	:"Bronze V",
2	:"Bronze IV",
3	:"Bronze III",
4	:"Bronze II",
5	:"Bronze I",
6	:"Silver V",
7	:"Silver IV",
8	:"Silver III",
9	:"Silver II",
10	:"Silver I",
11	:"Gold V",
12	:"Gold IV",
13	:"Gold III",
14	:"Gold II",
15	:"Gold I",
16	:"Platinum V",
17	:"Platinum IV",
18	:"Platinum III",
19	:"Platinum II",
20	:"Platinum I",
21	:"Diamond V",
22	:"Diamond IV",
23	:"Diamond III",
24	:"Diamond II",
25	:"Diamond I",
26	:"Ruby V",
27	:"Ruby IV",
28	:"Ruby III",
29	:"Ruby II",
30	:"Ruby I",

}

@app.route('/', methods = ["GET"])
def index():
    contents = '''
    <form action="/result" method="post" class="serch-form">
        <input type="text" name="user_id" placeholder="Please User ID" id="userSearchInput" required="">
        <button type="submit" class="form-control">Search</button>
    </form>
    '''
    if request.method == 'GET':
        return render_template('base.html', contents = '''<div class="content">''' + contents + '''</div>''')

@app.route('/result', methods = ["POST"])
def result():
    if request.method == 'POST':
        url = 'http://101.101.218.250:30002/models/'

        data = {
            'key' : 123456,
            'username' : request.form['user_id'],
            "model_type_click": {}
        }

        res = requests.post(url, json = data)
        res = res.json()

        if res['problems'][0]['model_type'] == 'Not-Found-Key':
                return render_template('base.html', contents = ''' <div class="content"> ''' + f"<h1> 키 값이 들립니다. </h1>" + '''</div>''')

        if res['problems'][0]['model_type'] == 'Not-Found-User':
                return render_template('base.html', contents = ''' <div class="content"> ''' + f"<h1> {request.form['user_id']} 존재하지 않는 아이디 입니다. </h1>" + '''</div>''')

        if res['problems'][0]['model_type'] == 'Not-Found-User-Solved-Problem':
                return render_template('base.html', contents = ''' <div class="content"> ''' + f"<h1> {request.form['user_id']} 푼 문제가 없습니다. </h1>" + '''</div>''')

        if res['problems'][0]['model_type'] == 'Not-Found-User-Lately-Solved-Problem':
                return render_template('base.html', contents = ''' <div class="content"> ''' + f"<h1> {request.form['user_id']} 최근에 푼 문제가 없습니다. </h1>" + '''</div>''')

        content = f'''
        <p> {request.form['user_id']} </p>
        <p> 당신이 최근에 선호 하는 유형: {'/'.join(res['tag'])} </p>
        <div class="item-list">
        '''

        problems = res['problems']
        for problem in problems:

            url = f"https://solved.ac/api/v3/problem/show?problemId={problem['output']}"
            headers = {"Content-Type": "application/json"}
            response = requests.request("GET", url, headers=headers)
            item = response.json()

            content += f'''
            <div class="item">
                <p id='item-name'><a href={'https://www.acmicpc.net/problem/' + str(item['problemId'])} target="_blank">{str(item['titleKo'])}</a></p>
                <p id='item-name'>level : {item_level[item['level']]}</p>
                <p id="item-property">acceptedUserCount : {str(item['acceptedUserCount'])}</p>
                <p id="item-property">model_type : {str(problem['model_type'])}</p>
            </div>
            '''

        content += f'''</div>'''

        return render_template('base.html', contents = ''' <div class="content"> ''' + content + ''' </div>''')

@app.route('/vote', methods = ["POST"])
def vote():
    if request.method == 'POST':

        with open(os.path.join(log_path, log_file_name), 'r', encoding = 'utf-8') as f:
            log = json.load(f)

        log[request.form['model_vote']] += 1
        
        with open(os.path.join(log_path, log_file_name), "w") as json_file:
            json.dump(log, json_file)
        
        return render_template('base.html', contents = f''' <div class="content"> <h1> {request.form['model_vote']} 감사합니다 </h1> </div>''')

if __name__ == '__main__':
    # app.run(debug = True)
    app.run(host='0.0.0.0', debug = True, port = 30001)

