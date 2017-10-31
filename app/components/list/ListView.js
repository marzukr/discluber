import React from 'react';

import ClubList from "./clubs/ClubList.js";
import TermList from "./terms/TermList.js";

import anime from 'animejs';

export default class ListView extends React.Component 
{
    animateFromBottom(endResultHidden)
    {
        
    }

    render() {
        return (
            <div className="row" id="listView" style={{opacity: "0.5"}}>
                <div className="col">
                    <h3 style={{textAlign: "center"}}>TERMS</h3><br/>
                    <TermList terms={this.props.listData.terms}/>
                </div>
                <div className="col">
                    <h3 style={{textAlign: "center"}}>CLUBS</h3><br/>
                    <ClubList clubList={this.props.listData.clubs}/>
                </div>
                <div className="col">
                    <h3 style={{textAlign: "center"}}>USERS</h3><br/>
                </div>
            </div>
        );
    }
}