import React from "react";
import ReactDOM from "react-dom";

import EntryController from "./entry/EntryController";
import ClubList from "./ClubList.js";

require("../styles/app.scss");

export default class App extends React.Component 
{
    render() {
        return (
            <div className="container">
                <EntryController/>
                {/* <ClubList/> */}
            </div>
        );
    }
}

ReactDOM.render(<App />, document.getElementById('root'));