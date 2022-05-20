# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_restx import Api, Resource, fields
from crawling.baekjoon import lately_solved_problem_seq_collection, total_solved_problem_seq_collection
from model.model import preprocessing_seq_problem_id2idx, preprocessing_seq_idx2problem_id, output_fitering, output_sorted, thompson_sampling, item2vec_model, user_seq_model, pretrained_user_seq_model, ease_model

app = Flask(__name__)
api = Api(app, title = "SantaBaekjoon's API Server", description = "SantaBaekjoon's Recomeder Problem-id list API", version = "0.1")

santa_bacek_joon_api = api.namespace('', description = '문제 추천 list 반환 산타 백준 api')

santa_bacek_joon_api_fields = santa_bacek_joon_api.model('Input', {  # Model 객체 생성
    'key': fields.Integer(description='인증을 위한 key 값', required=True),
    'username': fields.String(description='검색을 위한 user-ID', required=True, example = 'ID'),
})

santa_bacek_joon_api_returns = santa_bacek_joon_api.model('Output', {  # Model 객체 생성
    'model_type': fields.String(description='추천된 모델의 Type', required=True, example = "item2vec or user_seq or pretrained_user_seq"),
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
        
        # 추후에 DB와 연동
        model_type_click_dict = {
            'item2vec' : {'pos_click' : 1, 'total_view' : 1},
            'user_seq' : {'pos_click' : 1, 'total_view' : 1},
            'pretrained_user_seq' : {'pos_click' : 1, 'total_view' : 1},
        }
        
        model_type = 'Not-Found-Key'
        non_filtering_output = 'Not-Found-Key'
        lately_filtering_output = 'Not-Found-Key'
        total_filtering_output = 'Not-Found-Key'
        if request.json['key'] == 123456:
            model_type = 'Not-Found-User'
            non_filtering_output = 'Not-Found-User'
            lately_filtering_output = 'Not-Found-User'
            total_filtering_output = 'Not-Found-User'

            # 백준 아이디에 따른 추가 데이터 수집
            # (1) 백준 아이디 기준 지금 까지 푼 문제 리스트 수집
            user_id = request.json['username']
            total_solved_problem_seq = total_solved_problem_seq_collection(user_id)
            if total_solved_problem_seq != 'Not-Found-User':
                model_type = 'Not-Found-User-Lately-Solved-Problem'
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
                        
                        # MAB
                        model_type = thompson_sampling(model_type_click_dict)

                        # 추천
                        if model_type == 'item2vec':
                            output = item2vec_model(lately_solved_problem_seq)
                        elif model_type == 'user_seq':
                            output = user_seq_model(lately_solved_problem_seq)
                        elif model_type == 'pretrained_user_seq':
                            output = pretrained_user_seq_model(lately_solved_problem_seq)

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
            'model_type'   : model_type,
            'non_filtering_output'   : non_filtering_output,
            'lately_filtering_output': lately_filtering_output,
            'total_filtering_output' : total_filtering_output
            }

        return datas

santa_bacek_joon_model_test_api = api.namespace('test', description = '모델 성능 Test API')

santa_bacek_joon_model_test_api_fields = santa_bacek_joon_model_test_api.model('Model-Test-Input', {  # Model 객체 생성
    'key': fields.Integer(description='인증을 위한 key 값', required=True),
    'username': fields.String(description='검색을 위한 user-ID', required=True, example = 'ID'),
})

santa_bacek_joon_model_test_api_returns = santa_bacek_joon_model_test_api.model('Model-Test-Output', {  # Model 객체 생성
    'item2vec': fields.String(description='item2vec 지금 까지 푼 모든 문제 리스트가 필터링된 추천 List', required=True, example = "['1000', '1001'....]"),
    'user_seq': fields.String(description='user_seq 지금 까지 푼 모든 문제 리스트가 필터링된 추천 List', required=True, example = "['1000', '1001'....]"),
    'pretrained_user_seq': fields.String(description='pretrained_user_seq 지금 까지 푼 모든 문제 리스트가 필터링된 추천 List', required=True, example = "['1000', '1001'....]"),
    'ease': fields.String(description='ease 지금 까지 푼 모든 문제 리스트가 필터링된 추천 List', required=True, example = "['1000', '1001'....]"),
})

@santa_bacek_joon_model_test_api.route('/')
class SantaBacekJoonApiModelTestServer(Resource):

    @santa_bacek_joon_model_test_api.expect(santa_bacek_joon_model_test_api_fields)
    @santa_bacek_joon_model_test_api.response(200, 'Success', santa_bacek_joon_model_test_api_returns)
    def post(self):
        """각 모델에 따른 추천 결과를 반환합니다."""

        item2vec = 'Not-Found-Key'
        user_seq = 'Not-Found-Key'
        pretrained_user_seq = 'Not-Found-Key'
        ease = 'Not-Found-Key'

        if request.json['key'] == 123456:
            item2vec = 'Not-Found-User'
            user_seq = 'Not-Found-User'
            pretrained_user_seq = 'Not-Found-User'
            ease = 'Not-Found-User'

            # 백준 아이디에 따른 추가 데이터 수집
            # (1) 백준 아이디 기준 지금 까지 푼 문제 리스트 수집
            user_id = request.json['username']
            total_solved_problem_seq = total_solved_problem_seq_collection(user_id)
            if total_solved_problem_seq != 'Not-Found-User':
                item2vec = 'Not-Found-User-Lately-Solved-Problem'
                user_seq = 'Not-Found-User-Lately-Solved-Problem'
                pretrained_user_seq = 'Not-Found-User-Lately-Solved-Problem'
                ease = 'Not-Found-User-Lately-Solved-Problem'

                # 백준 아이디에 따른 추가 데이터 수집
                # (2) 백준 아이디 기준 최근 20개 문제 수집 (맞았습니다.)
                lately_solved_problem_seq = lately_solved_problem_seq_collection(user_id)

                if lately_solved_problem_seq:
                    # 모델 인풋 데이터 정제 (문제를 idx화 + 존재하지 않는 문제 제거)
                    lately_solved_problem_seq = preprocessing_seq_problem_id2idx(lately_solved_problem_seq)
                    if lately_solved_problem_seq:
                        # 백준 아이디 지금 까지 푼 문제 리스트 정제 (문제를 idx화 + 존재하지 않는 문제 제거)
                        total_solved_problem_seq = preprocessing_seq_problem_id2idx(total_solved_problem_seq)

                        item2vec = item2vec_model(lately_solved_problem_seq)
                        item2vec = output_fitering(output=item2vec, fiterling_list=total_solved_problem_seq)
                        item2vec = output_sorted(output=item2vec, top=10)
                        item2vec = preprocessing_seq_idx2problem_id(item2vec)

                        user_seq = user_seq_model(lately_solved_problem_seq)
                        user_seq = output_fitering(output=user_seq, fiterling_list=total_solved_problem_seq)
                        user_seq = output_sorted(output=user_seq, top=10)
                        user_seq = preprocessing_seq_idx2problem_id(user_seq)

                        pretrained_user_seq = pretrained_user_seq_model(lately_solved_problem_seq)
                        pretrained_user_seq = output_fitering(output=pretrained_user_seq, fiterling_list=total_solved_problem_seq)
                        pretrained_user_seq = output_sorted(output=pretrained_user_seq, top=10)
                        pretrained_user_seq = preprocessing_seq_idx2problem_id(pretrained_user_seq)

                        ease = ease_model(total_solved_problem_seq)
                        ease = output_fitering(output=ease, fiterling_list=total_solved_problem_seq)
                        ease = output_sorted(output=ease, top=10)
                        ease = preprocessing_seq_idx2problem_id(ease)

        datas = {
            'item2vec'           : item2vec,
            'user_seq'           : user_seq,
            'pretrained_user_seq': pretrained_user_seq,
            'ease'               : ease,
            }

        return datas

if __name__ == '__main__':
    # app.run(debug = True)
    app.run(host='0.0.0.0', debug = False, port = 30005)