import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import yaml
import time
from tqdm import tqdm

"""
1. 3개의 파일을 같은 폴더에 넣어주세요.
2. yaml파일에 적절한 파라미터를 넣어주세요.
3. python get_score.py 명령어 실행해주세요.
"""

def _get_users_by_problem(path):
    df = pd.read_csv(path)
    return df

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


def get_problem_list(start, end, headers, file_name) -> None:
    save_path = os.path.join(os.getcwd(), file_name)
    df_path = os.path.join(os.getcwd(), "users_by_problem.csv")

    df = _get_users_by_problem(df_path)
    problemId_filter = (df.index >= start) & (df.index <= end)
    cols = df.loc[problemId_filter, ['scoreId', 'User_userId', 'Problem_problemId']]

    df_score = pd.DataFrame()


    with tqdm(total=len(cols), leave=True) as pbar:
        for _, col in tqdm(cols.iterrows()):
            solved_id, user, problem_id = col
            try:
                url = f"https://www.acmicpc.net/status?user_id={user}&result_id=4&top={solved_id}"
                req = requests.get(url, headers=headers).text
                soup = BeautifulSoup(req, "html.parser")
                table = soup.select('table')
                timestamp = _get_timestamp(table)
                df_table = pd.read_html(str(table))[0]
                df_table['제출한 시간'] = timestamp
                df_table['target'] = problem_id
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
    with open("get_score.yaml") as f:
        params = yaml.load(f, Loader=yaml.FullLoader)
    get_problem_list(params['start'], params['end'], params['headers'], params['file_name'])
    end = time.time() - start
    print(end)

if __name__ == "__main__":
    main()