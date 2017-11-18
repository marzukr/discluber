import React from 'react';

import ClubList from "./clubs/ClubList.js";
import TermList from "./terms/TermList.js";

import anime from 'animejs';
import $ from "jquery";

export default class ListView extends React.Component 
{
    animateFromBottom()
    {
        
    }

    componentWillReceiveProps(nextProps)
    {
        if (nextProps.shouldDisplay)
        {
            console.log("hellow");
            $("body").css({"margin": "", "height": "", "overflow": ""});
        }
    }

    render() {
        return (
            <div className="row" id="listView" style={{marginTop: 500}}>
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