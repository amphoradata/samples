import React from "react";
import {
  BrowserRouter as Router,
  RouteComponentProps,
  Route,
  Switch,
  withRouter,
  Link,
} from "react-router-dom";
import { userManager } from "./amphora/userManager";
import { CallbackPage } from "react-amphora";
import { ProtectedRoute } from "./ProtectedRoute";
import { Home } from "./Home";
import { Dashboard } from "./dashboard/Dashboard";

function App() {

  return (
    <Switch>
      <Route exact path="/" component={Home} />
      <ProtectedRoute
        path="/dashboard"
        component={Dashboard}
      />
    </Switch>
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
