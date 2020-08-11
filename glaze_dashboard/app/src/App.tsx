import React from "react";
import {
  BrowserRouter as Router,
  RouteComponentProps,
  withRouter,
} from "react-router-dom";
import { userManager } from "./amphora/userManager";
import {
  CallbackPage,
  SignInButton,
  UserInformationComponent,
} from "react-amphora";
import "./App.css";
import logo from "./logo.svg";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <SignInButton alwaysOn={true} />
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
      <div>
        <UserInformationComponent />
      </div>
    </div>
  );
}

const AppWithCallbackPage: React.FunctionComponent<RouteComponentProps> = (
  props
) => {
  if (props.location.hash.substring(0, 10) === "#/callback") {
    const signInParams = props.location.hash.substring(10);
    return (
      <CallbackPage
        onSignIn={() => props.history.push("/")}
        {...props}
        userManager={userManager}
        signInParams={`${signInParams}`}
      />
    );
  }
  return <App />;
};

var ConnectedApp = withRouter(AppWithCallbackPage);

const RoutedApp: React.FunctionComponent = () => {
  return (
    <Router>
      <ConnectedApp />
    </Router>
  );
};

export default RoutedApp;
