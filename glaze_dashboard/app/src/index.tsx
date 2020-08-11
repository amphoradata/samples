import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import * as serviceWorker from "./serviceWorker";

import { AmphoraProvider } from "react-amphora";
import { userManager } from "./amphora/userManager";
import { initalConfiguration } from "./amphora/configuration";
import { actionLogger } from "./amphora/loggers";

ReactDOM.render(
  <React.StrictMode>
    <AmphoraProvider
      userManager={userManager}
      configuration={initalConfiguration}
      onAction={actionLogger}
      onActionResult={actionLogger}
    >
      <App />
    </AmphoraProvider>
  </React.StrictMode>,
  document.getElementById("root")
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
