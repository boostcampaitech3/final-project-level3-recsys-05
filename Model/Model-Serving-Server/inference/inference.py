from git import Object
import numpy as np
from scipy.stats import beta
from preprocessing.preprocessing import output2problem_id


def output_fitering(output:np.array, fiterling_list:list) -> np.array:
    output[fiterling_list] = -np.Inf
    return output


def output_sorted(output:np.array, top:int = 10)-> np.array:
    output = output.argsort()[::-1][:top]
    return output


async def inference(model:Object, problem_seq:list, fiterling_list:list) -> list:
    output = model.predict(problem_seq)
    output = output_fitering(output, fiterling_list)
    output = output_sorted(output)
    output = output2problem_id(output)
    return output


def thompson_sampling(model_types:list, model_type_click_dict:dict) -> str:
    '''
    model_type = ['model_type']

    model_type_click_dict = {
            'model_type' : {'pos_click' : 1, 'total_view' : 1},
    }
    '''

    sampling_list = [beta.rvs(max(model_type_click_dict[model_type]['pos_click'], 1), max(model_type_click_dict[model_type]['total_view'], 1)) for model_type in model_types]
    idx = np.argmax(sampling_list)
    return model_types[idx]