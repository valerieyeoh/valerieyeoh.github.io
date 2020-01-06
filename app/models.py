from django.db import models
from scipy.optimize import linprog
import numpy as np

class Session(models.Model):
	session_id = models.CharField(max_length=40, default = '', primary_key=True)
	raw_material = models.CharField(max_length=25, default = '', null=True)
	product = models.CharField(max_length=25, default='', null=True)

	# product_slate = models.CharField(max_length=100, default='', null=True)
	input_val_rm = models.CharField(max_length=100, default=[], null=True)
	input_val_prod = models.CharField(max_length=100, default=[], null=True)
	input_val_ass = models.CharField(max_length=100, default='', null=True)
	hourly_labor_cost = models.CharField(max_length=100, default='', null=True)
	labor_hours_avail = models.CharField(max_length=100, default='', null=True)
	product_1 = models.CharField(max_length=100, default='', null=True)
	product_2 = models.CharField(max_length=100, default='', null=True)
	product_3 = models.CharField(max_length=100, default='', null=True)
	gross_margins = models.CharField(max_length=100, default='', null=True)
	sector_req = models.CharField(max_length=100, default='', null=True)
	bounds = models.CharField(max_length=100, default='', null=True)
	result = models.CharField(max_length=100, default='', null=True)
	gross_margin = models.CharField(max_length=100, default='', null=True)
	revenue = models.CharField(max_length=100, default='', null=True)
	opex = models.CharField(max_length=100, default='', null=True)

# Create your models here.
class Calc(models.Model):
	Hourly_Labor_Cost_1 = models.IntegerField()
	Hourly_Labor_Cost_2 = models.IntegerField()
	Hourly_Labor_Cost_3 = models.IntegerField()
	Labor_Hours_Avail_1 = models.IntegerField()
	Labor_Hours_Avail_2 = models.IntegerField()
	Labor_Hours_Avail_3 = models.IntegerField()
	Product_1_USP = models.IntegerField()
	Product_1_UC = models.IntegerField()
	Product_1_S1 = models.IntegerField()
	Product_1_S2 = models.IntegerField()
	Product_1_S3 = models.IntegerField()
	Product_1_Min = models.IntegerField()
	Product_1_Max = models.IntegerField()
	Product_2_USP = models.IntegerField()
	Product_2_UC = models.IntegerField()
	Product_2_S1 = models.IntegerField()
	Product_2_S2 = models.IntegerField()
	Product_2_S3 = models.IntegerField()
	Product_2_Min = models.IntegerField()
	Product_2_Max = models.IntegerField()


	def calculation(self):
		solu = {}
		solu['gross_margin'] = [-(Product_1_USP - Product_1_UC - (Product_1_S1*Hourly_Labor_Cost_1+Product_1_S2*Hourly_Labor_Cost_2+Product_1_S3*Hourly_Labor_Cost_3)), -(Product_2_USP - Product_2_UC - (Product_2_S1*Hourly_Labor_Cost_1+Product_2_S2*Hourly_Labor_Cost_2+Product_2_S3*Hourly_Labor_Cost_3))]
		solu['sector_req'] = [[Product_1_S1, Product_2_S1],[Product_1_S2, Product_2_S2],[Product_1_S3, Product_2_S3]]
		solu['hours_avail'] = [Labor_Hours_Avail_1, Labor_Hours_Avail_2,Labor_Hours_Avail_3]
		solu['bounds'] = [[Product_1_Min, Product_1_Max],[Product_2_Min, Product_2_Max]]

		#Total quantity of raw material
		res = linprog(solu['gross_margin'], A_ub = solu['sector_req'], b_ub = solu['hours_avail'], bounds = solu['bounds'])
		#Total Gross Margin
		gmargin = -np.dot([res.x[0], res.x[1]], solu['gross_margin'])
		self.res_A = res[0]
		self.res_B = res[1]
		self.gmargin = gmargin
		return(res[0],res[1],gmargin)
