import React from "react";
import ReactDOM from "react-dom";

import TitleHeader from "./TitleHeader";

require("../styles/app.scss");

export default class App extends React.Component {
  render() {
    return (
        <TitleHeader/>
    );
  }
}

ReactDOM.render(<App />, document.getElementById('root'));