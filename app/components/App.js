import React from "react";
import ReactDOM from "react-dom";

import EntryController from "./entry/EntryController";
import ListView from "./list/ListView.js";

require("../styles/app.scss");

export default class App extends React.Component 
{
    constructor(props)
    {
        super(props);
        this.state = {
            shouldDisplayList: false,
            clubData: {clubs:[], terms:[]},
        };
    }

    displayList(clubData)
    {
        this.setState({
            shouldDisplayList: true,
            clubData: clubData,
        });
    }

    render() {
        return (
            <div className="container">
                <EntryController displayList={this.displayList.bind(this)}/>
                <ListView shouldDisplay={this.state.shouldDisplayList} listData={this.state.clubData}/>
            </div>
        );
    }
}

ReactDOM.render(<App />, document.getElementById('root'));