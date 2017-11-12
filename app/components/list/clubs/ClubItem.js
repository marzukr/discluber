import React from 'react';

export default class ClubItem extends React.Component 
{
    render() {
        return (
            <div className="row clubItem">
                <div className="col-auto" style={{textAlign: "left"}}>
                    <img src={this.props.clubObject.imageURL} className="rounded-circle border border-light" style={{height: "6em", width: "6em"}}/>
                </div>
                <div className="col verticalCenter leftText noWrap">
                    <h5>{this.props.number}. <a target="_blank" href={"https://twitter.com/" + this.props.clubObject.handle}>{this.props.clubObject.name}</a></h5>
                </div>
            </div>
        );
    }
}