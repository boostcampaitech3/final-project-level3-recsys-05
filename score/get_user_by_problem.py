import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import yaml
import time
from tqdm import tqdm

def _get_problem_list(path):
    problem_list = set(pd.read_csv(path)['problem_num'])
    return problem_list

def _get_timestamp(table):
    timestamp = []
    for data in table[0].find_all("a", class_="real-time-update"):
        timestamp.append(data.attrs['data-timestamp'])
    return timestamp

def _processing(df):
    df.rename(columns={
            "제출 번호": "scoreId",
            "아이디": "username",
            "문제": "problemId",
            "결과": "answer",
            "메모리": "memory",
            "시간": "time",
            "코드 길이": "length",
            "언어": "language",
            "제출한 시간": "date"
        }, inplace=True)
    return df


def get_user_by_problem(start, end, headers, file_name, problem_file) -> None:
    save_path = os.path.join(os.getcwd(), file_name)
    problem_list = _get_problem_list(problem_file)
    problem_range = set(i for i in range(start, end+1))
    problem_list = problem_list.intersection(problem_range)

    with tqdm(total=len(problem_list), leave=True) as pbar:
        for problem in tqdm(problem_list):
            try:
                url = f"https://www.acmicpc.net/status?problem_id={problem}&result_id=4"
                req = requests.get(url, headers=headers).text
                soup = BeautifulSoup(req, "html.parser")
                table = soup.select('table')
                timestamp = _get_timestamp(table)
                df_table = pd.read_html(str(table))[0]
                df_table['제출한 시간'] = timestamp
                df_score = pd.concat([df_score, df_table])
                pbar.update(1)
            except:
                df_score = _processing(df_score)
                df_score.to_json(save_path, orient='records', lines=True)
                print("Error! Temporary Json file save!")
    df_score = _processing(df_score)
    df_score.to_json(save_path, orient='records', lines=True)
    print("Json file save!")

def main():
    start = time.time()
    with open("get_users_by_problem.yaml") as f:
        params = yaml.load(f, Loader=yaml.FullLoader)
    get_user_by_problem(params['start'], params['end'], params['headers'], params['save_path'], params['problem_path'])
    end = time.time()
    print(end - start)

if __name__ == "__main__":
    main()