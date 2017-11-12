import React from 'react';

export default class TermItem extends React.Component 
{
    render() {
        let termList = [];
        for (let i = 0; i < this.props.term.list.length; i++)
        {
            let text = <h6 className="normalFontWeight" key={i}>{this.props.term.list[i].text}</h6>;
            let element = <a target="_blank" href={this.props.term.list[i].url}>{text}</a>;
            termList.push(element);
        }

        return (
            <div className="col centerText">
                <h5>{this.props.term.name.toUpperCase()}</h5>
                {termList}
            </div>
        );
    }
}