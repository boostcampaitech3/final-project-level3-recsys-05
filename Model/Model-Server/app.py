# -*- coding: utf-8 -*-
import requests
from flask import Flask, request, jsonify
from crawling.baekjoon import lately_solved_problem_seq_collection, total_solved_problem_seq_collection
from model.model import preprocessing_seq_problem_id2idx, preprocessing_seq_idx2problem_id, word2vec_model, output_fitering, output_sorted

app = Flask(__name__)

@app.route('/', methods = ["POST"])
def main():
    if request.method == 'POST':
        non_filtering_output = 'Not-Found-Key'
        lately_filtering_output = 'Not-Found-Key'
        total_filtering_output = 'Not-Found-Key'

        if request.json['key'] == 123456:
            non_filtering_output = 'Not-Found-User-Lately-Solved-Problem'
            lately_filtering_output = 'Not-Found-User-Lately-Solved-Problem'
            total_filtering_output = 'Not-Found-User-Lately-Solved-Problem'

            user_id = request.json['username']

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
                    output = word2vec_model(lately_solved_problem_seq)

                    # 필터링 + 문제 추천
                    non_filtering_output = output_sorted(output=output, top=10)

                    lately_filtering_output = output_fitering(output=output, fiterling_list=lately_solved_problem_seq)
                    lately_filtering_output = output_sorted(output=lately_filtering_output, top=10)

                    total_filtering_output = output_fitering(output=output, fiterling_list=total_solved_problem_seq)
                    total_filtering_output = output_sorted(output=total_filtering_output, top=10)

                    # 모델 아웃풋 데이터 정제(idx를 문제 번호로 변환)
                    non_filtering_output = preprocessing_seq_idx2problem_id(non_filtering_output)
                    lately_filtering_output = preprocessing_seq_idx2problem_id(lately_filtering_output)
                    total_filtering_output = preprocessing_seq_idx2problem_id(total_filtering_output)

        datas = {
            'non_filtering_output'   : non_filtering_output,
            'lately_filtering_output': lately_filtering_output,
            'total_filtering_output' : total_filtering_output
            }
        
        return jsonify(datas)

if __name__ == '__main__':
    # app.run(debug = True)
    app.run(host='0.0.0.0', debug = False, port = 30005)