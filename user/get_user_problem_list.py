import pandas as pd
import time, os, requests
import yaml
import warnings
warnings.filterwarnings(action='ignore')

from utils import dotdict
from bs4 import BeautifulSoup as bs


def get_user_problems(user_data, args):    
    for num in range(args.start, args.end+1):
        user_name = user_data['user_name'][num]

        url = args.init_url+str(user_name)
        req = requests.get(url, headers=args.headers).text
        page_source = bs(req, "html.parser")
        try:
            ## -- get problems
            problems = page_source.find('div', {'class':'problem-list'}).text.split()
            problems_count = int(page_source.find('span', {'id':'u-solved'}).text)
            print(f"{num}'s user extract complete!")
        except:
            print(f"{num}'s user error!")
            problems = []
            problems_count = 0            

        user_data['problems'][num] = problems
        user_data['problems_count'][num] = problems_count

        
        if num % 500 == 0:
            time.sleep(10)
    return user_data

if __name__ == '__main__':
    # -- args setting -- 
    args = None
    with open("get_user_problem_list.yaml") as f:
        tmp_args = yaml.load(f, Loader=yaml.FullLoader)
        args = dotdict(tmp_args)
    print(args)

    user_data = pd.read_csv(os.path.join(args.data_path, 'user.csv'))

    if 'problems' not in user_data.columns:
        user_data['problems'] = '-'
        user_data['problems_count'] = '-'
        user_data.rename(columns={'handle':'user_name'}, inplace=True)
    print(user_data.head)
    user_data_update = get_user_problems(user_data, args)
    user_data_update.to_csv(os.path.join(args.data_path, 'user_update.csv'), index=False)