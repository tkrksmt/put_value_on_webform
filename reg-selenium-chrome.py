import time
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import csv
import re
import random
import datetime

def get_csv_data(file_name):
    r = pd.read_csv(file_name , sep=',')
    # change '' string  nan 
    r = r.fillna('')
    return r

def get_url(isBasic, id , pw , url):
    data = id + ':' + pw + '@' if isBasic else ''    
    url = re.split('https://', url)
    url = 'https://' + data + url[1]
    #print(url)
    return url

def get_form_name_list(file_name):
    r = pd.read_csv(file_name , sep=',',)
    return r

def get_radio_button(type, result1 , result2, data):
    #gender or AB test
    r = result1
    if (type == 'gender' and data ！= '男') or data == '希望しない':
        r = result2
    return r

def get_select_index(type, data):
    r = -1
    if type == 'job':
        r = get_job_index(data)
    elif type == 'job-category':
        r = get_job_category_index(data)
    elif type == 'job-department':
        r = get_job_department_index(data)
    elif type == 'job-pref-address':
        r = get_pref_index(data)
    return r
    
def get_job_index(data):
    l = ['' , 'A' ,'B' ,'C' ,'D' ,'E']
    return get_list_index(l , data)

def get_job_category_index(data):
    l = ['' , 'A' ,'B' ,'C' ,'D']
    return get_list_index(l , data)

def get_job_department_index(data):
    l = ['' , 'A' ,'B' ,'C']
    return get_list_index(l , data) 

def get_pref_index(data):
    l = ['' , '北海道' , '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県',
    '群馬県' ,'埼玉県' ,'千葉県' ,'東京都' ,'神奈川県' ,'新潟県' ,'富山県' ,'石川県' ,'福井県' ,'山梨県',
    '長野県' ,'岐阜県' ,'静岡県' ,'愛知県' ,'三重県' ,'滋賀県' ,'京都府' ,'大阪府' ,'兵庫県' ,'奈良県',
    '和歌山県' ,'鳥取県' ,'島根県' ,'岡山県' ,'広島県' ,'山口県' ,'徳島県' ,'香川県' ,'愛媛県' ,'高知県',
    '福岡県' ,'佐賀県' ,'長崎県' ,'熊本県' ,'大分県' ,'宮崎県' ,'鹿児島県' ,'沖縄県']
    return get_list_index(l , data)

def get_list_index(l , data):
    r = -1
    for i, ar in enumerate(l):
        if ar == data:
            r = i
            break
    return r

def main():
    url = get_url(True , 'basic-id', 'basic-pw' , 'https://localhost:8080')
    user_data = get_csv_data('user_data.csv')
    form_data = get_form_name_list('web_form_list.csv')

    for data in user_data.values:
        #Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        #driver = webdriver.Chrome()

        '''
        # case : firefox
        ###
        # from selenium.webdriver.firefox.options import Options
        ###
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        '''
        
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.ID, 'submit')))

        submit_id = None
        
        for i , tag_name in enumerate(form_data.values , 0):
            #[0]:discription , [1]:type , [2]:input tagName, [3],RadioButton TagName
            
            if tag_name[1] == 'checbox':
                ck = driver.find_element_by_id(tag_name[2])
                ck.click()
            elif tag_name[1] == 'radio_button':
                d = get_radio_button(tag_name[1], tag_name[2] , tag_name[3] , data[i])
                driver.find_element_by_id(d).click()
            elif tag_name[1] == 'select':
                select_list = driver.find_element_by_name(tag_name[2])
                select = Select(select_list)

                d = get_select_index(tag_name[0] , data[i])
                select.select_by_index(d)           
            elif tag_name[1] == 'text':
                send_box = driver.find_element_by_name(tag_name[2])
                send_box.send_keys(data[i])
            
            # search submit tag
            if submit_id is None:
                submit_id = driver.find_element_by_name(tag_name[2])
        
        
        submit_id.submit()
        now = datetime.datetime.now()
        print(now)
        time.sleep(2)

        # next dispaly
        driver.find_element_by_name('XXXX').submit()
        driver.quit()

main()
