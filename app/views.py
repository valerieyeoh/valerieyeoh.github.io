from django.shortcuts import render, redirect
from app.models import Calc, Session
from scipy.optimize import linprog
import numpy as np
import pandas as pd
import mimetypes
import eikon as ek
import json
from django.http import HttpResponse

# Changeable inputs
title = 'Oilseeds Value Chain'
desc = 'The Oilseeds Value Chain constitutes important input for animal, food and fuel production with the products having an extensive range of uses and applications.'
sectors = {
	'1' : 'Crushing & Pressing',
	'2' : 'Secondary Transformation',
}
raw_materials = {
	'1': 'Rapeseed',
	'2': 'Sunflower',
	'3': 'Soya',
}
final_products = {
	'1': {'title': 'Rapeseed Products', 'desc': '40% Rapeseed oil, 60% Rapeseed meal'},
	'2': {'title': 'Sunflower Products', 'desc': '42% Sunflower oil, 35% Sunflower meal'},
	'3': {'title': 'Soya Products', 'desc': '20% Soybean oil, 46% Soybean meal'}
}
eproducts = {
	'1': 'Rapeseed Oil',
	'2': 'Rapeseed Meal',
	'3': 'Sunflower Oil',
	'4': 'Sunflower Meal',
	'5': 'Soybean Oil',
	'6': 'Soybean Meal',
}
# input_val_rm = [{'high-st': '0.00', 'high-mt': '0.00', 'high-lt': '0.00', 'low-st': '0.00', 'low-mt': '0.00', 'low-lt': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00', },{'high-st': '0.00', 'high-mt': '0.00', 'high-lt': '0.00', 'low-st': '0.00', 'low-mt': '0.00', 'low-lt': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00', },{'high-st': '0.00', 'high-mt': '0.00', 'high-lt': '0.00', 'low-st': '0.00', 'low-mt': '0.00', 'low-lt': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00', }]
# input_val_prod = [{'high-st': '0.00', 'high-mt': '0.00', 'high-lt': '0.00', 'low-st': '0.00', 'low-mt': '0.00', 'low-lt': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00', },{'high-st': '0.00', 'high-mt': '0.00', 'high-lt': '0.00', 'low-st': '0.00', 'low-mt': '0.00', 'low-lt': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00', },{'high-st': '0.00', 'high-mt': '0.00', 'high-lt': '0.00', 'low-st': '0.00', 'low-mt': '0.00', 'low-lt': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00', },{'high-st': '0.00', 'high-mt': '0.00', 'high-lt': '0.00', 'low-st': '0.00', 'low-mt': '0.00', 'low-lt': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00', },{'high-st': '0.00', 'high-mt': '0.00', 'high-lt': '0.00', 'low-st': '0.00', 'low-mt': '0.00', 'low-lt': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00', },{'high-st': '0.00', 'high-mt': '0.00', 'high-lt': '0.00', 'low-st': '0.00', 'low-mt': '0.00', 'low-lt': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00', }]
# input_val_ass = [{'hlc_1': '0', 'lha_1': '0', 'capex_1': '0', 'hlc_2': '0', 'lha_2': '0', 'capex_2': '0', 'lha_p1_s1': '0.0', 'lha_p1_s2': '0.0', 'lha_p2_s1': '0.0', 'lha_p2_s2': '0.0', 'lha_p3_s1': '0.0', 'lha_p3_s2': '0.0'}]
# input_val_ass = [{'hlc_1': '0', 'lha_1': '0', 'capex_1': '0','hlc_2': '0', 'lha_2': '0': 'capex_2': '0', 'lha_p1_s1': '0.0', 'lha_p1_s2': '0.0', 'lha_p2_s1': '0.0', 'lha_p2_s2': '0.0', 'lha_p3_s1': '0.0', 'lha_p3_s2': '0.0'}]


# options = ['Rapeseed low', 'Rapeseed average', 'Rapeseed high', 'Sunflower low', 'Sunflower average', 'Sunflower high', 'Soya low', 'Soya average', 'Soya high',]

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

