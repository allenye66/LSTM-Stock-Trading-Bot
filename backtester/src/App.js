import './App.css';

import { Analysis_Chart } from './Analysis_Chart'
import { Form } from './Form'



function App() {

  return (
    <div className="App">


      <div className="form">
        <Form />

        <div id='ranges'>
          <h2> Ticker Data Ranges: </h2>

          <ul>

            <li>
              <ul>
                <h4>  2018-12-17 to 2021-02-12 </h4>
                <li id="list_item">GOOG</li>
                <li id="list_item">GOOGL</li>
                <li id="list_item">AAPL</li>
                <li id="list_item">FB</li>

                <li id="list_item">EBAY</li>
                <li id="list_item">INTC</li>
                <li id="list_item">AMZN</li>
              </ul>
            </li>

            <li>
              <ul>
                <h4>  2018-12-17 to 2021-02-16 </h4>
                <li id="list_item">MSFT</li>
                <li id="list_item">NKE</li>
                <li id="list_item">NFLX</li>
                <li id="list_item">ORCL</li>
              </ul>
            </li>

            <li>
              <ul>
                <h4>  2019-12-18 to 2021-02-12 </h4>
                <li id="list_item">PYPL</li>

              </ul>
            </li>

            <li>
              <ul>
                <h4>  2020-12-17 to 2021-02-16 </h4>
                <li id="list_item">TSLA</li>
                <li id="list_item">V</li>
                <li id="list_item">TWTR</li>

              </ul>
            </li>
          </ul>
        </div>

      </div>

      <div align="center">


        <div id="analysis">
          <Analysis_Chart />
        </div>

      </div>



    </div>

  );
}

export default App;
