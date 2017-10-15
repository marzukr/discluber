import React from 'react';

import UserForm from "./UserForm";
import FormAlert from "./FormAlert";

export default class FormController extends React.Component 
{
    constructor(props)
    {
        super(props);
        this.state = {
            showAlert: false,
            twitterUsername: "",
            error: "",
        };
    }

    formSubmitWithValidData(dataIsValid, data)
    {
        this.setState({
            showAlert: !dataIsValid,
            twitterUsername: data,
        });

        if (!dataIsValid)
        {
            this.setState({error: "Invalid Twitter Username."});
        }
        else
        {
            this.props.moveUp();
        }
    }

    render() {
        return (
            <div id="entryItems">
                <UserForm formSubmitWithValidData={this.formSubmitWithValidData.bind(this)}/>
                <FormAlert showAlert={this.state.showAlert} error={this.state.error}/>
            </div>
        );
    }
}