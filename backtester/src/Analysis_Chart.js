import React, { useState, Component, useEffect } from "react";
import Plot from 'react-plotly.js';
export const Analysis_Chart = () => {


    //for graphing the stock data
    const [dates, setDates] = useState([])
    const [prices, setPrices] = useState([])
    //earliest date
    const [startRange, setStartRange] = useState("")
    //latest date
    const [endRange, setEndRange] = useState("")

    //graphs the profit history
    const [profitHistory, setProfitHistory] = useState([])
    //graphs the stocks held history
    const [stockHistory, setStockHistory] = useState([])
    //graphs the history of the account value 
    const [moneyHistory, setMoneyHistory] = useState([])

    //graphs the buy/sell date lines
    const [lineDates, setLineDates] = useState([])


    //table for the buy sell dates
    const [buySellDates, setBuySellDates] = useState([['default', 'value']])

    //table for the predictions per day
    const [datePreds, setdDatePreds] = useState([['default', 'value']])

    //percent profit
    const [percentProfit, setPercentProfit] = useState(['None'])
    //amount of actual profit
    const [moneyProfit, setMyProfit] = useState(['None'])
    //percent profit if were to buy and hold
    const [marketPercentProfit, setMarketPercentProfit] = useState(['None'])
    //number of buy trades
    const [numBuyTrades, setNumBuyTrades] = useState(['None'])
    //number of sell trades
    const [numSellTrades, setNumSellTrades] = useState(['None'])


    //query backend at 1 second intervals for data to display
    useEffect(() => {
        const intervalId = setInterval(() => {

            fetch("/backtest_results").then(
                res => res.json()).then(
                    myData => {
                        if (myData['has_data'] == true) {
                            setMoneyHistory(myData['money_history'])
                            setProfitHistory(myData['profit_history'])
                            setStockHistory(myData['stock_history'])
                            setLineDates(myData['date_lines'])
                            setDates(myData['dates'])
                            setPrices(myData['prices'])
                            setStartRange(myData['dates'][0])
                            setEndRange(myData['dates'][myData['dates'].length - 1])
                            setdDatePreds(myData['pred_values'])
                            setBuySellDates(myData['buy_sell_dates'])
                            setPercentProfit(myData['percent_profit'])
                            setMyProfit(myData['money_profit'])
                            setMarketPercentProfit(myData['market_percent_profit'])
                            setNumBuyTrades(myData['buy_num_trades'])
                            setNumSellTrades(myData['sell_num_trades'])
                        }
                    },
                )

        }, 1000)

        return () => clearInterval(intervalId);

    }, [useState])




    //for generating dynamic tables
    const generateRow = rowData => (<tr>{rowData.map(generateCell)}</tr>);
    const generateCell = cellData => (<td>{cellData}</td>);
    const all_cols = ['Date', 'Decision'];
    const generateHeader = (count) => (<tr>{all_cols.slice(0, count).map((name) => <th>{name}</th>)}</tr>);
    const all_cols2 = ['Date', 'Prediction'];
    const generateHeader2 = (count) => (<tr>{all_cols2.slice(0, count).map((name) => <th>{name}</th>)}</tr>);


    //display layout:
    //  two tables
    //  metrics
    //  3 graphs
    return (

        <div>
            <div id="info">
                <div id="table_parent">

                    <div id="tables">
                        <div class="table">
                            <table>
                                <tbody>
                                    {generateHeader(buySellDates[0].length)}
                                    {buySellDates.map(generateRow)}
                                </tbody>
                            </table>
                        </div>

                        <div class="table">
                            <table>
                                <tbody>
                                    {generateHeader2(datePreds[0].length)}
                                    {datePreds.map(generateRow)}
                                </tbody>
                            </table>
                        </div>
                    </div>

                </div>

                <div id="analysis_parent">

                    <div id="flex" >
                        <div id="metric" >
                            <h1 id='metricName'> Percent Profit: </h1>
                            <p> {percentProfit}</p>
                        </div>

                        <div id="metric" >
                            <h1 id='metricName'> Market Percent Increase: </h1>
                            <p> {marketPercentProfit}</p>
                        </div>

                        <div id="metric">
                            <h1 id='metricName' > Money Profit: </h1>
                            <p> {moneyProfit}</p>
                        </div>


                        <div id="metric">
                            <h1 id='metricName'> Buy Trades: </h1>
                            <p> {numBuyTrades}</p>
                        </div>

                        <div id="metric" >
                            <h1 id='metricName'> Sell Trades: </h1>
                            <p> {numSellTrades}</p>
                        </div>

                    </div>

                </div>
            </div>



            <div id="chart">
                <Plot
                    data={[
                        {
                            x: dates,
                            y: prices,
                            type: 'scatter',
                        }
                    ]}


                    layout={{
                        autosize: false,
                        width: 1500,
                        height: 700,
                        title: {
                            text: 'Stock Data',
                            font: {
                                size: 24
                            },
                            xref: 'paper',
                        },

                        xaxis: {
                            rangebreaks: [
                                { bounds: ["sat", "mon"] },
                                //{ values: data['bad_dates'] },
                                { bounds: [16, 9.5], pattern: "hour" }
                            ],
                            range: [startRange, endRange]
                        },

                        //graph buy/sell lines
                        shapes: lineDates.map(([d, type_color]) => ({
                            type: 'rect',
                            xref: 'x',
                            yref: 'paper',
                            x0: d,
                            y0: 0,
                            x1: d,
                            y1: 1,
                            fillcolor: '#d3d3d3',
                            opacity: 0.8,
                            line: {
                                color: type_color,
                                width: 3,
                                dash: 'dot'
                            }
                        }))
                    }

                    }

                />
            </div>



            <div id="chart">
                <Plot
                    data={[
                        {
                            x: dates,
                            y: stockHistory,
                            type: 'bar',
                        }
                    ]}



                    layout={{

                        autosize: false,
                        width: 1500,
                        height: 700,
                        title: {
                            text: 'Stocks Held',
                            font: {
                                size: 24
                            },
                            xref: 'paper',
                        },

                        xaxis: {
                            rangebreaks: [
                                { bounds: ["sat", "mon"] },
                                { bounds: [16, 9.5], pattern: "hour" }
                            ],
                            range: [startRange, endRange]
                        },

                    }

                    }

                />
            </div>

            <div id="chart">
                <Plot
                    data={[
                        {
                            x: dates,
                            y: moneyHistory,
                            type: 'scatter'
                        }
                    ]}


                    layout={{
                        autosize: false,
                        width: 1500,
                        height: 700,
                        title: {
                            text: 'Remaining Cash',
                            font: {
                                size: 24
                            },
                            xref: 'paper',
                        },

                        xaxis: {
                            rangebreaks: [
                                { bounds: ["sat", "mon"] },
                                { bounds: [16, 9.5], pattern: "hour" }
                            ],
                            range: [startRange, endRange]
                        },


                    }

                    }

                />
            </div>


            <div id="chart">
                <Plot
                    data={[
                        {
                            x: dates,
                            y: profitHistory,
                            type: 'scatter'
                        }
                    ]}


                    layout={{
                        autosize: false,
                        width: 1500,
                        height: 700,
                        title: {
                            text: 'Profit',
                            font: {
                                size: 24
                            },
                            xref: 'paper',
                        },

                        xaxis: {
                            rangebreaks: [
                                { bounds: ["sat", "mon"] },
                                { bounds: [16, 9.5], pattern: "hour" }
                            ],
                            range: [startRange, endRange]
                        },


                    }

                    }

                />
            </div>





        </div>
    )
}