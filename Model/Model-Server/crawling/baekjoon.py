import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': "Mediapartners-Google"}

def lately_solved_problem_seq_collection(user_id):
    url = f'https://www.acmicpc.net/status?problem_id=&user_id={user_id}&language_id=-1&result_id=4'
    response = requests.request("GET", url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    user_seq = [problem.text for problem in soup.select('td:nth-child(3) > a')]
    if not user_seq:
        user_seq = []
    else:
        # 중복 seq 제거
        user_seq = sorted(set(user_seq), key = lambda x: user_seq.index(x))

    # 빈 리스드면 최근 문제가 존재하지 않는 유저
    return user_seq

def total_solved_problem_seq_collection(user_id):
    url = f'https://www.acmicpc.net/user/{user_id}'
    response = requests.request("GET", url, headers=headers)

    if response.status_code == 404:
        user_seq = 'Not-Found-User'
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        user_seq = [problem.text for problem in soup.select('body > div.wrapper > div.container.content > div.row > div:nth-child(2) > div > div.col-md-9 > div:nth-child(2) > div.panel-body > div > a')]

    # 빈 리스드면 지금 까지 맞은 문제가 존재하지 않는 유저 or 아이디가 존재하지 않는 유저
    return user_seq