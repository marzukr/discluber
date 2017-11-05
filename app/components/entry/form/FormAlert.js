import React from 'react';

import anime from 'animejs';

export default class FormAlert extends React.Component 
{
    componentWillReceiveProps(nextProps)
    {
        if (nextProps !== this.props)
        {
            this.animateToggleHidden(nextProps);
        }
    }

    animateToggleHidden(nextProps)
    {
        let currentHeight = document.getElementById("errorBar").style.height;
        let nextHeight = nextProps.showAlert ? "4rem" : 0;

        let timeline = anime.timeline();
        timeline
            .add({
                targets: "#errorBar",
                height: [currentHeight, nextHeight],
                duration: 500,
                easing: "easeOutQuad",
            })
            .add({
                targets: "#errorBar",
                opacity: nextProps.showAlert ? 1 : 0,
                duration: 500,
                offset: 250,
                easing: "easeOutQuad",
            });
    }

    render() {
        return (
            <div className="row" style={{paddingTop: "0.5em", height: 0, opacity: 0}} id="errorBar">
                <div className="col"/>
                <div className="col-6">
                    <div className="alert alert-danger fade show" role="alert">{this.props.error}</div>
                </div>
                <div className="col"/>
            </div>
        );
    }
}