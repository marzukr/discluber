import React from 'react';

import ClubList from "./clubs/ClubList.js";
import TermList from "./terms/TermList.js";

import anime from 'animejs';

export default class ListView extends React.Component 
{
    animateFromBottom()
    {
        
    }

    componentWillReceiveProps(nextProps)
    {
        
    }

    render() {
        return (
            <div className="row" id="listView" style={{opacity: "1"}}>
                <div className="col"/>

                <div className="col-7">
                    <ClubList clubList={this.props.listData.clubs}/>
                    <TermList terms={this.props.listData.terms}/>
                </div>

                <div className="col"/>
            </div>
        );
    }
}