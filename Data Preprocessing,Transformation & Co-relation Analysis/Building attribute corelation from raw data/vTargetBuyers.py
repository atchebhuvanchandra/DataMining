from math import*
import math
import pandas as pd
from pandas import DataFrame
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt 
from scipy.stats import norm

file_handler = open("vTargetBuyers.csv","r")


dataset = pd.read_csv(file_handler,sep = ",")

file_handler.close()

dataset.set_index('CustomerKey',inplace = True)
print(dataset.isnull().sum())

'''Converting Gender to binary values replacing Male attribute by 1 and Female by 0 '''
dataset.Gender.loc[dataset.Gender == 'M'] = 1
dataset.Gender.loc[dataset.Gender == 'F'] = 0
'''Converting Marital Status to binary values replacing Married attribute by 1 and Single by 0 '''
dataset.MaritalStatus.loc[dataset.MaritalStatus == 'M'] = 1
dataset.MaritalStatus.loc[dataset.MaritalStatus == 'S'] = 0

''' Age and Salary columns need to be normalized using the '''
scaler = MinMaxScaler()

dataset [['YearlyIncome','Age']] = scaler.fit_transform(dataset[['YearlyIncome','Age']])
df_normalized = pd.DataFrame(dataset)
'''Giving Commute distance ranks based on the distance they travel

 0-1 Miles as 1
 1-2 Miles as 2
 2-5 Miles as 3
 5-10 Miles as 4
 10+ Miles as 5

 1,2.. 5 are in ascending order '''

dataset.CommuteDistance.loc[dataset.CommuteDistance == '0-1 Miles'] = 1
dataset.CommuteDistance.loc[dataset.CommuteDistance == '1-2 Miles'] = 2
dataset.CommuteDistance.loc[dataset.CommuteDistance == '2-5 Miles'] = 3
dataset.CommuteDistance.loc[dataset.CommuteDistance == '5-10 Miles'] = 4
dataset.CommuteDistance.loc[dataset.CommuteDistance == '10+ Miles'] = 5

''' One hot encoding of region data  '''
dataset = pd.concat([dataset,pd.get_dummies(dataset['Region'], prefix = 'country')],axis =1)
dataset.drop(['Region'],axis = 1, inplace = True)

'''Transfoming TotalChildren ,NumberCarsOwned, CommuteDistance'''
dataset[['TotalChildren','NumberChildrenAtHome','NumberCarsOwned','CommuteDistance']]=scaler.fit_transform(dataset[['TotalChildren','NumberChildrenAtHome','NumberCarsOwned','CommuteDistance']])


export_csv = dataset.to_csv(r'C:\Users\BHUVAN\Desktop\study zone\DataMinig\Lab 1\export_dataframe.csv',index = None ,header = True)

customerkey1=input('enter first customerkey to find out Simple Matching , Extended Jackard Similarity and Cosine Similarity')
customerkey2 = input('enter second customerkey to find out Simple Matching , Extended Jackard Similarity and Cosine Similarity')

''' Result for Sample matching'''
sm1 = dataset.loc[int(customerkey1)]
sm2 = dataset.loc[int(customerkey2)]
print(sm1[1])
res= sm1 == sm2
count = 0
i =0
print(res)
for i in range(0,8):
    if res[i] == True:
     count =count+1

if (res[9] == True | res[10] == True | res[11] == True):
        count = count + 1

print('Simple Matching Coefficient',count/10)

'''Result for Jaccard Similarity'''
intersection =0
union =0
for i in range(0,8):
    if res[i] == True:
        intersection = intersection + 1
        union = union + 1
    elif res[i]== False:
        union = union +1

if (res[9] == True|res[10] == True |res[11] == True):
        intersection = intersection +1
        union = union +1
    
print('Jaccard Similarity',(intersection/union))


'''Result of Cosine Similarity '''
dot_product = 0.0
square1 =0.0
square2 =0.0
cosine_similarity = 0.0
for j in range(0,11):
    dot_product = dot_product + (sm1[j]*sm2[j])
    square1 = square1 + (sm1[j]*sm1[j])
    square2 = square2 + (sm2[j]*sm2[j])

print('cosine_similarity', dot_product/((math.sqrt(square1))*(math.sqrt(square2))) )
pd.set_option('display.max_columns',None)

print(dataset.corr())


file_handler = open("corelation.csv","r")


dataset1 = pd.read_csv(file_handler,sep = ",")

file_handler.close()


dataset_bike1 = dataset1[dataset1['BikeBuyer'] ==1]

dataset_bike0= dataset1[dataset1['BikeBuyer'] ==0]

dataset_bike1.drop(['BikeBuyer'],axis = 1, inplace = True)
dataset_bike0.drop(['BikeBuyer'],axis = 1, inplace = True)


print(dataset_bike1.corr())
print(dataset_bike0.corr())
