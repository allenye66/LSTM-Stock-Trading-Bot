
import React, { useState } from "react";


export const Form = () => {


    const [startD, setStartD] = useState('')
    const [endD, setEndD] = useState('')
    const [company, setCompany] = useState('')
    const [shouldDraw, setShouldDraw] = useState(false)

    const handleSubmit = (event) => {

        event.preventDefault();

        //console.log("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        //console.log(startD)
        //console.log(endD)
        //console.log(company)
        //console.log(shouldDraw)


        const input = {
            "company": company, "startDate": startD, "endDate": endD, "drawLines": shouldDraw
        };

        fetch("/acceptDates", {
            method: 'POST',
            body: JSON.stringify(input),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json())
            .then(console.log("WORKED"))
            .catch(error => console.error('Error:', error));


    };


    return (
        <div>
            <form onSubmit={handleSubmit}>


                <select class="formInput" id="selectMenu" onChange={e => setCompany(e.target.value)}>
                    <option value="" disabled="disabled" selected="selected">Company</option>
                    <option value="GOOG">GOOG</option>
                    <option value="AAPL">AAPL</option>
                    <option value="FB">FB</option>
                    <option value="NFLX">NFLX</option>
                    <option value="AMZN">AMZN</option>
                    <option value="MSFT">MSFT</option>
                    <option value="NKE">NKE</option>
                    <option value="EBAY">EBAY</option>
                    <option value="TWTR">TWTR</option>
                    <option value="INTC">INTC</option>
                    <option value="TSLA">TSLA</option>
                    <option value="GOOGL">GOOGL</option>
                    <option value="NVDA">NVDA</option>
                    <option value="ORCL">ORCL</option>
                    <option value="V">V</option>
                    <option value="PYPL">PYPL</option>


                </select>


                <label> Start Date:</label>
                <input onChange={e => setStartD(e.target.value)} type="text" class="formInput" />
                <label> End Date:</label>
                <input onChange={e => setEndD(e.target.value)} type="text" class="formInput" />

                <input onChange={e => setShouldDraw(e.target.checked)}
                    type="checkbox" id="drawLines" name="drawLines" value="drawLines" />
                <label for="drawLines"> Draw Trade Lines </label>

                <input class="button" type="submit" value="submit" />



            </form>
        </div>
    );




}
