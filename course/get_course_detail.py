import pandas as pd
import time , os, requests
import yaml
import warnings
warnings.filterwarnings(action='ignore')

from utils import dotdict
from bs4 import BeautifulSoup as bs


def get_course_detail(total_course):
    init_url = "https://www.acmicpc.net/workbook/view/"

    data_all_df = pd.DataFrame({}, columns=['course_id', 'problem_id', 'title', 'correct_count', 
                                            'submmission_count', 'correct_ratio', 'detail'])

    for num in range(len(total_course)):  
        page = total_course['course_id'][num]

        url = init_url+str(page)
        req = requests.get(url, headers=args.headers).text
        page_source = bs(req, "html.parser")

        detail = page_source.find('div', {'class':'page-header'}).text
        content_box = page_source.find_all('tr')[1:]

        ## -- get content
        for content in content_box:
            problem_id = content.find('td').text
            title = content.find_all('a')[0].text
            try:
                correct_count = content.find_all('a')[1].text
                submmission_count = content.find_all('a')[2].text
            except:
                correct_count = '-'
                submmission_count = '-'
            correct_ratio = content.find_all('td')[-1].text
            course_id = page
            flash_data = [course_id, problem_id, title, correct_count, submmission_count, correct_ratio, detail]

            data_all_df = data_all_df.append(pd.Series(flash_data, index=data_all_df.columns), ignore_index=True)
        
        # time.sleep()
        print(f"{page}'s course extract complete!")
        if num % 500 == 0:
            print(num)
            time.sleep(10)
    return data_all_df


if __name__ == '__main__':
    # -- args setting -- 
    args = None
    with open("get_course.yaml") as f:
        tmp_args = yaml.load(f, Loader=yaml.FullLoader)
        args = dotdict(tmp_args)
    print(args)
    
    total_course = pd.read_csv(os.path.join(args.data_path, 'course_data_list.csv'))
    course_detail = get_course_detail(total_course)
    course_detail.to_csv(os.path.join(args.data_path, 'course_detail.csv'), index=False)
    print('Done!')