from flask import Flask, render_template, request
from lib.formula import Formula
from lib.exception import *
import os

app=Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method=='GET':
		return render_template('index.html')
	else:
		input_formula=request.form['formula']

		os.system('rm static/*.png 2>/dev/null')


		try:
			f=Formula(input_formula)
			#string=f.toString()
			#latex=f.getLatexString()
			df_list=[]
			for var in f.getVariables():
				df=f.getDerivativeBy(var)
				df_list.append(df)

			plot=None
			deri_plot=None
			if len(df_list)<=1:
				plot=f.getPlotImage(-6,6,'plot.png')
				if plot==True:
					os.system('mv plot.png static/ 2>/dev/null')
				if len(df_list)==1:
					deri_plot=df_list[0].getPlotImage(-10,10,'deri_plot.png')
					if deri_plot==True:
						os.system('mv deri_plot.png static/ 2>/dev/null')
			

			return render_template('index.html', input_formula=input_formula, formula=f, deri_formulas=df_list, plot=plot, deri_plot=deri_plot)
		except Error as e:
			return render_template('index.html', input_formula=input_formula, error=e)

if __name__=='__main__':
	app.run(host='0.0.0.0', port=8443, debug=True)
