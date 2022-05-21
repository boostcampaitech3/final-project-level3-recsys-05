import requests, time, json, os
import pandas as pd
import yaml
import warnings
warnings.filterwarnings(action='ignore')

from utils import dotdict

def get_data(problem_ids, total_data):
    url = "https://solved.ac/api/v3/problem/lookup"
    querystring = {"problemIds":problem_ids}
    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)

    flash_data = json.loads(response.text)
    total_data = total_data+flash_data
    return total_data

    
def get_problem_api_data(total_data):
    all_data_df = pd.DataFrame({}, columns = ['problem_id', 'is_solvable', 'is_partial', 
                                              'accepted_user_count', 'level', 'average_tries', 'problem_tags'])
    for problem in total_data:
        problem_id = problem['problemId']
        is_solvable = problem['isSolvable']
        is_partial = problem['isPartial']
        accepted_user_count = problem['acceptedUserCount']
        level = problem['level']
        average_tries = problem['averageTries']
        problem_tags = problem['tags']
        
        flash_data = [problem_id, is_solvable, is_partial, accepted_user_count, level, average_tries, problem_tags]
        all_data_df = all_data_df.append(pd.Series(flash_data, index=all_data_df.columns), ignore_index=True)
    return all_data_df
    

if __name__ == '__main__':
    try:
        # -- args setting -- 
        args = None
        with open("get_problem.yaml") as f:
            tmp_args = yaml.load(f, Loader=yaml.FullLoader)
            args = dotdict(tmp_args)
        print(args)

        total_data = []
        for i in range(args.start, args.end+1, 100):
            problem_list = [str(num) for num in range(i, i+100)]
        problem_ids = ','.join(problem_list)
        total_data = get_data(problem_ids, total_data)
        
        problems_df = get_problem_api_data(total_data)
        problems_df.to_csv(os.path.join(args.data_path, 'problem_api_data.csv'), index=False)
        print('Data extraction success!')
    except:
        print('Error!')