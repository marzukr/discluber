import React from 'react';

import TermItem from "./TermItem.js";

export default class TermList extends React.Component 
{
    render() {
        let termItemList = [];
        for (let i = 0; i < this.props.terms.length; i++)
        {
            termItemList.push(<TermItem term={this.props.terms[i]} key={i} number={i+1}/>);
        }

        return (
            <div>
                {termItemList}
            </div>
        );
    }
}