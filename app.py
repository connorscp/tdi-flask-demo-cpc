from flask import Flask, render_template, request
import requests
import pandas as pd
from io import StringIO
from bokeh.plotting import figure
from bokeh.embed import components

app = Flask(__name__)

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method =='GET':
        return render_template('userinfo.html')
    else:
        #request was a post

        # Set Quandl parameters
        stock_ticker = request.form['stock_ticker'].upper()
        database_name = 'WIKI'
        num_days = '28'
        api_key = '5CEVL-yKc5ufDbaeau8A'

        # Call Quandl API to get csv of Date and stock Close for date range and put in dataframe
        response = requests.get('https://www.quandl.com/api/v3/datasets/'+database_name+'/'+stock_ticker
            +'.csv?api_key='+api_key+'&rows='+num_days+'&column_index=0&column_index=4')

        stocks = pd.read_csv(StringIO(response.text), parse_dates=[0])
        
        # Build bokeh plot and grab script and div components
        p = figure(x_axis_type="datetime")
        p.title = stock_ticker+' Closing Prices'
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Stock Closing Price'
        p.line(stocks['Date'], stocks['Close'])

        script, div = components(p)

        return render_template('graph.html',stock=stock_ticker,script=script,div=div)

if __name__ == '__main__':
    #app.run(debug=True) # when running locally. Start w/ 127.0.0.1:5000/index
    #app.run(host='0.0.0.0') # when running on DO. Start w/ vagrant:5000/index
    app.run(port=33507) # when on Heroku. Start w/ 