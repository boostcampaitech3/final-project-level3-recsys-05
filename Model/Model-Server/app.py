# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_restx import Api, Resource, fields
from crawling.baekjoon import lately_solved_problem_seq_collection, total_solved_problem_seq_collection
from model.model import preprocessing_seq_problem_id2idx, preprocessing_seq_idx2problem_id, word2vec_model, output_fitering, output_sorted, user_seq_model

app = Flask(__name__)
api = Api(app, title = "SantaBaekjoon's API Server", description = "SantaBaekjoon's Recomeder Problem-id list API", version = "0.1")

santa_bacek_joon_api = api.namespace('', description = '문제 추천 list 반환 산타 백준 api')

santa_bacek_joon_api_fields = santa_bacek_joon_api.model('Input', {  # Model 객체 생성
    'key': fields.Integer(description='인증을 위한 key 값', required=True),
    'username': fields.String(description='검색을 위한 user-ID', required=True, example = 'ID'),
})

santa_bacek_joon_api_returns = santa_bacek_joon_api.model('Output', {  # Model 객체 생성
    'non_filtering_output': fields.String(description='필터링 되지 않은 추천 List', required=True, example = "Not-Found-Key or Not-Found-User or Not-Found-User-Lately-Solved-Problem or ['1000', '1001'....]"),
    'lately_filtering_output': fields.String(description='최근 풀이에 속하는 문제가 필터링된 추천 List', required=True, example = "Not-Found-Key or Not-Found-User or Not-Found-User-Lately-Solved-Problem or ['1000', '1001'....]"),
    'total_filtering_output' : fields.String(description='지금 까지 푼 모든 문제가 필터링된 추천 List', required=True, example = "Not-Found-Key or Not-Found-User or Not-Found-User-Lately-Solved-Problem or ['1000', '1001'....]"),
})

@santa_bacek_joon_api.route('/')
class SantaBacekJoonApiServer(Resource):

    @santa_bacek_joon_api.expect(santa_bacek_joon_api_fields)
    @santa_bacek_joon_api.response(200, 'Success', santa_bacek_joon_api_returns)
    def post(self):
        """해당 유저에 대한 추천 문제를 반환 합니다."""
        non_filtering_output = 'Not-Found-Key'
        lately_filtering_output = 'Not-Found-Key'
        total_filtering_output = 'Not-Found-Key'
        if request.json['key'] == 123456:
            non_filtering_output = 'Not-Found-User'
            lately_filtering_output = 'Not-Found-User'
            total_filtering_output = 'Not-Found-User'

            # 백준 아이디에 따른 추가 데이터 수집
            # (1) 백준 아이디 기준 지금 까지 푼 문제 리스트 수집
            user_id = request.json['username']
            total_solved_problem_seq = total_solved_problem_seq_collection(user_id)
            if total_solved_problem_seq != 'Not-Found-User':
                non_filtering_output = 'Not-Found-User-Lately-Solved-Problem'
                lately_filtering_output = 'Not-Found-User-Lately-Solved-Problem'
                total_filtering_output = 'Not-Found-User-Lately-Solved-Problem'

                # 백준 아이디에 따른 추가 데이터 수집
                # (2) 백준 아이디 기준 최근 20개 문제 수집 (맞았습니다.)
                lately_solved_problem_seq = lately_solved_problem_seq_collection(user_id)

                if lately_solved_problem_seq:
                    # 모델 인풋 데이터 정제 (문제를 idx화 + 존재하지 않는 문제 제거)
                    lately_solved_problem_seq = preprocessing_seq_problem_id2idx(lately_solved_problem_seq)
                    if lately_solved_problem_seq:
                        # 백준 아이디 지금 까지 푼 문제 리스트 정제 (문제를 idx화 + 존재하지 않는 문제 제거)
                        total_solved_problem_seq = preprocessing_seq_problem_id2idx(total_solved_problem_seq)

                        # 모델
                        output = user_seq_model(lately_solved_problem_seq)

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

        return datas

if __name__ == '__main__':
    # app.run(debug = True)
    app.run(host='0.0.0.0', debug = False, port = 30005)