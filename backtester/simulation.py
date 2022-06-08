from lstm import *
from connect_db import *
import collections
def simulate(data, money, threshold, features):
	"""
	Simulates the stock market for the bot.

	:param data: dict:
		dates: list | list of dates
		prices: list | list of prices
	:param money: int | starting amount of money
	:param threshold: float | constant used for bot
	:param features: int | constant used for bot, the bot makes a prediction when we have enough features
	"""

	#WRITE RETURN COMMENTS




	#lstm prediction values for each day
	pred_values = []
	#2d array. each element has [date, order type] format
	date_results = []
	#we segment the data into individual days. the data is cleaned, a single date has 390 corresponding price values
	segmentedData = []


	#now our data is a 2d array, where the format of each element is [dates for a day, prices for a day]
	i = 0
	tempDates = []
	tempPrice = []
	for date, price in zip(data['dates'], data['prices']):
		i += 1
		tempDates.append(date)
		tempPrice.append(price)
		if i == 390:
			segmentedData.append([tempDates, tempPrice])
			tempDates = []
			tempPrice = []
			i = 0

	data = segmentedData
	

	#how many stocks are currently owned
	stocks = 0
	#the value of the account which is composed of money and stocks * their valuation
	account_value = money
	#variable for calculating results
	initial = money 
	#the history of stocks owned
	stock_history = []
	#the history of cash
	money_history = []
	#the history of profit
	profit_history = []
	#the history of account value
	account_value_history = []
	#what day we are on
	day = 0
	#number of buy orders
	num_buys = 0
	#number of sell orders
	num_sells = 0


	#constant, maybe should change to accuracy of the model
	RATIO = 7 


	#starting market simulation, day by day
	for day in data: 
		#array to feed into the lstm model
		to_predict = []
		#since the bot only buys once a day at most
		bought = False
		#the prediction value for this day
		pred = None


		#streaming in the day's data
		for date, price in zip(day[0], day[1]):
			to_predict.append(price)

			#updates account value since stock prices are changing
			account_value = stocks * price + money

			#each minute we store the history
			account_value_history.append(account_value)
			profit_history.append(account_value - initial)
			money_history.append(money)
			stock_history.append(stocks)


			#when we have enough data for making a prediction
			if(len(to_predict) == features):

				pred = predict_day(to_predict, features)
				pred_values.append([str(date)[:10], str(round(pred,3))])
				

			#when we are ready to make an order
			if(pred != None and bought == False):
					
				#green day
				if(price < to_predict[0] and pred > threshold): 
					num_buys += 1
					date_results.append([date, 'BUY'])
					stocks += (money * RATIO/10)/price
					money -= money * RATIO/10
					bought = True

				#red day
				elif price > to_predict[0] and pred < threshold:

					num_sells += 1
					date_results.append([date, 'SELL'])
					num_to_sell = stocks//2
					stocks -= num_to_sell
					money += num_to_sell*price
					bought = True



	profit = (account_value - initial)
	percent_gain = (account_value - initial)/initial
	market_percent_gain = (data[-1][1][-1] - data[0][1][0])/data[0][1][0]
	date_results = sorted(date_results, key=lambda x: x[0])

	#print("END GAIN:",  profit)
	#print("PERCENT GAIN:", percent_gain)
	#print("MARKET GAIN", market_percent_gain)
	#print("^^^^^^^^^^^^^", pred_values)


	return {"money_history": money_history, "stock_history": stock_history, "profit_history": profit_history,"pred_values": pred_values, "buy_sell_dates": date_results, "percent_gain": round(percent_gain,2), "profit": round(profit, 2) , "market_gain": round(market_percent_gain, 2), "num_buys": num_buys, "num_sells": num_sells}


if __name__ == "__main__":
	date_1 = "2018-12-20"
	date_2 = "2021-02-20"
	table = "GOOGL_DATA"
	data_1 = retrieve_data(table, date_1, date_1)
	data_2 = retrieve_data("AAPL_DATA", date_1, date_2)
	data_3 = retrieve_data("FB_DATA", date_1, date_2)
	money_1 = 1000000
	money_2 = 1
	threshold = 0.587
	features = 250
	print({"dates":data_1['dates'], "prices": data_1['prices']})
	#print((simulate({"dates":data_1['dates'], "prices": data_1['prices']}, money_1, threshold, features)))
	#print((simulate({"dates":data_2['dates'], "prices": data_2['prices']}, money_1, threshold, features)))
	#print((simulate({"dates":data_3['dates'], "prices": data_3['prices']}, money_1, threshold, features)))