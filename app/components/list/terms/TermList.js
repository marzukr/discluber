import React from 'react';

import TermItem from "./TermItem.js";

export default class TermList extends React.Component 
{
    render() {
        let termItemList = [];
        for (let i = 0; i < this.props.terms.length; i++)
        {
            termItemList.push(<TermItem term={this.props.terms[i]} key={i}/>);
        }

        return (
            <div>
                <div className="card">
                    <div className="card-header">
                        <h3 className="cardHeader">Methodology</h3>
                    </div>
                    <div className="card-body centerText">
                        <div className="row">
                            {termItemList}
                        </div>
                    </div>
                </div>
                <div className="buffer"/>
            </div>
        );
    }
}