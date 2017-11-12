import React from 'react';

import ClubList from "./clubs/ClubList.js";
import TermList from "./terms/TermList.js";

import anime from 'animejs';

export default class ListView extends React.Component 
{
    animateFromBottom(endResultHidden)
    {
        
    }

    render() {
        let terms = [
            {
                name: "Terms",
                list: [{text: "term1", url: "yo"}, {text: "term1"}, {text: "term1", url: "yo"}],
            },
            {
                name: "Hashtags",
                list: [{text: "term1", url: "yo"}, {text: "term1"}, {text: "term1", url: "yo"}],
            },
            {
                name: "Websites",
                list: [{text: "term1", url: "yo"}, {text: "term1"}, {text: "term1", url: "yo"}],
            },
        ]
        return (
            <div className="row" id="listView" style={{opacity: "1"}}>
                <div className="col"/>

                <div className="col-7">
                    <ClubList clubList={[{name: "Clubs", handle: "handle", imageURL: "url"}, {name: "Clubs Of THi THi HTi THi", handle: "handle", imageURL: "url"}]}/>
                    <TermList terms={terms}/>
                </div>

                <div className="col"/>
            </div>
        );
    }
}