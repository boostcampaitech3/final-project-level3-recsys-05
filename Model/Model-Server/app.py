# -*- coding: utf-8 -*-
from attr import field, fields_dict
from flask import Flask, request
from flask_restx import Api, Resource, fields
from crawling.baekjoon import lately_solved_problem_seq_collection, total_solved_problem_seq_collection
from model.model import thompson_sampling, item2vec_model, user_seq_model, pretrained_user_seq_model, ease_model, multi_modal_user_seq_model
from model.model import clean_item2vec_model, clean_user_seq_model, clean_pretrained_user_seq_model, clean_ease_model, clean_multi_modal_user_seq_model
from preprocessing.preprocessing import output_fitering, output_sorted, serch_best_tag, serch_rank
from preprocessing.preprocessing import preprocessing_seq_problem_id2idx, preprocessing_seq_idx2problem_id
from preprocessing.preprocessing import clean_preprocessing_seq_problem_id2idx, clean_preprocessing_seq_idx2problem_id


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

model_output = santa_bacek_joon_model_test_api.model(
    'model', {
        'user_seq': fields.String(description='user_seq 지금 까지 푼 모든 문제 리스트가 필터링된 추천 List', required=True, example = "['1000', '1001'....]"),
        'pretrained_user_seq': fields.String(description='pretrained_user_seq 지금 까지 푼 모든 문제 리스트가 필터링된 추천 List', required=True, example = "['1000', '1001'....]"),
        'multi_modal_user_seq': fields.String(description='multi_modal_user_seq 지금 까지 푼 모든 문제 리스트가 필터링된 추천 List', required=True, example = "['1000', '1001'....]"), 
        'ease': fields.String(description='ease 지금 까지 푼 모든 문제 리스트가 필터링된 추천 List', required=True, example = "['1000', '1001'....]"),
        'pretrained_user_seq_and_ease': fields.String(description='pretrained_user_seq의 필터링으로 ease를 사용하고 지금 까지 푼 모든 문제 리스트가 필터링된 추천 List', required=True, example = "['1000', '1001'....]"),
    }
)

tag_output = santa_bacek_joon_model_test_api.model(
    'tag', {
        'lately_preference_tags': fields.String(description='최근에 푼 문제 리스트로 파악된 선호', required=True, example = "['구현', '수학'....]"),
        'total_preference_tags': fields.String(description='지금 까지 푼 모든 문제 리스트로 파악된 선호', required=True, example = "['구현', '수학'....]"),
    }
)

santa_bacek_joon_model_test_api_returns = santa_bacek_joon_model_test_api.model('Model-Test-Output', {
        'model' : fields.Nested(model_output),
        'tag' : fields.Nested(tag_output),
        'rank' : fields.String(description='최근 문제 푼 리스트 + 전체 문제 푼 리스트를 이용하여 파악된 수준', required=True, example = "'Silver III'"),
})

