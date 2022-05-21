import pandas as pd
import time, os, requests
import yaml
import warnings
warnings.filterwarnings(action='ignore')

from utils import dotdict
from bs4 import BeautifulSoup as bs


def get_page_source(problem_id, args):
    url = args.init_url+str(problem_id)
    
    currentpage = requests.get(url, headers=args.headers).text
    page_source = bs(currentpage, "html.parser")

    return page_source


def get_problem_meta_data(page_source):
    ### get_data ###
    # -- title --
    title = page_source.find('title').text

    # -- problem_info --
    problem_info_all = page_source.find_all('td')
    problem_info = [info.text for info in problem_info_all]

    # -- problem_description --
    problem_description = page_source.find('div', {'class':'problem-text', 'id':'problem_description'}).text
    try:
        problem_input = page_source.find('div', {'class':'problem-text', 'id':'problem_input'}).text
    except:
        problem_input = '-'
    try:
        problem_output = page_source.find('div', {'class':'problem-text', 'id':'problem_output'}).text
    except:
        problem_output = '-'
    try:
        problem_hint = page_source.find('div', {'class':'problem-text', 'id':'problem_hint'}).text
    except:
        problem_hint = '-'
    try:
        problem_limit = page_source.find('div', {'class':'problem-text', 'id':'problem_limit'}).text
    except:
        problem_limit = '-'

    # -- sample_list --
    sample_num = 1
    sample_list = []
    while True:
        try:
            sample_in = page_source.find('pre', {'id':'sample-input-{}'.format(sample_num)}).text
            sample_out = page_source.find('pre', {'id':'sample-output-{}'.format(sample_num)}).text
            sample_list.append([sample_in, sample_out])
            sample_num += 1
        except:
            break

    # -- problem_association --
    try:
        problem_list_temp = page_source.find('section', {'id':'problem_association'}).find_all('li')
        problem_association = [problem.text for problem in problem_list_temp]
    except:
        problem_association = []
        
    flash_data = [title, problem_info, problem_description, problem_input, problem_output,
                problem_hint, problem_limit, sample_list, problem_association, problem_id]
    
    return flash_data

def write_error_problem(error_problem, args):
    print('Problem {} does not exist.'.format(error_problem))

    file = os.path.join(args.data_path, args.error_file)    
    f = open(file, 'a')
    problems = ', '.join(map(str, error_problem))
    f.write(problems)
    f.close()


if __name__ == '__main__':
    # -- args setting -- 
    args = None
    with open("get_problem.yaml") as f:
        tmp_args = yaml.load(f, Loader=yaml.FullLoader)
        args = dotdict(tmp_args)
    print(args)
    
    # -- 데이터를 저장할 Data Frame --
    data_all_df = pd.DataFrame({}, columns=['title', 'problem_info', 'problem_description',
                                        'problem_input', 'problem_output', 'problem_hint',
                                        'problem_limit', 'sample_list', 
                                        'problem_association', 'problem_id'])
    error_problem = []


    # -- data scraping --        
    for problem_id in range(args.start, args.end+1):
        try:
            page_source = get_page_source(problem_id, args) 

            try:  
                flash_data = get_problem_meta_data(page_source)            
                data_all_df = data_all_df.append(pd.Series(flash_data, index=data_all_df.columns), ignore_index=True)

            except:
                error_problem.append(problem_id)
                continue
            
            # time sleep 
            if problem_id % 100 == 0:
                print('now {}'.format(problem_id))
                time.sleep(10)
            
            if problem_id % 1000 == 0:
                time.sleep(20)
                
        except:
            print('scraping error. end point is {}'.format(problem_id))
            data_all_df.to_csv(args.data_path+'/{}_{}_to_{}.csv'.format(args.file_name, args.start, problem_id), encoding='utf-8', index=False)
            write_error_problem(error_problem, args)
            
    print('scraping is done')
    data_all_df.to_csv(args.data_path+'/{}_{}_to_{}.csv'.format(args.file_name, args.start, problem_id), encoding='utf-8', index=False)
    write_error_problem(error_problem, args)

