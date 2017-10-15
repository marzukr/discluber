import React from 'react';

import ClubItem from "./ClubItem.js";

export default class ClubList extends React.Component 
{
    render() {
        return (
            <div className="row">
                <div className="col"/>
                <div className="col">
                    <ClubItem/>
                    <ClubItem/>
                    <ClubItem/>
                    <ClubItem/>
                    <ClubItem/>
                </div>
                <div className="col"/>
            </div>
        );
    }
}