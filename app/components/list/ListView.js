import React from 'react';

import ClubList from "./clubs/ClubList.js";
import TermList from "./terms/TermList.js";

import anime from 'animejs';

export default class ListView extends React.Component 
{
    animateFromBottom()
    {
        let clubSpacer = document.querySelector('#clubSpacer');
        anime({
            targets: clubSpacer,
            height: ["100vh", "0vh"],
            easing: "easeInOutQuad",
            duration: 750,
            complete: this.props.disableScroll(false),
        });
    }

    componentWillReceiveProps(nextProps)
    {
        if (nextProps.shouldDisplay)
        {
            this.animateFromBottom();
        }
    }

    render() {
        return (
            <div className="row" id="listView">
                <div className="col"/>

                <div className="col-7">
                    <div id="clubSpacer" style={{height: "100vh"}}/>
                    <ClubList clubList={this.props.listData.clubs}/>
                    <TermList terms={this.props.listData.terms}/>
                </div>

                <div className="col"/>
            </div>
        );
    }
}