#Preliminary Work
wb_rm = pd.read_excel('app/raw-materials-upload-template.xlsx', names = ['Date','RAPESEED LOW', 'RAPESEED AVG', 'RAPESEED HIGH', 'SUNFLOWER LOW', 'SUNFLOWER AVG', 'SUNFLOWER HIGH', 'SOYA LOW', 'SOYA AVG', 'SOYA HIGH'])
# wb['Date'] = [date.strftime("%b %Y") for date in wb['Date']]
rapeseed = wb_rm[['Date', 'RAPESEED AVG']].values.tolist()
sunflower = wb_rm[['Date', 'SUNFLOWER AVG']].values.tolist()
soya = wb_rm[['Date', 'SOYA AVG']].values.tolist()
xaxis = wb_rm['Date'].values.tolist()

wb = pd.read_excel('app/final-prod-prices.xlsx', names = ['Date','RAPESEED OIL', 'RAPESEED MEAL', 'SUNFLOWER OIL', 'SUNFLOWER MEAL', 'SOYBEAN OIL', 'SOYBEAN MEAL'])

rapeseed_oil = wb[['Date', 'RAPESEED OIL']].values.tolist()
rapeseed_meal = wb[['Date', 'RAPESEED MEAL']].values.tolist()
sunflower_oil = wb[['Date', 'SUNFLOWER OIL']].values.tolist()
sunflower_meal = wb[['Date', 'SUNFLOWER MEAL']].values.tolist()
soybean_oil = wb[['Date', 'SOYBEAN OIL']].values.tolist()
soybean_meal = wb[['Date', 'SOYBEAN MEAL']].values.tolist()

def home(request):
	temp = request.session.session_key
	print(temp)
	context = {'temp': temp}
	return render(request, 'home.html', context)

def error(request):
	return render(request, '404.html', {})

def download(request):
	path = 'app'
	filename = 'raw-materials-upload-template.xlsx'
	fl = open(path, 'r')
	mime_type, _ = mimetypes.guess_type(path)
	response = HttpResponse(fl, content_type=mime_type)
	response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
	return response

def oilseeds(request):
	context = {
		'title': title,
		'desc': desc,
		'products': final_products,
		'sectors': sectors,
		}
	return render(request, 'oilseeds-vc.html', context)

