from flask import Flask, render_template, request
from lib.formula import Formula
from lib.vector import Vector
from lib.exception import *
import os
import re

app=Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method=='GET':
		return render_template('index.html')
	else:
		formula_input=str(request.form['formula'])
		plot_range=str(request.form['range'])
		vector_input=str(request.form['vector'])
		
		inputs={}
		inputs['formula']=formula_input
		inputs['ranges']=plot_range
		inputs['vector']=vector_input

		try:
			f=Formula(formula_input)

			


			start=-20
			end=20
			
			
			ranges=filter(None, re.split(r"[\s,]", plot_range))
			if len(ranges)==2:
				start=int(ranges[0])
				end=int(ranges[1])
			print "ranges : ", ranges


			vec_list=filter(None, re.split(r"[\s,]", vector_input))
			to_real_vector=[]
			for vec in vec_list:
				to_real_vector.append(float(vec))
			print "torealvector : ", to_real_vector

			dir_deri=None
			if len(vec_list)>0 and len(vec_list)==len(f.getVariables()):
				dir_deri=f.getDirectionalDerivative(Vector(to_real_vector)).toString()
			elif len(vec_list)!=len(f.getVariables()):
				raise InvalidVectorInput()
			

			os.system('rm static/*.png 2>/dev/null')
	
			
			df_list=[]
			if len(f.getVariables())==0:
				df_list.append(f.getDerivativeBy("None"))
			for var in f.getVariables():
				df=f.getDerivativeBy(var)
				df_list.append(df)

			plot=None
			deri_plot=None
			if len(df_list)<=1:
				plot=f.getPlotImage(start,end,'plot.png')
				if plot==True:
					os.system('mv plot.png static/ 2>/dev/null')
				if len(df_list)==1:
					deri_plot=df_list[0].getPlotImage(start,end,'deri_plot.png')
					if deri_plot==True:
						os.system('mv deri_plot.png static/ 2>/dev/null')
			

			return render_template('index.html', inputs=inputs, formula=f, deri_formulas=df_list, plot=plot, deri_plot=deri_plot, dir_deri=dir_deri)


		except Error as e:
			return render_template('index.html', inputs=inputs, error=e)

if __name__=='__main__':
	app.run(host='0.0.0.0', port=8443, debug=True)
