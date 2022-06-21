import os
import time
import ndjson
import requests
from fake_useragent import UserAgent

def get_user() -> None:
    url = "https://solved.ac/api/v3/ranking/tier"
    ua = UserAgent()
    file_path = os.path.join(os.getcwd(), "user.json")
    user_info_list = []
    count = requests.get(url).json()['count']
    headers = {"User-agent": ua.random}

    try:
        for page in range(1, count//100+2):
            if page % 100 == 0:
                headers = {"User-agent": ua.random}
                time.sleep(1000)
            params = {"page": page}
            res = requests.get(url, headers=headers, params=params)
            user_info_list.extend(res.json()['items'])

        with open(file_path, 'w', encoding='utf-8') as file:
            ndjson.dump(user_info_list, file)
    except:
        with open(file_path, 'w', encoding='utf-8') as file:
            ndjson.dump(user_info_list, file)

def main():
    get_user()

if __name__ == "__main__":
    main()