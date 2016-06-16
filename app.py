from flask import Flask, render_template, request, jsonify
from lib.formula import Formula
from lib.vector import Vector
from lib.exception import *
import os
import re

import math

app=Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method=='GET':
		return render_template('index.html')
	else:
		formula_input=str(request.form['formula'])
	#	plot_range=str(request.form['range'])
	#	vector_input=str(request.form['vector2'])
		
	#	formula=formula_input
	#	inputs['formula']=formula_input
	#	inputs['ranges']=plot_range
	#	inputs['vector']=vector_input

		try:
			global f
			f=Formula(formula_input)

			


			start=-1*math.pi
			end=math.pi
			
			
	#		ranges=filter(None, re.split(r"[\s,]", plot_range))
	#		try:
	#			if len(ranges)==2:
	#				start=int(ranges[0])
	#				end=int(ranges[1])
	#		except:
	#			raise InvalidPlotRange()

	#		print "ranges : ", ranges

	#		vec_list=filter(None, re.split(r"[\s,]", vector_input))
	#		to_real_vector=[]
	#		for vec in vec_list:
	#			to_real_vector.append(float(vec))
	#		print "torealvector : ", to_real_vector

			print "varaibles : ", f.getVariables()

			dir_deri=None
	#		if len(vec_list)>0 and len(vec_list)==len(f.getVariables()):
	#			dir_deri=f.getDirectionalDerivative(Vector(to_real_vector)).toString()
	#		elif len(vec_list)>0 and len(vec_list)!=len(f.getVariables()):
	#			raise InvalidVectorInput()
			

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

			plot=None
			deri_plot=None
			if len(df_list)<=1:
				plot=f.getPlotImage(-50,50,'plot.png')
				if plot==True:
					os.system('mv plot.png static/ 2>/dev/null')
				if len(df_list)==1:
					deri_plot=df_list[var_list[0]].getPlotImage(start,end,'deri_plot.png')
					if deri_plot==True:
						os.system('mv deri_plot.png static/ 2>/dev/null')
			

			return render_template('index.html', formula_input=formula_input, formula=f, deri_formulas=df_list, plot=plot, deri_plot=deri_plot, dir_deri=dir_deri)


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

	os.system('rm static/*.png 2>/dev/null')
	plot=None		
	deri_plot=None
	if len(df_list)<=1:
		plot=f.getPlotImage(start,end,'plot.png')
		if plot==True:
			os.system('mv plot.png static/ 2>/dev/null')
		if len(df_list)==1:
			deri_plot=df_list[var_list[0]].getPlotImage(start,end,'deri_plot.png')
			if deri_plot==True:
				os.system('mv deri_plot.png static/ 2>/dev/null')
	return jsonify()
	

if __name__=='__main__':
	app.run(host='0.0.0.0', port=8443, debug=True)