def oilseeds_raw_materials(request):
	try:
		sess = Session.objects.get(session_id=request.session.session_key)
	except Session.DoesNotExist:
		sess = Session(session_id = request.session.session_key)

	if((sess.input_val_rm) == None):
		input_val_rm = [{'high-st': '0.00', 'high-mt': '0.00', 'high-lt': '0.00', 'low-st': '0.00', 'low-mt': '0.00', 'low-lt': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00', },{'high-st': '0.00', 'high-mt': '0.00', 'high-lt': '0.00', 'low-st': '0.00', 'low-mt': '0.00', 'low-lt': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00', },{'high-st': '0.00', 'high-mt': '0.00', 'high-lt': '0.00', 'low-st': '0.00', 'low-mt': '0.00', 'low-lt': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00', }]
	else:
		input_val_rm = sess.input_val_rm

	if((sess.raw_material) == None):
		selected = [{},{},{}]
	else:
		selected = sess.raw_material

	context = {
		'title': title,
		'desc': desc,
		'instr': "Here, we upload an excel file containing the raw material prices, the assumed premium/discount and the transportation costs for the defined periods. Download the sample to view the excel template. ",
		'raw_materials': raw_materials,
		'input_val': input_val_rm,
		'selected': selected,
		'xaxis': xaxis,
		'rapeseed': rapeseed,
		'sunflower': sunflower,
		'soya': soya,
		'sess': sess
		}

	if request.method == "POST":
		input_val = (request.POST.get('input_val'))
		selected = request.POST.get('selected')

		sess.raw_material = selected
		sess.input_val_rm = input_val
		sess.save(force_update=True)
		return redirect('oilseeds_products')

	if request.method == "GET":
		return render(request, 'oilseeds-raw-materials.html', context)

# https://developers.refinitiv.com/eikon-apis/eikon-data-apis/quick-start (for TR)
# tmp_df, err = ek.get_data(quote, ['DSPLY_NAME'])
# futures = tmp_df['Instrument'].tolist()[1:]
# df = ek.get_timeseries(futures, interval="daily", start_date="", end_date="")

def oilseeds_products(request):
	try:
		sess = Session.objects.get(session_id=request.session.session_key)
	except Session.DoesNotExist:
		sess = Session(session_id = request.session.session_key)

	print(sess.input_val_prod == None)
	print(len(sess.input_val_prod))
	if((sess.input_val_prod) == None or len(sess.input_val_prod) == 0):
		print("here")
		input_val_prod = [{'high-st': '0.00', 'high-mt': '0.00', 'high-lt': '0.00', 'low-st': '0.00', 'low-mt': '0.00', 'low-lt': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00', },{'high-st': '0.00', 'high-mt': '0.00', 'high-lt': '0.00', 'low-st': '0.00', 'low-mt': '0.00', 'low-lt': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00', },{'high-st': '0.00', 'high-mt': '0.00', 'high-lt': '0.00', 'low-st': '0.00', 'low-mt': '0.00', 'low-lt': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00', },{'high-st': '0.00', 'high-mt': '0.00', 'high-lt': '0.00', 'low-st': '0.00', 'low-mt': '0.00', 'low-lt': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00', },{'high-st': '0.00', 'high-mt': '0.00', 'high-lt': '0.00', 'low-st': '0.00', 'low-mt': '0.00', 'low-lt': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00', },{'high-st': '0.00', 'high-mt': '0.00', 'high-lt': '0.00', 'low-st': '0.00', 'low-mt': '0.00', 'low-lt': '0.00', 'quality-prem': '0.00', 'transport-cost': '0.00', }]
	else:
		print('there')
		input_val_prod = sess.input_val_prod

	if((sess.product) == None):
		selected = [{},{},{},{},{},{}]
	else:
		selected = sess.product	

	context = {
		'title': title,
		'desc': desc,
		'products': eproducts,
		'xaxis': xaxis,
		'input_val': input_val_prod,
		'selected': selected,
		'rapeseed_oil': rapeseed_oil,
		'rapeseed_meal': rapeseed_meal,
		'sunflower_oil': sunflower_oil,
		'sunflower_meal': sunflower_meal,
		'soybean_oil': soybean_oil,
		'soybean_meal': soybean_meal,
		'sess': sess
		}
	
	if request.method == "POST":
		input_val = (request.POST.get('input_val'))
		selected = request.POST.get('selected')

		sess.product = selected
		sess.input_val_prod = input_val
		sess.save(force_update=True)
		return redirect('oilseeds_assets')

	return render(request, 'oilseeds-products.html', context)

def oilseeds_assets(request):
	try:
		sess = Session.objects.get(session_id=request.session.session_key)
	except Session.DoesNotExist:
		sess = Session(session_id = request.session.session_key)

	if request.method == "GET":
		context = {
		'title': title,
		'desc': desc,
		'input_val': sess.input_val_ass,
		'raw_materials': raw_materials,
		'products': final_products,
		'sectors': sectors,
		'sess': sess,
		'hourly_labor_cost': sess.hourly_labor_cost,
		'labor_hours_avail': sess.labor_hours_avail,
		'sector_req': sess.sector_req
		}
		return render(request, 'oilseeds-assets.html', context)

	if request.method == "POST":
		Hourly_Labor_Cost_1 = float(request.POST.get('HLC_1', False))
		Hourly_Labor_Cost_2 = float(request.POST.get('HLC_2', False))
		Labor_Hours_Avail_1 = float(request.POST.get('LHA_1', False))
		Labor_Hours_Avail_2 = float(request.POST.get('LHA_2', False))
		Product_1_S1 = float(request.POST.get('Rapeseed Products_S1', False))
		Product_1_S2 = float(request.POST.get('Rapeseed Products_S2', False))
		Product_2_S1 = float(request.POST.get('Sunflower Products_S1', False))
		Product_2_S2 = float(request.POST.get('Sunflower Products_S2', False))
		Product_3_S1 = float(request.POST.get('Soya Products_S1', False))
		Product_3_S2 = float(request.POST.get('Soya Products_S2', False))

		Hourly_Labor_Cost = [Hourly_Labor_Cost_1, Hourly_Labor_Cost_2]
		Labor_Hours_Avail = [Labor_Hours_Avail_1, Labor_Hours_Avail_2]
		Product_1 = [Product_1_S1, Product_1_S2]
		Product_2 = [Product_2_S1, Product_2_S2]
		Product_3 = [Product_3_S1, Product_3_S2]
		sector_req = [[Product_1_S1, Product_2_S1, Product_3_S1],[Product_1_S2, Product_2_S2, Product_3_S2]]

		sess.input_val_ass = request.POST.get('input_val', False)
		sess.hourly_labor_cost = Hourly_Labor_Cost
		sess.labor_hours_avail = Labor_Hours_Avail
		sess.product_1 = Product_1
		sess.product_2 = Product_2
		sess.product_3 = Product_3
		sess.sector_req = sector_req
		sess.save(force_update = True)

		return redirect('oilseeds_optimisation')

def oilseeds_optimisation(request):
	# wb = pd.read_excel('app/raw-materials-upload-template.xlsx', names = ['Date','RAPESEED LOW', 'RAPESEED AVG', 'RAPESEED HIGH', 'SUNFLOWER LOW', 'SUNFLOWER AVG', 'SUNFLOWER HIGH', 'SOYA LOW', 'SOYA AVG', 'SOYA HIGH', 'CANOLA LOW', 'CANOLA AVG', 'CANOLA HIGH'])
	# xaxis = wb['Date'].values.tolist()
	try:
		sess = Session.objects.get(session_id=request.session.session_key)
	except Session.DoesNotExist:
		sess = Session(session_id = request.session.session_key)

	context ={
		'title': title,
		'desc': desc,
		'sectors': sectors,
		'products': final_products,
		'dates': xaxis,
		'sess': sess}

	if request.method == 'POST':
		Product_1_USP = float(request.POST.get('product_1_usp', False))
		Product_1_UC = float(request.POST.get('product_1_uc', False))
		Product_1_Min = float(request.POST.get('product_1_Min', False))
		Product_1_Max = float(request.POST.get('product_1_Max', False))
		Product_2_USP = float(request.POST.get('product_2_USP', False))
		Product_2_UC = float(request.POST.get('product_2_UC', False))
		Product_2_Min = float(request.POST.get('product_2_Min', False))
		Product_2_Max = float(request.POST.get('product_2_Max', False))
		Product_3_USP = float(request.POST.get('product_3_USP', False))
		Product_3_UC = float(request.POST.get('product_3_UC', False))
		Product_3_Min = float(request.POST.get('product_3_Min', False))
		Product_3_Max = float(request.POST.get('product_3_Max', False))
		print(request.POST.get('product_1_usp'))
		print(Product_1_USP)
		print('test')
		print(request.POST.get('Hourly_Labor_Cost_1', False))


		#manipulation from whatever models field to list values
		product_1 = json.loads(sess.product_1)
		product_2 = json.loads(sess.product_2)
		product_3 = json.loads(sess.product_3)
		hlc = json.loads(sess.hourly_labor_cost)
		sector_req = json.loads(sess.sector_req)
		labor_hours_avail = json.loads(sess.labor_hours_avail)
		solu = {}
		solu['gross_margins'] = [-(Product_1_USP - Product_1_UC - (np.dot(product_1, hlc))), -(Product_2_USP - Product_2_UC - (np.dot(product_2, hlc))), -(Product_3_USP - Product_3_UC - (np.dot(product_3, hlc)))]
		solu['sector_req'] = sector_req
		solu['hours_avail'] = labor_hours_avail
		solu['bounds'] = [[Product_1_Min, Product_1_Max],[Product_2_Min, Product_2_Max], [Product_3_Min, Product_3_Max]]
		product = json.loads(sess.product)

		#Total quantity of raw material
		res = linprog(solu['gross_margins'], A_ub = solu['sector_req'], b_ub = solu['hours_avail'], bounds = solu['bounds'])
		# print(res)
		# prod_price = [Product_1_USP, Product_2_USP, Product_3_USP]
		# print(product)
		# print(product[0])
		# print(product[0]['ydata'])
		prod_price = [(float(0.4*product[0]['ydata'][0])+ float(0.6*product[1]['ydata'][0])), (float(0.42*product[2]['ydata'][0])+float(0.35*product[3]['ydata'][0])), (float(0.2*product[4]['ydata'][0])+ float(0.46*product[5]['ydata'][0]))]
		print("printign res")
		print(res)
		sess.gross_margins = solu['gross_margins']
		sess.bounds = solu['bounds']
		sess.result = list(res.x)
		print("values")
		print(Product_1_USP)
		print(Product_2_USP)
		print(Product_3_USP)
		sess.gross_margin = np.dot([Product_1_USP, Product_2_USP, Product_3_USP], res.x)
		print(np.dot(res.x, [Product_1_USP, Product_2_USP, Product_3_USP]))
		sess.revenue = np.dot(res.x, prod_price)
		sess.opex = np.dot(res.x, list(np.dot([product_1, product_2, product_3], hlc)))

		sess.save(force_update=True)
		return redirect('oilseeds_result')

	return render(request, 'oilseeds-opt.html', context)

def oilseeds_result(request):
	try:
		sess = Session.objects.get(session_id=request.session.session_key)
	except Session.DoesNotExist:
		sess = Session(session_id = request.session.session_key)

	if request.method == "GET":
		raw_material = json.loads(sess.raw_material)
		prod_usp = json.loads(sess.product)
		hourly_labor_cost = json.loads(sess.hourly_labor_cost)
		product_1 = json.loads(sess.product_1)
		product_2 = json.loads(sess.product_2)
		product_3 = json.loads(sess.product_3)
		hlc = json.loads(sess.hourly_labor_cost)
		res = json.loads(sess.result)

		# opex cost of the products
		opex = list(np.dot([product_1, product_2, product_3], hlc))

		# raw material cost
		rm_cost = np.dot([raw_material[0]['ydata'][0], raw_material[1]['ydata'][0], raw_material[2]['ydata'][0]],res)

		# transformation cost
		trans_cost = np.dot(opex, res)
		print("opexing now")
		print(opex)
		print(trans_cost)

		gmargin_f = []
		revenue_f = []

		# per unit time / year
		for i in range(len(xaxis)):
			temp1 = []
			temp2 = []

			# prod price for the year, using respective percentages of oil and meal
			prod_price = [int(0.4*prod_usp[0]['ydata'][i]) + int(0.6*prod_usp[1]['ydata'][i]),
					int(0.42*prod_usp[2]['ydata'][i]) + int(0.35*prod_usp[3]['ydata'][i]),
					int(0.2*prod_usp[4]['ydata'][i]) + int(0.46*prod_usp[5]['ydata'][i])]
			print(prod_price)
			temp1 = np.dot(prod_price, res)
			print(temp1)

			# gmargin for the year
			gmargin = [prod_price[0]-raw_material[0]['ydata'][i]-opex[0], prod_price[1]-raw_material[1]['ydata'][i]-opex[1], prod_price[2]-raw_material[2]['ydata'][i]-opex[2]]
			temp2 = np.dot(gmargin, res)
			print(temp2)	

			revenue_f.append(round(temp1,2))
			gmargin_f.append(round(temp2,2))
		print(revenue_f)
		print(gmargin_f)

		context = {
			'title': title,
			'desc': desc,
			'raw_materials': raw_materials,
			'products': eproducts,
			'xaxis': xaxis,
			'sectors': sectors,
			'sess': sess,
			'rev': revenue_f,
			'gmargin': gmargin_f,
			'rm_cost': rm_cost,
			'trans_cost': trans_cost
			}

		return render(request, 'oilseeds-res.html', context)

def oilseeds_financials(request):
	try:
		sess = Session.objects.get(session_id=request.session.session_key)
	except Session.DoesNotExist:
		sess = Session(session_id = request.session.session_key)

	context = {
		'title': title,
		'desc': desc,
		'raw_materials': raw_materials,
		'products': eproducts,
		'xaxis': xaxis,
		'sectors': sectors,
		'sess': sess,
		}
	return render(request, 'oilseeds-financials.html', context)

def grains(request):
	context = {
		'title': title,
		'desc': desc,
		}
	return render(request, 'grains-vc.html', context)

def grains_raw_materials(request):
	categories = ['Wheat-good','Wheat-bad']
	wheat_good = [[1,2],[5,10],[20,30]]
	wheat_bad = [[1,3],[5,20],[20,40]]

	values = [[1,3],[5,20],[20,40]]
	context = {
		'title': title,
		'desc': desc,
		'instr': "Here, we upload an excel file containing the raw material prices, the assumed premium/discount and the transportation costs for the defined periods. Download the sample to view the excel template. ",
		'raw_materials': {
			'1': 'Rapeseed',
			'2': 'Sunflower',
			'3': 'Soya',
			'4': 'Canola'
			},
		'chart': {
		 	'chart': {'type': 'line'},
		    'title': {'text': 'Graph Title'}, 
		    'series': [{'name': 'Rapeseed',
		    'data': values
		    	}]
	    	},
		}
	return render(request, 'grains-raw-materials.html', context)

def grains_asset(request):
	#Input asset information in the following order: asset name, description of asset, assumptions made, cost per asset, quantity of asset
	asset = {
	'asset1': ['Silos and Elevators', 'Description of silos and elevators. Estimated capital cost is XX. Estimated maintenance cost is XX.', 'Capacity of XX', '2', '1',''],
	'asset2': ['Bulk terminals and logistics assets', 'Description of bulk terminals. Estimated capital cost is XX. Estimated maintenance cost is XX.', 'Capacity of XX', '5', '1',''],
	'asset3': ['Mills', 'Description of mills. Estimated capital cost is XX. Estimated maintenance cost is XX.', 'Capacity of XX', '3', '1',''],
	'asset4': ['Packaging and distribution facilities', 'Description of packaging and distribution facilities. Estimated capital cost is XX. Estimated maintenance cost is XX.', 'Capacity of XX', '7', '1',''],
	}
	context = {
	'title': title,
	'desc': desc,
	'asset': asset}
	return render(request, 'grains-asset.html', context)

def grains_final_products(request):
	context = {}
	return render(request, 'grains-final-prods.html', context)

def grains_uc(request):
	if request.method == "GET":
		process = {
		'Drying & Storage': 'Harvested grains are stored in elevators and silos for processing and shipment',
		'Trading & Chartering': 'International seaborne trade',
		'Terminals & Storage': 'Receiving terminals for storage and conditioning',
		'Primary Transformation': {
			'Cleaning': 'Description including fixed and variable costs',
			'Conditioning': 'Description including fixed and variable costs',
			'Milling': 'Description including fixed and variable costs',
			'Sieving': 'Description including fixed and variable costs'
		},
		'Packaging, Storage & Distribution': 'Packaging and distribution',
		'Secondary Transformation': 'Milled products are processed and blended',
		}

		context = {
		'title': title,
		'desc': desc,
		'process': process,
		# 'data': excel_data
		}
		return render(request, 'grains-uc.html', context)

def grains_uch(request):
	#Input information of the process, following the order 'process step title': 'process step description' for each step
	if request.method == "GET":
		wb = pd.read_excel('app/raw-materials-prices.xlsx')
		print(wb.iloc[0][:1].values)
		excel_data = dict()
		# for i in range(6):
		# 	temp = wb.loc[i,:]
		# 	key = wb.loc[i,0:1]
		# 	print(key)
		# 	data = list()
			# for j in temp:
			# 	print(j)
		# for i in range(6):
		# 	temp = wb.loc[i,0:1]
		# 	print(temp)
		# 	test = wb.loc[i, 1:]
		# 	print("here:",test)

			# excel_data[wb.loc[i,:1]] = wb.loc[i, 1:]

		# print(excel_data)
		# wb = load_workbook('app/raw-materials-prices.xlsx', data_only=True)
		# ws = wb.active

		# excel_data = dict()
		# count = 0
		# for row in ws.iter_rows():
		# 	if count == 0:
		# 		xAxis = list()
		# 		count += 1
		# 		for cell in row:
		# 			xAxis.append(cell.value)
		# 	else:
		# 		count += 1
		# 		row_data = list()
		# 		for cell in row:
		# 			row_data.append(cell.value)
		# 	excel_data.append(row_data)

		test = [
		{'label': 'Wheat-good','data': [[1,2],[5,10],[20,30]]},
		{'label': 'Wheat-bad','data': [[1,3],[5,20],[20,40]]},]

		categories = ['Wheat-good','Wheat-bad']
		wheat_good = [[1,2],[5,10],[20,30]]
		wheat_bad = [[1,3],[5,20],[20,40]]

		chart = {
	        'chart': {'type': 'line'},
	        'title': {'text': 'Title'},
	        'xAxis': {'categories': categories},
	        'series': [wheat_good, wheat_bad],
	    }

	    # chart = json.dumps(chart)
	    # chart = json.dumps(json.loads(chart))

	    # dump = json.dumps(chart)
		# print(excel_data[0])
		# print(excel_data[1])

		temp = [[1,2],[5,10],[20,30]]
		process = {
		'Drying & Storage': 'Harvested grains are stored in elevators and silos for processing and shipment',
		'Trading & Chartering': 'International seaborne trade',
		'Terminals & Storage': 'Receiving terminals for storage and conditioning',
		'Primary Transformation': {
			'Cleaning': 'Description including fixed and variable costs',
			'Conditioning': 'Description including fixed and variable costs',
			'Milling': 'Description including fixed and variable costs',
			'Sieving': 'Description including fixed and variable costs'
		},
		'Packaging, Storage & Distribution': 'Packaging and distribution',
		'Secondary Transformation': 'Milled products are processed and blended',
		}

		context = {
		'title': title,
		'desc': desc,
		'process': process,
		'chart': chart,
		# 'data': [[1,2],[3,4]],
		'test': test,
		'titles': {'1': 'Wheat-good', '2': 'Wheat-bad'},
		'data': {'Wheat-good': temp, 'Wheat-bad': [[1,5],[5,20],[20,40]]}
		# 'data': excel_data
		}
		return render(request, 'grains-uc.html', context)

def grains_opt(request):
	products = {
		'1': 'Flour',
		'2': 'Rice',
	}
	context = {
		'title': title,
		'desc': desc,
		'products': products,
		'sec1': sector1,
		'sec2': sector2,
		'sec3': sector3,
		}

	if request.method == "GET":
		return render(request, 'grains-opt.html', context)

	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			return redirect('grains_opt', pk=post.pk)

def grains_res(request):

	if request.method == "POST":
		Hourly_Labor_Cost_1 = int(request.POST.get('Hourly_Labor_Cost_1', False))
		Hourly_Labor_Cost_2 = int(request.POST.get('Hourly_Labor_Cost_2', False))
		Hourly_Labor_Cost_3 = int(request.POST.get('Hourly_Labor_Cost_3', False))
		Labor_Hours_Avail_1 = int(request.POST.get('Labor_Hours_Avail_1', False))
		Labor_Hours_Avail_2 = int(request.POST.get('Labor_Hours_Avail_2', False))
		Labor_Hours_Avail_3 = int(request.POST.get('Labor_Hours_Avail_3', False))
		Product_1_USP = int(request.POST.get('Product_1_USP', False))
		Product_1_UC = int(request.POST.get('Product_1_UC', False))
		Product_1_S1 = int(request.POST.get('Product_1_S1', False))
		Product_1_S2 = int(request.POST.get('Product_1_S2', False))
		Product_1_S3 = int(request.POST.get('Product_1_S3', False))
		Product_1_Min = request.POST.get('Product_1_Min', False)
		Product_1_Max = request.POST.get('Product_1_Max', False)
		Product_2_USP = int(request.POST.get('Product_2_USP', False))
		Product_2_UC = int(request.POST.get('Product_2_UC', False))
		Product_2_S1 = int(request.POST.get('Product_2_S1', False))
		Product_2_S2 = int(request.POST.get('Product_2_S2', False))
		Product_2_S3 = int(request.POST.get('Product_2_S3', False))
		Product_2_Min = request.POST.get('Product_2_Min', False)
		Product_2_Max = request.POST.get('Product_2_Max', False)
		solu = {}
		solu['gross_margin'] = [-(Product_1_USP - Product_1_UC - (Product_1_S1*Hourly_Labor_Cost_1+Product_1_S2*Hourly_Labor_Cost_2+Product_1_S3*Hourly_Labor_Cost_3)), -(Product_2_USP - Product_2_UC - (Product_2_S1*Hourly_Labor_Cost_1+Product_2_S2*Hourly_Labor_Cost_2+Product_2_S3*Hourly_Labor_Cost_3))]
		solu['sector_req'] = [[Product_1_S1, Product_2_S1],[Product_1_S2, Product_2_S2],[Product_1_S3, Product_2_S3]]
		solu['hours_avail'] = [Labor_Hours_Avail_1, Labor_Hours_Avail_2,Labor_Hours_Avail_3]
		solu['bounds'] = [[Product_1_Min, Product_1_Max],[Product_2_Min, Product_2_Max]]
		print(solu)

		#Total quantity of raw material
		res = linprog(solu['gross_margin'], A_ub = solu['sector_req'], b_ub = solu['hours_avail'], bounds = solu['bounds'])
		print(res)

		context = {
		'title': title,
		'product_1': 'Flour',
		'product_2': 'Rice',
		'res_A': res.x[0],
		'res_B': res.x[1],
		'gmargin': -(res.fun)
		}
	return render(request, 'grains-res.html', context)

def grains_cashflow(request):
	context = {
	'title': title,
	'desc': desc,
	'raw_material_1': 'Flour',
	'raw_material_2': 'Rice'}
	return render(request, 'grains-cashflow.html', context)

def test(request):
	return render(request, 'test.html', {})

def test1(request):
	if request.method == "POST":
		Hourly_Labor_Cost_1 = request.POST['Hourly_Labor_Cost_1']
		Hourly_Labor_Cost_2 = request.POST['Hourly_Labor_Cost_2']
		Hourly_Labor_Cost_3 = request.POST['Hourly_Labor_Cost_3']
		Labor_Hours_Avail_1 = request.POST['Labor_Hours_Avail_1']
		Labor_Hours_Avail_2 = request.POST['Labor_Hours_Avail_2']
		Labor_Hours_Avail_3 = request.POST['Labor_Hours_Avail_3']
		Product_A_USP = request.POST['Product_A_USP']
		Product_A_UC = request.POST['Product_A_UC']
		Product_A_S1 = request.POST['Product_A_S1']
		Product_A_S2 = request.POST['Product_A_S2']
		Product_A_S3 = request.POST['Product_A_S3']
		Product_A_Min = request.POST['Product_A_Min']
		Product_A_Max = request.POST['Product_A_Max']
		Product_B_USP = request.POST['Product_B_USP']
		Product_B_UC = request.POST['Product_B_UC']
		Product_B_S1 = request.POST['Product_B_S1']
		Product_B_S2 = request.POST['Product_B_S2']
		Product_B_S3 = request.POST['Product_B_S3']
		Product_B_Min = request.POST['Product_B_Min']
		Product_B_Max = request.POST['Product_B_Max']

		Calc.objects.create(
            Hourly_Labor_Cost_1 = Hourly_Labor_Cost_1,
            Hourly_Labor_Cost_2 = Hourly_Labor_Cost_2,
            Hourly_Labor_Cost_3 = Hourly_Labor_Cost_3,
            Labor_Hours_Avail_1 = Labor_Hours_Avail_1,
            Labor_Hours_Avail_2 = Labor_Hours_Avail_2,
            Labor_Hours_Avail_3 = Labor_Hours_Avail_3,
            Product_A_USP = Product_A_USP,
            Product_A_UC = Product_A_UC,
            Product_A_S1 = Product_A_S1,
            Product_A_S2 = Product_A_S2,
            Product_A_S3 = Product_A_S3,
            Product_A_Min = Product_A_Min,
            Product_A_Max = Product_A_Max,
            Product_B_USP = Product_B_USP,
            Product_B_UC = Product_B_UC,
            Product_B_S1 = Product_B_S1,
            Product_B_S2 = Product_B_S2,
            Product_B_S3 = Product_B_S3,
            Product_B_Min = Product_B_Min,
            Product_B_Max = Product_B_Max
        )

	return render(request, 'test.html', {})