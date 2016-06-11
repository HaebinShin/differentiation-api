from flask import Flask, render_template, request
from lib.formula import Formula

app=Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method=='GET':
		return render_template('index.html')
	else:
		input_formula=request.form['formula']
		print input_formula
		f=Formula(input_formula)
		
		return render_template('index.html', formula=f.getLatex())

if __name__=='__main__':
	app.run(host='0.0.0.0', port=8443, debug=True)