@santa_bacek_joon_model_test_api.route('/')
class SantaBacekJoonApiModelTestServer(Resource):

    @santa_bacek_joon_model_test_api.expect(santa_bacek_joon_model_test_api_fields)
    @santa_bacek_joon_model_test_api.response(200, 'Success', santa_bacek_joon_model_test_api_returns)
    def post(self):
        """각 모델에 따른 추천 결과를 반환합니다."""
        lately_preference_tags = 'Not-Found-Key'
        total_preference_tags = 'Not-Found-Key'
        rank = 'Not-Found-Key'

        item2vec = 'Not-Found-Key'
        ease = 'Not-Found-Key'
        user_seq = 'Not-Found-Key'
        pretrained_user_seq = 'Not-Found-Key'
        multi_modal_user_seq = 'Not-Found-Key'

        clean_item2vec = 'Not-Found-Key'
        clean_ease = 'Not-Found-Key'
        clean_user_seq = 'Not-Found-Key'
        clean_pretrained_user_seq = 'Not-Found-Key'
        clean_multi_modal_user_seq = 'Not-Found-Key'

        if request.json['key'] == 123456:

            lately_preference_tags = 'Not-Found-User'
            total_preference_tags = 'Not-Found-User'
            rank = 'Not-Found-User'

            item2vec = 'Not-Found-User'
            ease = 'Not-Found-User'
            user_seq = 'Not-Found-User'
            pretrained_user_seq = 'Not-Found-User'
            multi_modal_user_seq = 'Not-Found-User'

            clean_item2vec = 'Not-Found-User'
            clean_ease = 'Not-Found-User'
            clean_user_seq = 'Not-Found-User'
            clean_pretrained_user_seq = 'Not-Found-User'
            clean_multi_modal_user_seq = 'Not-Found-User'

            # 백준 아이디에 따른 추가 데이터 수집
            # (1) 백준 아이디 기준 지금 까지 푼 문제 리스트 수집
            user_id = request.json['username']
            total_solved_problem_seq = total_solved_problem_seq_collection(user_id)
            if total_solved_problem_seq != 'Not-Found-User':

                lately_preference_tags = 'Not-Found-User-Lately-Solved-Problem'
                total_preference_tags = 'Not-Found-User-Lately-Solved-Problem'
                rank = 'Not-Found-User-Lately-Solved-Problem'

                item2vec = 'Not-Found-User-Lately-Solved-Problem'
                ease = 'Not-Found-User-Lately-Solved-Problem'
                user_seq = 'Not-Found-User-Lately-Solved-Problem'
                pretrained_user_seq = 'Not-Found-User-Lately-Solved-Problem'
                multi_modal_user_seq = 'Not-Found-User-Lately-Solved-Problem'

                clean_item2vec = 'Not-Found-User-Lately-Solved-Problem'
                clean_ease = 'Not-Found-User-Lately-Solved-Problem'
                clean_user_seq = 'Not-Found-User-Lately-Solved-Problem'
                clean_pretrained_user_seq = 'Not-Found-User-Lately-Solved-Problem'
                clean_multi_modal_user_seq = 'Not-Found-User-Lately-Solved-Problem'

                # 백준 아이디에 따른 추가 데이터 수집
                # (2) 백준 아이디 기준 최근 20개 문제 수집 (맞았습니다.)
                lately_solved_problem_seq = lately_solved_problem_seq_collection(user_id)

                if lately_solved_problem_seq:
                    # 모델 인풋 데이터 정제 (문제를 idx화 + 존재하지 않는 문제 제거)
                    pre_lately_solved_problem_seq = preprocessing_seq_problem_id2idx(lately_solved_problem_seq)
                    clean_pre_lately_solved_problem_seq = clean_preprocessing_seq_problem_id2idx(lately_solved_problem_seq)

                    if pre_lately_solved_problem_seq:

                        # 백준 아이디 지금 까지 푼 문제 리스트 정제 (문제를 idx화 + 존재하지 않는 문제 제거)
                        pre_total_solved_problem_seq = preprocessing_seq_problem_id2idx(total_solved_problem_seq)
                        clean_pre_total_solved_problem_seq = clean_preprocessing_seq_problem_id2idx(total_solved_problem_seq)
                        
                        # rank + tag
                        lately_preference_tags = serch_best_tag(pre_lately_solved_problem_seq, top = 3)
                        total_preference_tags = serch_best_tag(pre_total_solved_problem_seq, top = 3)
                        rank = serch_rank(pre_total_solved_problem_seq, pre_lately_solved_problem_seq)

                        item2vec = item2vec_model(pre_lately_solved_problem_seq)
                        item2vec = output_fitering(output=item2vec, fiterling_list=pre_total_solved_problem_seq)
                        item2vec = output_sorted(output=item2vec, top=5)
                        item2vec = preprocessing_seq_idx2problem_id(item2vec)

                        ease = ease_model(pre_lately_solved_problem_seq)
                        ease = output_fitering(output=ease, fiterling_list=pre_total_solved_problem_seq)
                        ease = output_sorted(output=ease, top=5)
                        ease = preprocessing_seq_idx2problem_id(ease)

                        user_seq = user_seq_model(pre_lately_solved_problem_seq)
                        user_seq = output_fitering(output=user_seq, fiterling_list=pre_total_solved_problem_seq)
                        user_seq = output_sorted(output=user_seq, top=5)
                        user_seq = preprocessing_seq_idx2problem_id(user_seq)

                        pretrained_user_seq = pretrained_user_seq_model(pre_lately_solved_problem_seq)
                        pretrained_user_seq = output_fitering(output=pretrained_user_seq, fiterling_list=pre_total_solved_problem_seq)
                        pretrained_user_seq = output_sorted(output=pretrained_user_seq, top=5)
                        pretrained_user_seq = preprocessing_seq_idx2problem_id(pretrained_user_seq)

                        multi_modal_user_seq = multi_modal_user_seq_model(pre_lately_solved_problem_seq)
                        multi_modal_user_seq = output_fitering(output=multi_modal_user_seq, fiterling_list=pre_total_solved_problem_seq)
                        multi_modal_user_seq = output_sorted(output=multi_modal_user_seq, top=5)
                        multi_modal_user_seq = preprocessing_seq_idx2problem_id(multi_modal_user_seq)

                        # clean
                        clean_item2vec = clean_item2vec_model(clean_pre_lately_solved_problem_seq)
                        clean_item2vec = output_fitering(output=clean_item2vec, fiterling_list=clean_pre_total_solved_problem_seq)
                        clean_item2vec = output_sorted(output=clean_item2vec, top=5)
                        clean_item2vec = clean_preprocessing_seq_idx2problem_id(clean_item2vec)

                        clean_ease = clean_ease_model(clean_pre_lately_solved_problem_seq)
                        clean_ease = output_fitering(output=clean_ease, fiterling_list=clean_pre_total_solved_problem_seq)
                        clean_ease = output_sorted(output=clean_ease, top=5)
                        clean_ease = clean_preprocessing_seq_idx2problem_id(clean_ease)

                        clean_user_seq = clean_user_seq_model(clean_pre_lately_solved_problem_seq)
                        clean_user_seq = output_fitering(output=clean_user_seq, fiterling_list=clean_pre_total_solved_problem_seq)
                        clean_user_seq = output_sorted(output=clean_user_seq, top=5)
                        clean_user_seq = clean_preprocessing_seq_idx2problem_id(clean_user_seq)

                        clean_pretrained_user_seq = clean_pretrained_user_seq_model(clean_pre_lately_solved_problem_seq)
                        clean_pretrained_user_seq = output_fitering(output=clean_pretrained_user_seq, fiterling_list=clean_pre_total_solved_problem_seq)
                        clean_pretrained_user_seq = output_sorted(output=clean_pretrained_user_seq, top=5)
                        clean_pretrained_user_seq = clean_preprocessing_seq_idx2problem_id(clean_pretrained_user_seq)

                        clean_multi_modal_user_seq = clean_multi_modal_user_seq_model(clean_pre_lately_solved_problem_seq)
                        clean_multi_modal_user_seq = output_fitering(output=clean_multi_modal_user_seq, fiterling_list=clean_pre_total_solved_problem_seq)
                        clean_multi_modal_user_seq = output_sorted(output=clean_multi_modal_user_seq, top=5)
                        clean_multi_modal_user_seq = clean_preprocessing_seq_idx2problem_id(clean_multi_modal_user_seq)

        datas = {    
            'model' : {
                'item2vec'                     : item2vec,
                'ease'                         : ease,
                'user_seq'                     : user_seq,
                'pretrained_user_seq'          : pretrained_user_seq,
                'multi_modal_user_seq'         : multi_modal_user_seq,

                'clean_item2vec'                     : clean_item2vec,
                'clean_ease'                         : clean_ease,
                'clean_user_seq'                     : clean_user_seq,
                'clean_pretrained_user_seq'          : clean_pretrained_user_seq,
                'clean_multi_modal_user_seq'         : clean_multi_modal_user_seq,
            },

            'tag' : {
                'lately_preference_tags' : lately_preference_tags,
                'total_preference_tags'  : total_preference_tags,
            },

            'rank' : rank,
        }

        return datas

if __name__ == '__main__':
    # app.run(debug = True)
    app.run(host='0.0.0.0', debug = False, port = 30005)