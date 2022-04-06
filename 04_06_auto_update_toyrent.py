import os
import pandas as pd
import numpy as np
from tkinter import filedialog
from tkinter import messagebox

#file 변수에 선택 파일 경로 넣기
file1 = filedialog.askopenfilenames(initialdir="/",\
                 title = "이전 파일을 선택 해 주세요",\
                    filetypes = (("*.csv","*csv"),("*.xlsx","*xlsx"),("*.xls","*xls")))
file2 = filedialog.askopenfilenames(initialdir="/",\
                 title = "최근 파일을 선택 해 주세요",\
                    filetypes = (("*.csv","*csv"),("*.xlsx","*xlsx"),("*.xls","*xls")))

#파일 선택 안했을 때 메세지 출력

if file1 == '':
    messagebox.showwarning("경고", "파일을 추가 하세요")
if file2 == '':
    messagebox.showwarning("경고", "파일을 추가 하세요")

print(file1)    #files 리스트 값 출력

#dir_path에 파일경로 넣어서 읽기
for dir_path in file1:
    prior = pd.read_csv(dir_path ,sep=',', encoding='cp949')
for dir_path in file2:
    later = pd.read_csv(dir_path ,sep=',', encoding='cp949')

print(len(prior))
print(len(later))

## 폐기, 기증, 판매 등 메모 항목으로 현재 없는 장난감 걸러내는 함수
def out(x):
    for i in range(len(x['메모'])):
      if x['메모'].find('폐기') != -1 :
        x['out'] = 1
      elif x['메모'].find('폐') != -1 :
        x['out'] = 1
      elif x['메모'].find('기증') != -1 :
        x['out'] = 1
      elif x['메모'].find('송천') != -1 :
        x['out'] = 1
      elif x['메모'].find('인후') != -1 :
        x['out'] = 1
      elif x['메모'].find('판매') != -1 :
        x['out'] = 1
      else:
        x['out'] = 0
    return x

## 함수 적용
prior = prior.apply(lambda x: out(x), axis=1)
later = later.apply(lambda x: out(x), axis=1)
prior=prior[prior['out']==0]
later=later[later['out']==0]
print(len(prior))
print(len(later))

#보유==0인 장난감 리스트 정리해주는 함수
def toylist(data):
  data=data.iloc[:,3:6]
  data['대여상태']=data['대여상태'].replace('보유중',1)
  data['대여상태']=data['대여상태'].replace('대여중',0)
  data_sum=data.groupby(['상품명']).sum()
  data_sum=data_sum.reset_index()
  c=[]
  for i in range(len(data_sum)):
    if data_sum['대여상태'][i]==0:
        c.append(data_sum['상품명'][i])
  return(c)

#리스트 비교
out_update=list(set(toylist(later))-set(toylist(prior)))
in_update=list(set(toylist(prior))-set(toylist(later)))

#출력
print()
print('대여중으로 바꿀 장난감:\n',out_update,'\n')
print('보유중(대여가능)으로 바꿀 장난감:\n',in_update,'\n')



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.chrome.service import Service

# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
#
# s = Service('./chromedriver')
#
# driver = webdriver.Chrome(service=s)

driver = webdriver.Chrome('./chromedriver')

try:

    # 로그인
    driver.get("http://jbyuseong.ivyro.net/2019/bbs/login.php")
    time.sleep(2)
    elem = driver.find_element_by_name('mb_id')
    elem.send_keys('admin')
    elem = driver.find_element_by_name('mb_password')
    elem.send_keys('123456')
    elem.send_keys(Keys.RETURN)

    time.sleep(2)

#장난감 목록들어가기
    driver.get("http://jbyuseong.ivyro.net/2019/bbs/content.php?co_id=toy_1")
    driver.get("http://jbyuseong.ivyro.net/2019/bbs/board.php?bo_table=toy_6&vtoy=1")

#대여중으로 바꿀 품목 처리
    for i in range(len(out_update)):
        # 검색
        elem = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[2]/fieldset/form/input[4]')
        ac = ActionChains(driver)
        ac.move_to_element(elem)
        ac.click()

        ac.send_keys(out_update[i])
        # elem.submit()
        ac.perform()
        elem.send_keys(Keys.RETURN)

        time.sleep(2)
        try:
            # 첫번째 항목 누르기
            driver.find_elements_by_css_selector(
                '#gall_ul > li > div > div.gall_con > div.gall_text_href > a.bo_tit > b')[0].click()
            # 수정 누르기
            driver.find_elements_by_css_selector('#bo_v_top > ul.bo_v_left > li:nth-child(1) > a')[0].click()
            # 대여 여부 수정하기

            select = Select(driver.find_element_by_css_selector('#autosave_wrapper\ write_div > select'))
            # select box에서 index 1 이 대여
            select.select_by_index(1)
            # 작성완료
            driver.find_elements_by_css_selector('#btn_submit')[0].click()
            # 목록으로 복귀
            driver.find_elements_by_css_selector('#bo_v_top > ul.bo_v_com > li:nth-child(1) > a')[0].click()

        except Exception as e:
            print('오류 품목: ',out_update[i])
            print(e)
            driver.get("/2019/bbs/board.php?bo_table=toy_6&amp;vtoy=1")
    print('대여중 업데이트 완료')

# 대여가능으로 바꿀 품목 처리

    for i in range(len(in_update)):
        # 검색
        elem = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[2]/fieldset/form/input[4]')
        ac = ActionChains(driver)
        ac.move_to_element(elem)
        ac.click()

        ac.send_keys(in_update[i])
        # elem.submit()
        ac.perform()
        elem.send_keys(Keys.RETURN)

        time.sleep(2)
        try:
            # 첫번째 항목 누르기
            driver.find_elements_by_css_selector(
                '#gall_ul > li > div > div.gall_con > div.gall_text_href > a.bo_tit > b')[
                0].click()
            # 수정 누르기
            driver.find_elements_by_css_selector('#bo_v_top > ul.bo_v_left > li:nth-child(1) > a')[0].click()
            # 대여 여부 수정하기

            select = Select(driver.find_element_by_css_selector('#autosave_wrapper\ write_div > select'))
            # select box에서 index 0 이 대여가능
            select.select_by_index(0)
            # 작성완료
            driver.find_elements_by_css_selector('#btn_submit')[0].click()
            # 목록으로 복귀
            driver.find_elements_by_css_selector('#bo_v_top > ul.bo_v_com > li:nth-child(1) > a')[0].click()

        except Exception as e:
            print('오류 품목: ',in_update[i])
            print(e)
            driver.get("/2019/bbs/board.php?bo_table=toy_6&amp;vtoy=1")
    print('대여가능 업데이트 완료')
#
except Exception as e:
    print('오류발생')
    print(e)