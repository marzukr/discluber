import React from 'react';

export default class ClubItem extends React.Component 
{
    render() {
        return (
            <div className="row" style={{paddingBottom: "3em"}}>
                <div className="col" style={{textAlign: "right"}}>
                    <img src={this.props.clubObject.imageURL} className="rounded-circle border border-light" style={{height: "6em", width: "6em"}}/>
                </div>
                <div className="col align-self-center">
                    <h5>{this.props.number}. <a target="_blank" href={"https://twitter.com/" + this.props.clubObject.handle}>{this.props.clubObject.name}</a></h5>
                </div>
            </div>
        );
    }
}