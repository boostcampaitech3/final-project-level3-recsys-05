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
    contents = '''
    <form action="/result" method="post" class="serch-form">
        <input type="text" name="user_id" placeholder="Please User ID" id="userSearchInput" required="">
        <button type="submit" class="form-control">Search</button>
    </form>
    '''
    if request.method == 'POST':
        url = 'http://101.101.218.250:30005/test/'

        data = {
            'key' : 123456,
            'username' : request.form['user_id'],
        }

        res = requests.post(url, json = data)
        res = res.json()

        if not os.path.isdir(log_path):
            os.mkdir(log_path)

        if not os.path.isfile(os.path.join(log_path, log_file_name)):
            log = {model_type : 0 for model_type in res.keys()}
            with open(os.path.join(log_path, log_file_name), "w") as json_file:
                json.dump(log, json_file)

        total_content = ''

        for model_type in res.keys():
            item_list = res[model_type]
            if isinstance(item_list, str):
                return render_template('base.html', contents = ''' <div class="content"> ''' + f"<h1> {request.form['user_id']} 존재하지 않는 아이디 입니다. </h1>" + '''</div>''')

            item_list = ",".join(list(map(str, item_list)))
            url = f"https://solved.ac/api/v3/problem/lookup?problemIds={item_list}"
            headers = {"Content-Type": "application/json"}
            response = requests.request("GET", url, headers=headers)
            item_list = response.json()

            content = f'''
            <div class="item-list">
            <input type="radio" id="{model_type}" name="model_vote" value="{model_type}">
             <label for="{model_type}"> {model_type} </label><br>
            '''
            for item in item_list:
                content += f'''
                <div class="item">
                    <p id='item-name'><a href={'https://www.acmicpc.net/problem/' + str(item['problemId'])} target="_blank">{str(item['titleKo'])}</a></p>
                    <p id='item-name'>level : {item_level[item['level']]}</p>
                    <p id="item-property">acceptedUserCount : {str(item['acceptedUserCount'])}</p>
                </div>
                '''
            content += f'''</div>'''

            total_content += content

        return render_template('base.html', contents = ''' <div class="content"> <form action="/vote" method="post"> ''' + total_content + '''<input type="submit" value="Submit"> </form> </div>''')

@app.route('/vote', methods = ["POST"])
def vote():
    if request.method == 'POST':

        with open(os.path.join(log_path, log_file_name), 'r', encoding = 'utf-8') as f:
            log = json.load(f)

        log[request.form['model_vote']] += 1
        print(log)
        
        with open(os.path.join(log_path, log_file_name), "w") as json_file:
            json.dump(log, json_file)
        
        return render_template('base.html', contents = f''' <div class="content"> <h1> {request.form['model_vote']} 감사합니다 </h1> </div>''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False, port = 30001)

