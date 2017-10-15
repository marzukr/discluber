import React from 'react';

import TitleHeader from "./TitleHeader";
import FormController from "./form/FormController";

import anime from 'animejs';

export default class EntryController extends React.Component 
{
    moveUp()
    {
        let topSpacer = document.querySelector('#topSpacer');
        anime({
            targets: topSpacer,
            height: ["38.2vh", "7vh"],
            easing: "easeInOutQuad",
            duration: 750,
        });
    }

    render() {
        return (
            <div>
                <div className="row" style={{ height: "38.2vh" }} id="topSpacer"/>
                <TitleHeader/>
                <FormController moveUp={this.moveUp.bind(this)}/>
            </div>
        );
    }
}