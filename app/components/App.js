import React from "react";
import ReactDOM from "react-dom";

import TitleHeader from "./TitleHeader";
import UserForm from "./UserForm";

require("../styles/app.scss");

export default class App extends React.Component {
  render() {
    return (
        <div className="container">
            <div className = "row" style={{height: "38.2vh"}}/>
            <TitleHeader/>
            <UserForm/>
        </div>
    );
  }
}

ReactDOM.render(<App />, document.getElementById('root'));