from flask import Flask,render_template

#Creates a flask webpage
app = Flask(__name__)

#Creates a webpage based on the html template given
@app.route('/')
def index():
	return render_template('main.js')
#used to actually run the webpage server
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

