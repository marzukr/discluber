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
                <div className="card">
                    <div className="card-header">
                        <h3 className="cardHeader">Clubs</h3>
                    </div>
                    <div className="card-body centerText">
                        <div className="divInlineBlock">
                            {clubItemList}
                        </div>
                    </div>
                </div>
                <div className="buffer"/>
            </div>
        );
    }
}