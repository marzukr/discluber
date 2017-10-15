import React from "react";
import ReactDOM from "react-dom";

import EntryController from "./entry/EntryController";

require("../styles/app.scss");

export default class App extends React.Component 
{
    render() {
        return (
            <div className="container">
                <EntryController/>
            </div>
        );
    }
}

ReactDOM.render(<App />, document.getElementById('root'));