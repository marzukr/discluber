import React from 'react';
import 'bootstrap';

export default class FormAlert extends React.Component 
{
    render() {
        return (
            <div className="row" style={{paddingTop: "0.5em"}}>
                <div className="col"/>
                <div className="col">
                    <div className={"alert alert-danger fade " + (this.props.showAlert ? "show" : "")} role="alert">{this.props.error}</div>
                </div>
                <div className="col"/>
            </div>
        );
    }
}