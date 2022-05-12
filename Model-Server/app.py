# -*- coding: utf-8 -*-
import requests
from flask import Flask, request, jsonify
from crawling.baekjoon import lately_solved_problem_seq_collection, total_solved_problem_seq_collection
from preprocessing.preprocessing import preprocessing_seq_problem_id2idx, preprocessing_seq_idx2problem_id

app = Flask(__name__)

@app.route('/', methods = ["POST"])
def main():
    if request.method == 'POST':
        
        if request.json['key'] == 123456:
            user_id = request.json['user_id']
            # user_id = request.form['user_id']

            # 백준 아이디에 따른 추가 데이터 수집
            # (1) 백준 아이디 기준 최근 20개 문제 수집 (맞았습니다.)
            lately_solved_problem_seq = lately_solved_problem_seq_collection(user_id)

            # (2) 백준 아이디 지금 까지 푼 문제 리스트 수집
            total_solved_problem_seq = total_solved_problem_seq_collection(user_id)

            if lately_solved_problem_seq:
                # 모델 인풋 데이터 정제 (문제를 idx화 + 존재하지 않는 문제 제거)
                lately_solved_problem_seq = preprocessing_seq_problem_id2idx(lately_solved_problem_seq)
                if lately_solved_problem_seq:
                    # 백준 아이디 지금 까지 푼 문제 리스트 정제 (문제를 idx화 + 존재하지 않는 문제 제거)
                    total_solved_problem_seq = preprocessing_seq_problem_id2idx(total_solved_problem_seq)

                    # 모델
                    ## output = model(lately_solved_problem_seq)
                    
                    # 모델 아웃풋 데이터 필터링
                    ## output = 필터링 (풀었던 문제 list 제거 + argsort Top10 문제 추출)

                    # 모델 아웃풋 데이터 정제(idx를 문제 번호로 변환)
                    output = preprocessing_seq_idx2problem_id(lately_solved_problem_seq)
                    
                else:
                    output = '최근 문제가 없는 유저 입니다.'
            else:
                output = '최근 문제가 없는 유저 입니다.'

        else:
            output = '존재하지 않는 key 값 입니다.'

        datas = {'output': output}

        return jsonify(datas)

if __name__ == '__main__':
    # app.run(debug = True)
    app.run(host='0.0.0.0', debug = False, port = 30005)