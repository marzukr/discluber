import React from 'react';

import FormController from "./form/FormController";

import anime from 'animejs';

export default class EntryController extends React.Component 
{
    moveUp()
    {
        let topSpacer = document.querySelector('#topSpacer');

        if (topSpacer.style.height !== "7vh")
        {
            anime({
                targets: topSpacer,
                height: ["38.2vh", "7vh"],
                easing: "easeInOutQuad",
                duration: 750,
            });
        }
    }

    render() {
        return (
            <div>
                <div className="row" style={{ height: "38.2vh" }} id="topSpacer"/>
                <div className="row">
                    <div className="col"/>
                    <div className="col-7">
                        <div className="card">
                            <div className="card-body">
                                <div className="row">
                                    <div className="col" style={{ textAlign: "center" }}>
                                        <h1>Discluber <em>your</em> club</h1><br />
                                        <h5>Want to join a club? Let Discluber find one to suit your interests...</h5>
                                    </div>
                                </div>
                                <FormController moveUp={this.moveUp.bind(this)} displayList={this.props.displayList}/>
                            </div>
                        </div>
                    </div>
                    <div className="col"/>
                </div>
            </div>
        );
    }
}