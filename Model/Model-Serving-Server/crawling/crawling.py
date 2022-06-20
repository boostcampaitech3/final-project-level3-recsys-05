import httpx
from bs4 import BeautifulSoup

headers = {'User-Agent': "Mediapartners-Google"}

async def lately_solved_problem_seq_crawling(username : str) -> list:
    url = f'https://www.acmicpc.net/status?problem_id=&user_id={username}&language_id=-1&result_id=4'
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    user_seq = [problem.text for problem in soup.select('td:nth-child(3) > a')]
    
    if user_seq:
        # 중복 seq 제거
        user_seq = sorted(set(user_seq), key = lambda x: user_seq.index(x))

    # 빈 리스드면 최근 문제가 존재하지 않는 유저
    return user_seq

async def total_solved_problem_seq_crawling(username : str) -> list:
    url = f'https://www.acmicpc.net/user/{username}'

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    
    if response.status_code == 404: user_seq = 'Not-Found-User'
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        user_seq = soup.find('div', {'class':'problem-list'}).text.split()

    # 빈 리스드면 지금 까지 맞은 문제가 존재하지 않는 유저
    return user_seq