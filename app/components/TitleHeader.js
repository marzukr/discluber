import React from 'react';

export default class TitleHeader extends React.Component {
    render() {
        return (
            <div className="row">
                <div className="col" style={{textAlign: "center"}}>
                    <h1>Discluber <em>your</em> club</h1><br/>
                    <h5>Want to join a club? Let Discluber find one to suit your interests...</h5>
                </div>
            </div>
        );
    }
}