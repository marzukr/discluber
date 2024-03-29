import React from 'react';

import UserForm from "./UserForm";
import FormAlert from "./FormAlert";
import LoadingIcon from "./LoadingIcon";

import $ from "jquery";

export default class FormController extends React.Component
{
    constructor(props)
    {
        super(props);
        this.state = {
            showAlert: false,
            twitterUsername: "",
            error: "",
            showLoadIcon: false,
            disableSubmit: false,
            resultsDisplayed: false,
            lastClubData: {clubs:[], terms:[]},
        };
    }

    formSubmitWithValidData(dataIsValid, data)
    {
        this.setState({
            showAlert: !dataIsValid,
            twitterUsername: data,
            showLoadIcon: dataIsValid,
            disableSubmit: dataIsValid,
        });

        if (!dataIsValid)
        {
            this.setState({error: "Invalid Twitter Username."});
        }
        else
        {
            if (this.state.resultsDisplayed)
            {
                this.props.resizeSpacer(true);
                this.props.displayList(false, this.state.lastClubData);
            }

            $.ajax({
                url: "/api/recommend",
                type: "GET",
                data: {twitterUsername: data},
                success: function(data) {
                    this.setState({
                        showLoadIcon: false, 
                        disableSubmit: false, 
                        resultsDisplayed: true, 
                        lastClubData: data,
                    });
                    this.props.resizeSpacer(false);
                    this.props.displayList(true, data);
                }.bind(this),
                error: (data) => {
                    console.log(data.responseJSON.message);
                },
            })
        }
    }

    render() {
        return (
            <div id="entryItems">
                <UserForm formSubmitWithValidData={this.formSubmitWithValidData.bind(this)} disableSubmit={this.state.disableSubmit}/>
                <FormAlert showAlert={this.state.showAlert} error={this.state.error}/>
                <LoadingIcon size={30} showLoadIcon={this.state.showLoadIcon}/>
            </div>
        );
    }
}