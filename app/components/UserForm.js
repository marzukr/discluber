import React from 'react';

export default class UserForm extends React.Component {
    render() {
        return (
            <div className="row" style={{paddingTop: "1.5em"}}>
                <div className="col"/>
                <div className="col">
                    <form>
                        <div className="form-row">
                            <div className="col">
                                <input type="text" class="form-control" id="inlineFormInputGroupUsername" placeholder="Username"/>
                            </div>
                            <div className="col-auto">
                                <button type="submit" class="btn btn-primary">Submit</button>
                            </div>
                        </div>
                    </form>
                </div>
                <div className="col"/>
            </div>
        );
    }
}