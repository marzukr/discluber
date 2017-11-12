import React from 'react';

export default class UserForm extends React.Component 
{
    constructor(props)
    {
        super(props);
        this.state = {
            twitterUsername: "",
        };
    }

    textInputChanged(event)
    {
        this.setState({
            [event.target.id]: event.target.value,
        });
    }

    formSubmitted(event)
    {
        event.preventDefault();
        let isValid = /(^@?[a-zA-Z_0-9]{1,15})$/.test(this.state.twitterUsername);
        this.props.formSubmitWithValidData(isValid, this.state.twitterUsername);
    }

    render() {
        return (
            <div className="row" style={{paddingTop: "1.5em"}}>
                <div className="col"/>
                <div className="col-6">
                    <form onSubmit={this.formSubmitted.bind(this)} autoComplete="off">
                        <div className="form-row">
                            <div className="col">
                                <input type="text" className="form-control" id="twitterUsername" placeholder="Twitter Username" value={this.state.twitterUsername} onChange={this.textInputChanged.bind(this)}/>
                            </div>
                            <div className="col-auto">
                                <button type="submit" className="btn btn-primary" disabled={this.props.disableSubmit}>Submit</button>
                            </div>
                        </div>
                    </form>
                </div>
                <div className="col"/>
            </div>
        );
    }
}