from flask import Flask, render_template, request, jsonify
from lib.formula import Formula
from lib.vector import Vector
from lib.exception import *
import os
import re
from collections import OrderedDict

import math

app=Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method=='GET':
		return render_template('index.html')
	else:
		formula_input=str(request.form['formula'])
		try:
			global f
			f=Formula(formula_input)

			start=-math.pi
			end=math.pi
			
			os.system('rm static/*.png 2>/dev/null')
	
			global df_list
			global var_list
			df_list={}
			var_list=[]
			if len(f.getVariables())==0:
				var_list.append('constant')
				df_list['constant']=f.getDerivativeBy('None')
			for var in f.getVariables():
				var_list.append(var)
				df=f.getDerivativeBy(var)
				df_list[str(var)]=df
			df_list=OrderedDict(sorted(df_list.items()))

			is_ploted=False
			is_deri_ploted=False
			if len(df_list)==1:
				is_ploted=draw_plot(start, end, f, 'plot.png')
				is_deri_ploted=draw_plot(start, end, df_list[var_list[0]], 'deri_plot.png')
			

			return render_template('index.html', formula_input=formula_input, formula=f, deri_formulas=df_list, is_ploted=is_ploted, is_deri_ploted=is_deri_ploted)


		except Error as e:
			return render_template('index.html', formula_input=formula_input, error=e)

@app.route('/_vector_input')
def render_dir_deri():
	vector_input=request.args.get('vector')

	vec_list=filter(None, re.split(r"[\s,]", vector_input))
	to_real_vector=[]
	for vec in vec_list:
		to_real_vector.append(float(vec))

	
	dir_deri=None
	try:
		if len(vec_list)>0 and len(vec_list)==len(f.getVariables()):
			dir_deri=f.getDirectionalDerivative(Vector(to_real_vector)).toString()
		elif len(vec_list)>0 and len(vec_list)!=len(f.getVariables()):
			raise InvalidVectorInput()
	except InvalidVectorInput as e:
		dir_deri=str(e)
		
	

	return jsonify(dir_deri=dir_deri)

@app.route('/_range_input')
def re_draw_plot():
	start=request.args.get('start')
	end=request.args.get('end')
	
	start=int(start)
	end=int(end)

	if len(df_list)==1:
		draw_plot(start, end, f, 'plot.png')
		draw_plot(start, end, df_list[var_list[0]], 'deri_plot.png')

	return jsonify()


def draw_plot(start, end, formula, filename):
	is_success=formula.getPlotImage(start, end, filename)
	if is_success==True:
		os.system('mv '+filename+' static/ 2>/dev/null')
	return is_success
		
	
if __name__=='__main__':
	app.run(host='0.0.0.0', port=8443, debug=True)
