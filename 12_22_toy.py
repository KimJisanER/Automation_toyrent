import pandas as pd
import numpy as np

data=pd.read_csv('toy_raw.csv',sep=',', encoding='cp949')

data=data.iloc[:,3:5]
data['대여상태']=data['대여상태'].replace('보유중',1)
data['대여상태']=data['대여상태'].replace('대여중',0)
print(data)
data_sum=data.groupby(['상품명']).sum()
data_sum=data_sum.reset_index()
print(data_sum)

c=[]
for i in range(len(data_sum)):
    if data_sum['대여상태'][i]==0:
        c.append(data_sum['상품명'][i])

print(c)
c=pd.DataFrame(c)
print(c)

c.to_csv('toy_out.csv')

