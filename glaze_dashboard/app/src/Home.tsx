import React from "react";
import { Link } from "react-router-dom";
import {
  SignInButton,
  UserInformationComponent,
  useConfigState,
} from "react-amphora";
import "./App.css";
import logo from "./logo.svg";

export const Home = () => {
  const configState = useConfigState();
  const [isAuthenticated, setAuthenticated] = React.useState(
    configState.isAuthenticated
  );
  React.useEffect(() => {
    setAuthenticated(configState.isAuthenticated);
  }, [configState.isAuthenticated]);

  return (
    <div className="App">
      <header className="App-header">
        <SignInButton alwaysOn={true} />
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        {isAuthenticated && <Link className="App-link" to="/dashboard">View Dashboard</Link>}
      </header>
      <div>
        <UserInformationComponent />
      </div>
    </div>
  );
};
