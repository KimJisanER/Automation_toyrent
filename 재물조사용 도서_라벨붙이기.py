
##사용방법

# 1. run 누르기
# 2. 파일 넣어주기 대여현황('조이렌트 장난감/도서' 폴더에 있는 Exp221024_170332.csv 이런 식으로 된 홈페이지업데이트에 쓰는 것과 동일한 파일, 가장최근 것)
# 3. 파일 넣어주기('조이렌트 장난감/재물조사_도서' 폴더에 있는 도서라벨.csv)
# 4. '조이렌트 장난감/재물조사_도서' 폴더에서 대여현황_도서라벨.csv 확인하기
# 5. 프린트는 열에 맞춰서 해주기

import os
import pandas as pd
import numpy as np
from tkinter import filedialog
from tkinter import messagebox
import re


#files 변수에 선택 파일 경로 넣기
file1 = filedialog.askopenfilenames(initialdir="/",\
                 title = "도서대여현황을 선택 해 주세요",\
                    filetypes = (("*.csv","*csv"),("*.xlsx","*xlsx"),("*.xls","*xls")))
file2 = filedialog.askopenfilenames(initialdir="/",\
                 title = "도서라벨을 선택 해 주세요",\
                    filetypes = (("*.csv","*csv"),("*.xlsx","*xlsx"),("*.xls","*xls")))

#파일 선택 안했을 때 메세지 출력

if file1 == '':
    messagebox.showwarning("경고", "파일을 추가 하세요")
if file2 == '':
    messagebox.showwarning("경고", "파일을 추가 하세요")

print(file1)    #files 리스트 값 출력

#dir_path에 파일경로 하나씩 넣어서 읽기
for dir_path in file1:
    rent = pd.read_csv(dir_path ,sep=',', encoding='cp949')
for dir_path in file2:
    label = pd.read_csv(dir_path ,sep=',', encoding='cp949')

rent=rent[['바코드','상품명','장르','대여상태']]
# rent=rent[rent['대여상태']=='보유중']
label=label[['바코드','라벨번호']]

# print(rent.head())
# print(label.head())

rent_label = pd.merge(rent, label, left_on='바코드', right_on='바코드', how='left')

rent_label['라벨번호_str'] = rent_label['라벨번호'].str.extract(r'(\D+)')
rent_label['라벨번호_int'] = rent_label['라벨번호'].str.extract(r'(\d+)')
rent_label['라벨번호_int'] = pd.to_numeric(rent_label['라벨번호_int'])

rent_label=rent_label.sort_values(by=['라벨번호_str','라벨번호_int'])
rent_label=rent_label.drop(columns=['라벨번호_str','라벨번호_int'])

rent_label.to_csv('C:/Users/User/Desktop/조이렌트 장난감/재물조사_도서/대여현황_도서라벨.csv',index=False,encoding='euc-kr')
print('저장완료:대여현황_도서라벨.csv 확인')