import React from "react";
import ReactDOM from "react-dom";

import TitleHeader from "./TitleHeader";
import FormController from "./FormController";

require("../styles/app.scss");

export default class App extends React.Component 
{
    formSubmitWithValidData(dataIsValid, data)
    {
        alert(dataIsValid);
    }

    render() {
        return (
            <div className="container">
                <div className="row" style={{ height: "38.2vh" }} />
                <TitleHeader/>
                <FormController/>
            </div>
        );
    }
}

ReactDOM.render(<App />, document.getElementById('root'));