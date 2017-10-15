import React from 'react';

export default class ClubList extends React.Component 
{
    render() {
        return (
            <div className="row" style={{paddingBottom: "3em"}}>
                <div className="col" style={{textAlign: "right"}}>
                    <img src="https://pbs.twimg.com/profile_images/378800000051668402/a15076880a27de03987d7d3e2b6df5eb.jpeg" className="rounded-circle border border-light" style={{height: "6em", width: "6em"}}/>
                </div>
                <div className="col align-self-center">
                    <h5>1. Sailing Club</h5>
                </div>
            </div>
        );
    }
}