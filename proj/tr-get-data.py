# ek.set_app_key('b527a1554b6741759550a454c6117c78f783d7e1')
# temp = ek.get_timeseries(['RSc1','SUFc1','Sc1','COMc1','NRSc1'], interval="monthly", start_date="2019-01-01", end_date="2020-12-12", fields=['open','high','low','close'])
# temp.to_excel('C:/Users/chuen.wen.v.yeoh/OneDrive - Accenture/Desktop/Projects/temp/proj/app/TR-prices.xlsx', encoding='utf-8')

'''
data= pd.read_excel('C:/Users/chuen.wen.v.yeoh/OneDrive - Accenture/Desktop/Projects/temp/proj/app/TR-prices.xlsx', header=None)
count = 1
for x in range(5):
	value = data.loc[0,count]
	data.loc[0,count+1] = data.loc[0,count+2] = data.loc[0,count+3] = value
	count += 4

for x in range(1, data.shape[1]):
	value1 = data.loc[0,x]
	value2 = data.loc[1,x]
	value = str(value1) + ' ' + str(value2)
	data.loc[2,x] = value

data.to_excel('C:/Users/chuen.wen.v.yeoh/OneDrive - Accenture/Desktop/Projects/temp/proj/app/TR-prices-edited.xlsx')
'''

# ek.set_app_key('b527a1554b6741759550a454c6117c78f783d7e1')
# df_biodiesel = ek.get_timeseries(['PALMOLEO-MYc1','RSc1','RME-DDPCPTc1'], interval="monthly", start_date="2015-01-01", end_date="2020-01-12", fields=['open','high','low','close'])
# df_biodiesel.to_csv('C:/Users/chuen.wen.v.yeoh/OneDrive - Accenture/Desktop/Projects/temp/proj/app/raw-materials-prices.csv', encoding='utf-8') 


#https://stackoverflow.com/questions/17096888/getting-a-django-view-python-dict-into-highcharts-series-data/17107626#17107626

# https://developers.refinitiv.com/eikon-apis/eikon-data-apis/quick-start (for TR)
# tmp_df, err = ek.get_data(quote, ['DSPLY_NAME'])
# futures = tmp_df['Instrument'].tolist()[1:]
# df = ek.get_timeseries(futures, interval="daily", start_date="", end_date="")