from flask import Flask, request, render_template, jsonify, redirect, url_for, copy_current_request_context
from flask_sqlalchemy import SQLAlchemy
from regex import P
from connect_db import *
import threading
from threading import Timer
import time
from flask_cors import CORS, cross_origin
from lstm import *
from simulation import *
from constants import *

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def index():
    return "<h1 > Home page </h1>"


@app.after_request
def set_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response


def validDate(date):
    """
    Validates a string representing a date

    :param date: string
    :return: bool
    """

    arr = date.split("-")

    # check correct syntax
    if len(arr) != 3 or len(arr[0]) != 4 or len(arr[1]) != 2 or len(arr[2]) != 2:
        return False

    for num in arr:
        if(num.isdigit() == False):
            return False

    # check valid month values
    if not (int(arr[1]) > 0 and int(arr[1]) < 13):
        return False

    # check valid day value (simple)
    if not (int(arr[2]) > 0 and int(arr[2]) < 32):
        return False

    return True


@app.route('/acceptDates', methods=['GET', 'POST'])
def get_dates():
    """
    Receives input from the React form and changes the global variables to initiate /backtest_results

    startD: string | start date
    endD: string | end date
    company: string | ticker name
    drawLines: bool | if we should draw the buy/sell lines
    shouldPredict: bool | if /backtest_results should run
    """

    global startD
    global endD
    global company
    global drawLines
    global shouldPredict
    

    sent_input = request.get_json()

    if sent_input is not None:

        startD = sent_input['startDate']
        endD = sent_input['endDate']
        company = sent_input['company']
        drawLines = sent_input['drawLines']

        if (validDate(startD) == False or validDate(endD) == False):
            return "BAD INPUT"

        #makes startD always the earlier date
        if(startD > endD):
            startD, endD = endD, startD

        shouldPredict = True

        return "DONE"
    else:
        
        return "BAD INPUT"


@app.route('/backtest_results', methods=['GET', 'POST'])
def backtest():
    """
    When shouldPredict turns to true, first query the database to obtain the data for the given dates.
    After getting the data from the query, send the data to simulation.
    Return simulation results.

    return: dict:
        has_data: bool | to tell frontend if it should accept new results
        profit_history: list | a list of the profit values at every minute
        stock_history: list | a list of the amount of stocks held at every minute
        dates: list | a list of the dates at minute intervals from startD to endD range
        prices: list | a list of the open price of the stock at every minute
        pred_values: list | a list of the LSTM prediction results for every day
        date_lines: list | a 2D list where each inner list element contains the date when the bot buys/sells and the color of the line
        buy_sell_dates: list | a 2D list where each inner list element contains the date when the bot buys/sells and the order type
        percent_profit: float | the percent profit respective to the starting amount of money
        money_profit: float | the amount of actual profit
        market_percent_profit: float | the profit that can be made if just buying and holding
        buy_num_trades: int | the number of buy trades
        sell_num_trades: int | the number of sell trades
    """
    
    global shouldPredict
    global date_lines
    global company
    global drawLines

    if(shouldPredict):

        #the vertical lines that show when the bot buys/sells
        date_lines = []

        #the table names are in GOOG_DATA format
        table_name = company + '_DATA'

        #calls the retrieve data function from connect_db.py
        data = retrieve_data(table_name, startD, endD)

        simulation_data = {"dates": data['dates'], "prices": data['prices']}

        #pass the data to the simulation function in simulation.py
        simulation_res = simulate(
            simulation_data, MONEY, THRESHOLD, FEATURE_SIZE)

        #the user can choose whether to draw the lines or not
        if(drawLines):
            for date, order_type in simulation_res['buy_sell_dates']:
                if order_type == "BUY":
                    date_lines.append([date, 'green'])
                else:
                    date_lines.append([date, 'red'])
        

        shouldPredict = False

        return jsonify({"money_history": simulation_res['money_history'], "has_data": True, "profit_history": simulation_res['profit_history'], 'stock_history': simulation_res['stock_history'], "dates": data['dates'], 'prices': data['prices'], "pred_values": simulation_res['pred_values'], "date_lines": date_lines, "buy_sell_dates": simulation_res['buy_sell_dates'], "percent_profit": simulation_res['percent_gain'], "money_profit": simulation_res["profit"], "market_percent_profit": simulation_res["market_gain"], 'buy_num_trades': simulation_res['num_buys'], 'sell_num_trades': simulation_res['num_sells']})

    else:
        return jsonify({})


if __name__ == '__main__':
    global startD
    global endD
    global shouldPredict
    global company
    global drawLines

    # default values for global variables initialization
    drawLines = False
    company = 'GOOG'
    startD = "2019-12-13"
    endD = "2019-12-25"
    shouldPredict = False
    date_lines = []

    app.run(debug=True)
