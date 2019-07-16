import pandas as pd
import numpy as np
import datetime

holidays = pd.read_csv("holidays.csv")
holidays.head(10)

holidays["Date"] = holidays["Date"].str.replace("-"," ")
holidays["Year"] = 2019
new = holidays["Date"].str.split(" ", expand = True)
holidays["Dates"]= new[0] 
holidays["Month"]= new[1]
holidays.drop(columns =["Date"], inplace = True)

holidays['FullDate'] = holidays['Dates'].map(str) + '-' + holidays['Month'].map(str) + '-' + holidays['Year'].map(str)
holidays['FullDate']= pd.to_datetime(holidays['FullDate'])
holidays.head()

dict_holidays = holidays.to_dict('records')
dict_holidays[:5]

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


@app.route("/")
def hello():
    return "Holiday Yay!"

@app.route("/holidays",methods=['GET'])
def holiday_10():
	hols_list = []
	curr_date = datetime.datetime.today()
	for hols in dict_holidays:
		if(curr_date <= hols['FullDate']):
			hols_list.append(hols)

	sorted_hols = sorted(hols_list, key=lambda x: x['FullDate'])
	return jsonify(sorted_hols[:10])

@app.route("/holidays/<string:holiday_type>",methods=['GET'])
def holiday_type_func(holiday_type):
	#holidaytype = request.args.get('type')
	hols_list = []
	curr_date = datetime.datetime.today()
	for hols in dict_holidays:
		if(curr_date <= hols['FullDate']):
			if(hols['Type'] == holiday_type):
				hols_list.append(hols)

	sorted_hols = sorted(hols_list, key=lambda x: x['FullDate'])
	return jsonify(sorted_hols[:10])



if __name__ == '__main__':
    app.run(debug=True)