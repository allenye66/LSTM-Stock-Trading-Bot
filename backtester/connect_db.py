import pandas as pd
import datetime
import psycopg2
from psycopg2 import sql


def add_zero(t):
    """
    Adds a "0" to the front of a string

    :param: string
    :return: string
    """
    t = str(t)
    if(len(t) == 1):
        return "0" + t
    else:
        return t 


def generate_dates(start, end):
    """
    Generates a list of consecutive BUSINESS dates starting from the first day to the end day

    :param start: string | start date
    :param end: string | end date
    :return: list | list of all the dates
    """
    date_list = pd.bdate_range(start, end)
    dates = []
    for d in date_list:
        temp = str(d.year) + "-" + add_zero(d.month) + "-" + add_zero(d.day)
        dates.append(temp)
    return dates



def retrieve_data(table_name, start, end):
    """
    Queries and retrieves data from PostgreSQL database. First calls generate_dates to find all the dates needed and then for each date sends a query.

    :param table_name: str | the table which we are querying from
    :param start: str | start date
    :param end: str | end date
    :return: dict:
        dates: list | a 1D list of sorted dates in str format
        prices: list | a 1D list of prices corresponding to the sorted dates
        bad_dates: list | a list of dates where the amount of data isn't normal
    """

    conn = psycopg2.connect(host="localhost", port = 5432, database="stock", user="allen") #password not needed for now
    cur = conn.cursor()

    all_open_data = []
    all_dates_data = []

    dates = generate_dates(start, end)

    #generate dates from start to end
    bad_dates = []
    for date in dates:

        date += "%"

        #special query format since dynamically choosing what table
        cur.execute(
    sql.SQL("""SELECT open, date FROM {table} where date like  (%s)""")
        .format(table=sql.Identifier(table_name)),
    [date])

        query_results = cur.fetchall()

        #if we have the normal amount of data, keep it
        if(len(query_results) == 390):

            for q in query_results:
                all_dates_data.append(str(q[1]))
                all_open_data.append(float(q[0]))
        else:
            bad_dates.append(date[:-1])
 
    #the queries aren't sorted, so sort the prices according to the dates
    sorted_prices = [x for _,x in sorted(zip(all_dates_data,all_open_data))]
    sorted_dates = sorted(all_dates_data) 

    cur.close()
    conn.close()

    return {"dates": sorted_dates, "prices": sorted_prices, "bad_dates": bad_dates}


