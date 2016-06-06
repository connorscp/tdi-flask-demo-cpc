from flask import Flask, render_template, request
import datetime
from dateutil import relativedelta
import requests
import pandas as pd
from io import StringIO
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.util.string import encode_utf8
from bokeh.resources import INLINE

app = Flask(__name__)

database_name = 'WIKI'
api_key = '5CEVL-yKc5ufDbaeau8A'

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method =='GET':
        return render_template('userinfo.html')
    else:
        #request was a post

        # Get stock
        stock_ticker = request.form['stock_ticker'].upper()
        print stock_ticker

        # Set start_date as one month previous from today's date
        #now = datetime.datetime.now()
        #start_date = now + dateutil.relativedelta.relativedelta(months=-1)
        #start_date = start_date.strftime("%Y-%m-%d")
        #print start_date

        # Since ^ not working right now, set start date as one month previous
        start_date = '2016-05-05'
        print start_date

        # Call Quandl API to get csv of Date and stock Close for date range and put in dataframe
        response = requests.get('https://www.quandl.com/api/v3/datasets/'+database_name+'/'+stock_ticker
            +'.csv?api_key='+api_key+'&start_date='+start_date+'%column_index=0&column_index=4')

        stocks = pd.read_csv(StringIO(response.text), parse_dates=[0])

        # Build bokeh plot and grab script and div components
        p = figure(x_axis_type="datetime")
        p.title = stock_ticker+' Closing Prices'
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Stock Closing Price'
        p.line(stocks['Date'], stocks['Close'])

        # Configure resources to include BokehJS inline in the document.
        # For more details see:
        #   http://bokeh.pydata.org/en/latest/docs/reference/resources_embedding.html#bokeh-embed
        #js_resources = INLINE.render_js()
        #css_resources = INLINE.render_css()
        
        # For more details see:
        #   http://bokeh.pydata.org/en/latest/docs/user_guide/embedding.html#components
        #script, div = components(p, INLINE)
        #html = flask.render_template(
        #    'embed.html',
        #    plot_script=script,
        #    plot_div=div,
        #    js_resources=js_resources,
        #    css_resources=css_resources
        #)
        #return encode_utf8(html)
        
        
        
        script, div = components(p)

        return render_template('graph.html',stock=stock_ticker,script=script,div=div)

if __name__ == '__main__':
    #app.run(debug=True) # when running locally. Start w/ 127.0.0.1:5000/index
    app.run(host='0.0.0.0') # when running on DO. Start w/ vagrant:5000/index
    #app.run(port=33507) # when on Heroku. Start w/ 