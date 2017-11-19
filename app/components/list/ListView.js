import React from 'react';

import ClubList from "./clubs/ClubList.js";
import TermList from "./terms/TermList.js";

import anime from 'animejs';

export default class ListView extends React.Component 
{
    animateOnScreen()
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

    animateOffScreen()
    {
        this.props.disableScroll(true);
        let clubSpacer = document.querySelector('#clubSpacer');
        anime({
            targets: clubSpacer,
            height: ["0vh", "100vh"],
            easing: "easeInOutQuad",
            duration: 750,
        });
    }

    componentWillReceiveProps(nextProps)
    {
        if (nextProps.shouldDisplay !== this.props.shouldDisplay)
        {
            if (nextProps.shouldDisplay)
            {
                this.animateOnScreen();
            }
            else
            {
                this.animateOffScreen();
            }
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