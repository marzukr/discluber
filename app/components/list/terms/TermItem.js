import React from 'react';

export default class TermItem extends React.Component 
{
    render() {
        return (
            <div className="row">
                <div className="col" style={{textAlign: "right", paddingRight: "0.5em"}}>
                    <h5>{this.props.number}.</h5>
                </div>
                <div className="col" style={{paddingLeft: "0"}}>
                    <h5>{this.props.term[0]}</h5>
                </div>
            </div>
        );
    }
}