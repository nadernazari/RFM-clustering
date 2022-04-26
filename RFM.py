#the more recent the purchase, the more responsive the customer is to promotions
#the more frequently the customer buys, the more engaged and satisfied they are
#monetary value differentiates heavy spenders from low-value purchasers
'''
Champions: are your best customers, who bought most recently, most often, and
are heavy spenders.Reward these customers. They can become early adopters for
new products and will help promote your brand.

Potential Loyalists: are your recent customers with average frequency and who
spent a good amount.Offer membership or loyalty programs or recommend related
products to upsell them and help them become your Loyalists or Champions.

New Customers: are your customers who have a high overall RFM score but are not
frequent shoppers.Start building relationships with these customers by providing
onboarding support and special offers to increase their visits.

At Risk Customers: are your customers who purchased often and spent big amounts,
but haven’t purchased recently.Send them personalized reactivation campaigns to
reconnect, and offer renewals and helpful products to encourage another purchase.

Can’t Lose Them: are customers who used to visit and purchase quite often, but
haven’t been visiting recently.Bring them back with relevant promotions, and run
surveys to find out what went wrong and avoid losing them to a competitor.
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#read Data
df = pd.read_excel("C:/Users/Nazari/Desktop/project/RFM/RFM.xlsx",
                   engine="openpyxl")

df = df.rename(columns={'کد مشتری':'Customer_ID',
                        'نام شرکت نگاشت':'company',
                        'نام شعبه':'‌Branch'})
#remove Na from customer Id column
df = df.dropna(subset=['Customer_ID'])
#create Monetary column
df['Monetary'] = df[['1398-01','1398-02','1398-03','1398-04','1398-05',
                     '1398-06','1398-07','1398-08','1398-09','1398-10',
                     '1398-11','1398-12','1399-01','1399-02','1399-03',
                     '1399-04','1399-05','1399-06','1399-07','1399-08',
                     '1399-09','1399-10','1399-11','1399-12','1400-01',
                     '1400-02','1400-03']].sum(axis=1,)
#remove 0 monetary
df = df[(df['Monetary'] != 0)]


df['Frequency'] = df[['1398-01','1398-02','1398-03','1398-04','1398-05',
                      '1398-06','1398-07','1398-08','1398-09','1398-10',
                      '1398-11','1398-12','1399-01','1399-02','1399-03',
                      '1399-04','1399-05','1399-06','1399-07','1399-08',
                      '1399-09','1399-10','1399-11','1399-12','1400-01',
                      '1400-02','1400-03']].apply(lambda s: (s > 0).sum(), axis=1)

df["Recency"] =  np.where( df['1400-03'] > 0, 0,
                 np.where( df['1400-02'] > 0, 1,
                 np.where( df['1400-01'] > 0, 2,
                 np.where( df['1399-12'] > 0, 3,
                 np.where( df['1399-11'] > 0, 4,
                 np.where( df['1399-10'] > 0, 5,
                 np.where( df['1399-09'] > 0, 6,
                 np.where( df['1399-08'] > 0, 7,
                 np.where( df['1399-07'] > 0, 8,
                 np.where( df['1399-06'] > 0, 9,
                 np.where( df['1399-05'] > 0, 10,
                 np.where( df['1399-04'] > 0, 11,
                 np.where( df['1399-03'] > 0, 12,
                 np.where( df['1399-02'] > 0, 13,
                 np.where( df['1399-01'] > 0, 14,
                 np.where( df['1398-12'] > 0, 15,
                 np.where( df['1398-11'] > 0, 16,
                 np.where( df['1398-10'] > 0, 17,
                 np.where( df['1398-09'] > 0, 18,
                 np.where( df['1398-08'] > 0, 19,
                 np.where( df['1398-07'] > 0, 20,
                 np.where( df['1398-06'] > 0, 21,
                 np.where( df['1398-05'] > 0, 22,
                 np.where( df['1398-04'] > 0, 23,
                 np.where( df['1398-03'] > 0, 24,
                 np.where( df['1398-02'] > 0, 25,
                 np.where( df['1398-01'] > 0, 26,27)))))))))))))))))))))))))))               
###########################################################################################
#sort & cunsum Monetary
df.sort_values(by=['Monetary'], inplace=True, ascending=False)
df['percent_Monetary']=df['Monetary']/sum(df['Monetary'])
df['percent_cumsum_Monetary']=df['percent_Monetary'].cumsum()
#if
df["Score_Monetary"] = np.where( df["percent_cumsum_Monetary"] >=0.75, 1,
                       np.where((df["percent_cumsum_Monetary"] >=0.5 ) & (df["percent_cumsum_Monetary"] <0.75), 2,
                       np.where((df["percent_cumsum_Monetary"] >=0.25) & (df["percent_cumsum_Monetary"] <0.5 ), 3,4)))
######################################################
#sort & cunsum Frequency
df.sort_values(by=['Frequency'], inplace=True, ascending=False)
df['percent_Frequency']=df['Frequency']/sum(df['Frequency'])
df['percent_cumsum_Frequency']=df['percent_Monetary'].cumsum()
#if
df["Score_Frequency"] = np.where( df["percent_cumsum_Frequency"] >=0.75, 1,
                        np.where((df["percent_cumsum_Frequency"] >=0.5 ) & (df["percent_cumsum_Frequency"] <0.75), 2,
                        np.where((df["percent_cumsum_Frequency"] >=0.25) & (df["percent_cumsum_Frequency"] <0.5 ), 3,4)))
######################################################
#sort & cunsum Recency
df.sort_values(by=['Recency'], inplace=True, ascending=False)
df['percent_Recency']=df['Recency']/sum(df['Recency'])
df['percent_cumsum_Recency']=df['percent_Recency'].cumsum()
#if
df["Score_Recency"] = np.where( df["percent_cumsum_Recency"] >=0.75, 4,
                      np.where((df["percent_cumsum_Recency"] >=0.5 ) & (df["percent_cumsum_Recency"] <0.75), 3,
                      np.where((df["percent_cumsum_Recency"] >=0.25) & (df["percent_cumsum_Recency"] <0.5 ), 2,1)))
######################################################
#Sum of three scores
df['RFM_score'] = df["Score_Recency"]+df["Score_Frequency"]+df["Score_Monetary"]
#Sumif each atribute

df['max_customerID_Frequency'] = df.groupby(['Customer_ID'])['Frequency'].transform('max')
df['min_customerID_Recency'] = df.groupby(['Customer_ID'])['Recency'].transform('min')

#create new data frame
df1 = df[['Customer_ID','Monetary','max_customerID_Frequency','min_customerID_Recency']]

df1["Monetary"] = df1["Monetary"][df1["Monetary"]>=0]
df1['Monetary'] = df1.groupby(['Customer_ID'])['Monetary'].transform('sum')

df1 = df1.drop_duplicates(subset ='Customer_ID', keep='first')
###########################################################################################
#Classification after group by Customer ID
###########################################################################################
#rename column
df1 = df1.rename(columns={'max_customerID_Frequency': 'Frequency',
                          'min_customerID_Recency':'Recency'})
######################################################
#sort & cunsum Monetary
df1.sort_values(by=['Monetary'], inplace=True, ascending=False)
df1['percent_Monetary']=df1['Monetary']/sum(df1['Monetary'])
df1['percent_cumsum_Monetary']=df1['percent_Monetary'].cumsum()
#if
df1["Score_Monetary"] = np.where( df1["percent_cumsum_Monetary"] >=0.75, 1,
                        np.where((df1["percent_cumsum_Monetary"] >=0.5 ) & (df1["percent_cumsum_Monetary"] <0.75), 2,
                        np.where((df1["percent_cumsum_Monetary"] >=0.25) & (df1["percent_cumsum_Monetary"] <0.5 ), 3,4)))
######################################################
#sort & cunsum Frequency
df1.sort_values(by=['Frequency'], inplace=True, ascending=False)
df1['percent_Frequency']=df1['Frequency']/sum(df1['Frequency'])
df1['percent_cumsum_Frequency']=df1['percent_Monetary'].cumsum()
#if
df1["Score_Frequency"] = np.where( df1["percent_cumsum_Frequency"] >=0.75, 1,
                         np.where((df1["percent_cumsum_Frequency"] >=0.5 ) & (df1["percent_cumsum_Frequency"] <0.75), 2,
                         np.where((df1["percent_cumsum_Frequency"] >=0.25) & (df1["percent_cumsum_Frequency"] <0.5 ), 3,4)))
######################################################
#sort & cunsum Recency
df1.sort_values(by=['Recency'], inplace=True, ascending=False)
df1['percent_Recency']=df1['Recency']/sum(df1['Recency'])
df1['percent_cumsum_Recency']=df1['percent_Recency'].cumsum()
#if
df1["Score_Recency"] = np.where( df1["percent_cumsum_Recency"] >=0.75, 4,
                       np.where((df1["percent_cumsum_Recency"] >=0.5 ) & (df1["percent_cumsum_Recency"] <0.75), 3,
                       np.where((df1["percent_cumsum_Recency"] >=0.25) & (df1["percent_cumsum_Recency"] <0.5 ), 2,1)))
###########################################################################################
#Sum of three scores
df1['RFM_score'] = df1["Score_Recency"] + df1["Score_Frequency"] + df1["Score_Monetary"]

writer = pd.ExcelWriter('RFM_analysis1.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='RFM_analysis')
df1.to_excel(writer, sheet_name='RFM_analysis1')
writer.save()

x = df['RFM_score']
plt.hist(x, bins = 20)
plt.show()

x = df1['RFM_score']
plt.hist(x, bins = 20)
plt.show()
