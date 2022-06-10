import os
import json
import asyncio
import uvicorn
from fastapi import FastAPI
from utlis.utils import ModelUpdateInput, ModelUpdateOutput, Input, Output, title, description, docs_url, redoc_url
from crawling.crawling import total_solved_problem_seq_crawling, lately_solved_problem_seq_crawling
from preprocessing.preprocessing import problem_seq2idx, serch_best_tag
from inference.inference import inference, thompson_sampling
from model.model import ServingEASE, ServingItem2Vec, ServingLightGCN, ServingMultiModal
from collections import deque

app = FastAPI(title=title, description=description, docs_url=docs_url, redoc_url=redoc_url)

models = {}
logging_dir = "./log"
standard_model_type_click_dict = {
                        'item2vec' : {'pos_click' : 4, 'total_view' : 25},
                        'ease' : {'pos_click' : 7, 'total_view' : 25},
                        'lightGCN' : {'pos_click' : 7, 'total_view' : 25},
                        'multi_modal' : {'pos_click' : 7, 'total_view' : 25},
                    }


@app.on_event("startup")
def startup_event():
    with open(os.path.join(logging_dir, 'model_types_to_run_id_and_model_name.json'), 'r', encoding = 'utf-8') as f:
        model_types_to_run_id_and_model_name = json.load(f)

    model_types = model_types_to_run_id_and_model_name.keys()
    for model_type in model_types:
        if model_type[:len('multi_modal')] == 'multi_modal':
            models[model_type] = ServingMultiModal(run_id=model_types_to_run_id_and_model_name[model_type]["run_id"],model_name=model_types_to_run_id_and_model_name[model_type]["model_name"])
        elif model_type[:len('lightGCN')] == 'lightGCN':
            models[model_type] = ServingLightGCN(run_id=model_types_to_run_id_and_model_name[model_type]["run_id"],model_name=model_types_to_run_id_and_model_name[model_type]["model_name"])
        elif model_type[:len('item2vec')] == 'item2vec':
            models[model_type] = ServingItem2Vec(run_id=model_types_to_run_id_and_model_name[model_type]["run_id"],model_name=model_types_to_run_id_and_model_name[model_type]["model_name"])
        elif model_type[:len('ease')] == 'ease':
            models[model_type] = ServingEASE(run_id=model_types_to_run_id_and_model_name[model_type]["run_id"],model_name=model_types_to_run_id_and_model_name[model_type]["model_name"])


@app.on_event("shutdown")
def shutdown_event():
    model_types = models.keys()
    
    model_types_to_run_id_and_model_name = {}
    for model_type in model_types:
        model_types_to_run_id_and_model_name[model_type] = {"run_id" : models[model_type].run_id, "model_name": models[model_type].model_name}
    
    with open(os.path.join(logging_dir, "model_types_to_run_id_and_model_name.json"), "w") as json_file:
        json.dump(model_types_to_run_id_and_model_name, json_file)


@app.post('/update', response_model = ModelUpdateOutput, tags=['update'], description="학습 모델 업데이트")
async def model_update(input : ModelUpdateInput) -> ModelUpdateOutput:
    state = 'Not-Found-Key'
    if input.key == 123456:
        if input.model_type[:len('multi_modal')] == 'multi_modal':
            models[input.model_type] = ServingMultiModal(run_id=input.run_id,model_name=input.model_name)
        elif input.model_type[:len('lightGCN')] == 'lightGCN':
            models[input.model_type] = ServingLightGCN(run_id=input.run_id,model_name=input.model_name)
        elif input.model_type[:len('item2vec')] == 'item2vec':
            models[input.model_type] = ServingItem2Vec(run_id=input.run_id,model_name=input.model_name)
        elif input.model_type[:len('ease')] == 'ease':
            models[input.model_type] = ServingEASE(run_id=input.run_id,model_name=input.model_name)
        
        standard_model_type_click_dict[input.model_type] = {'pos_click' : 7, 'total_view' : 25}
        state = "Model-Update"
    
    return {'state' : state}


@app.post('/models', response_model=Output, tags=['models'], description="추천 결과 반환")
async def main(input: Input) -> Output:
    problems = 'Not-Found-Key'
    tag = 'Not-Found-Key'

    if input.key == 123456:
        problems = 'Not-Found-User'
        tag = 'Not-Found-User'

        crawlings = [total_solved_problem_seq_crawling(input.username), lately_solved_problem_seq_crawling(input.username)]
        total_solved_problem_seq, lately_solved_problem_seq = await asyncio.gather(*crawlings)

        if not isinstance(total_solved_problem_seq, str):
            problems = 'Not-Found-User-Solved-Problem'
            tag = 'Not-Found-User-Solved-Problem'

            if total_solved_problem_seq:
                problems = 'Not-Found-User-Lately-Solved-Problem'
                tag = 'Not-Found-User-Lately-Solved-Problem'

                preprocessings = [problem_seq2idx(total_solved_problem_seq), problem_seq2idx(lately_solved_problem_seq)]
                total_solved_problem_seq, lately_solved_problem_seq = await asyncio.gather(*preprocessings)

                if lately_solved_problem_seq:
                    tag = serch_best_tag(lately_solved_problem_seq)

                    model_type_click_dict = input.model_type_click if input.model_type_click else standard_model_type_click_dict

                    model_types = list(model_type_click_dict.keys())
                    inferences = [inference(models[model_type], lately_solved_problem_seq, total_solved_problem_seq) for model_type in model_types]
                    inferences = await asyncio.gather(*inferences)
                    model_type_to_output = {model_type:deque(output) for model_type, output in zip(model_types, inferences)}

                    problems = []
                    while len(problems) < 10:
                        model_type = thompson_sampling(model_types, model_type_click_dict)
                        
                        output = model_type_to_output[model_type]
                        output = output.popleft()

                        problems.append(
                                {
                                    'model_type' : model_type,
                                    'output' : output
                                }
                            )
                        
                        for model_type in model_types:
                            if not model_type_to_output[model_type]:
                                del model_type_click_dict[model_type]
                            else:
                                if output in model_type_to_output[model_type]:
                                    model_type_to_output[model_type].remove(output)
    
    datas = {    
            'problems' : problems,
            'tag' : tag,
        }

    try:
        Output(**datas)
    
    except:
        datas = {    
            'problems' : [{'model_type': problems, 'output': problems}],
            'tag' : [tag],
        }
    
    return datas


if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=30002, reload=True)


