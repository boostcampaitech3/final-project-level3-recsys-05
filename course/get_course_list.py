import pandas as pd
import time, os, requests
import yaml
import warnings
warnings.filterwarnings(action='ignore')

from bs4 import BeautifulSoup as bs
from utils import dotdict


def get_course(start, end):
    data_all_df = pd.DataFrame({}, columns=['course_id', 'author', 'course_name'])
    init_url = "https://www.acmicpc.net/workbook/top/"

    for page in range(start, end+1):  # 1~47 page
        url = init_url+str(page)

        ## -- page parsing
        currentpage = requests.get(url, headers=args.headers).text
        page_source = bs(currentpage, "html.parser")
        content_box = page_source.find_all('tr')[1:]

        ## -- get content
        for content in content_box:
            course_id = content.find('td').text
            author = content.find_all('a')[0].text
            course_name = content.find_all('a')[1].text
            flash_data = [course_id, author, course_name]

            data_all_df = data_all_df.append(pd.Series(flash_data, index=data_all_df.columns), ignore_index=True)
    
    return data_all_df


def get_codeplus_course(start, end):
    data_all_df = pd.DataFrame({}, columns=['course_id', 'author', 'course_name', 'course_name_main'])
    init_url = "https://www.acmicpc.net/workbook/codeplus/"

    for page in range(start, end+1):  # 1~3 page
        url = init_url+str(page)

        ## -- page parsing
        currentpage = requests.get(url, headers=args.headers).text
        page_source = bs(currentpage, "html.parser")
        content_box = page_source.find_all('tr')[1:]

        ## -- get content
        for content in content_box:
            course_id = content.find('td').text
            course_name_main = content.find_all('a')[0].text
            course_name = content.find_all('a')[1].text
            author = 'codeplus'
            flash_data = [course_id, author, course_name, course_name_main]

            data_all_df = data_all_df.append(pd.Series(flash_data, index=data_all_df.columns), ignore_index=True)
        
    return data_all_df


if __name__ == '__main__':
    # -- args setting -- 
    args = None
    with open("get_course.yaml") as f:
        tmp_args = yaml.load(f, Loader=yaml.FullLoader)
        args = dotdict(tmp_args)
    print(args)

    course = get_course(args.start, args.end)
    print('course data extraction success!')
    course_codeplus = get_codeplus_course(args.codeplus_start, args.codeplus_end)
    print('codeplus course data extraction success!')

    course['course_name_main'] = '-'

    total_course = pd.concat([course, course_codeplus])
    total_course.to_csv(os.path.join(args.data_path, 'course_data_list.csv'), index=False)
    print('Done!')