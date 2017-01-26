from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/welcome')
def welcome():
    return render_template('welcom.html')
@app.route('/goodbye')
def goodbye():
    return render_template('goodbye.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/report_filter_screen')
def rfs():
    return render_template('rfs.html')
@app.route('/facility_inventory_report')
def fir():
    return render_template('fir.html')
@app.route('/in_transit_report')
def itr():
    return render_template('itr.html')
@app.route('/logout')
def logout():
    return render_template('logout.html')


