import React from 'react';

import ClubList from "./clubs/ClubList.js";
import TermList from "./terms/TermList.js";

export default class ListView extends React.Component 
{
    render() {
        return (
            <div className="row" style={{display: (this.props.shouldDisplay ? "" : "none")}}>
                <div className="col">
                    <h3 style={{textAlign: "center"}}>Terms:</h3><br/>
                    <TermList terms={this.props.listData.terms}/>
                </div>
                <div className="col">
                    <h3 style={{textAlign: "center"}}>Clubs:</h3><br/>
                    <ClubList clubList={this.props.listData.clubs}/>
                </div>
                <div className="col">
                    <h3 style={{textAlign: "center"}}>Users:</h3><br/>
                </div>
            </div>
        );
    }
}