import React from 'react';

import anime from 'animejs';

export default class LoadingIcon extends React.Component 
{
    componentWillReceiveProps(nextProps)
    {
        if (nextProps !== this.props)
        {
            this.animateOpacity(nextProps.showLoadIcon);
        }
    }

    animateOpacity(showLoadIcon)
    {
        anime({
            targets: "#loadingIcon",
            height: this.props.size * (showLoadIcon ? 1 : 0),
            width: this.props.size * 4 * (showLoadIcon ? 1 : 0),
            duration: 300,
            easing: "easeInOutQuad",
        });
    }

    render() {
        return (
            <div className="row">
                <div className="col" style={{textAlign: "center"}}>
                    <svg id="loadingIcon" width="0" height="0" viewBox="0 0 135 135" xmlns="http://www.w3.org/2000/svg" className="loadingIcon">
                        <circle cx="15" cy="15" r="15">
                            <animate attributeName="r" from="15" to="15"
                                begin="0s" dur="0.8s"
                                values="15;9;15" calcMode="linear"
                                repeatCount="indefinite" />
                            <animate attributeName="fillOpacity" from="1" to="1"
                                begin="0s" dur="0.8s"
                                values="1;.5;1" calcMode="linear"
                                repeatCount="indefinite" />
                        </circle>
                        <circle cx="60" cy="15" r="9" fillOpacity="0.3">
                            <animate attributeName="r" from="9" to="9"
                                begin="0s" dur="0.8s"
                                values="9;15;9" calcMode="linear"
                                repeatCount="indefinite" />
                            <animate attributeName="fillOpacity" from="0.5" to="0.5"
                                begin="0s" dur="0.8s"
                                values=".5;1;.5" calcMode="linear"
                                repeatCount="indefinite" />
                        </circle>
                        <circle cx="105" cy="15" r="15">
                            <animate attributeName="r" from="15" to="15"
                                begin="0s" dur="0.8s"
                                values="15;9;15" calcMode="linear"
                                repeatCount="indefinite" />
                            <animate attributeName="fillOpacity" from="1" to="1"
                                begin="0s" dur="0.8s"
                                values="1;.5;1" calcMode="linear"
                                repeatCount="indefinite" />
                        </circle>
                    </svg>
                </div>
            </div>
        );
    }
}