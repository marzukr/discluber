import React from 'react';

import ClubItem from "./ClubItem.js";

export default class ClubList extends React.Component 
{
    render() {
        let clubItemList = [];
        for (let i = 0; i < this.props.clubList.length; i++)
        {
            clubItemList.push(<ClubItem number={i + 1} clubObject={this.props.clubList[i]} key={i}/>);
        }

        return (
            <div>
                {clubItemList}
            </div>
        );
    }
}