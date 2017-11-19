import React from "react";
import ReactDOM from "react-dom";

import EntryController from "./entry/EntryController";
import ListView from "./list/ListView.js";

import $ from "jquery";

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

    displayList(shouldDisplay, clubData = {clubs:[], terms:[]})
    {
        this.setState({
            shouldDisplayList: shouldDisplay,
            clubData: clubData,
        });
    }

    disableScroll(shouldDisable)
    {
        console.log("Changing");
        if (shouldDisable)
        {
            $("body").css({"margin": "0", "height": "100%", "overflow": "hidden"});
        }
        else
        {
            $("body").css({"margin": "", "height": "", "overflow": ""});
        }
    }

    render() {
        return (
            <div className="container">
                <EntryController displayList={this.displayList.bind(this)}/>
                <ListView shouldDisplay={this.state.shouldDisplayList} listData={this.state.clubData} disableScroll={this.disableScroll.bind(this)}/>
                <div style={{height: "7vh", marginTop: "-2rem"}}/>
            </div>
        );
    }
}

ReactDOM.render(<App />, document.getElementById('root'));