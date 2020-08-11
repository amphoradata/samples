import * as React from "react";
import { useConfigState } from "react-amphora";
import { Redirect, Route, RouteProps } from "react-router";

export const ProtectedRoute: React.FC<RouteProps> = (props) => {
  const state = useConfigState();

  if (state.isAuthenticated) {
    return <Route {...props} />;
  } else {
    const renderComponent = () => <Redirect to={{ pathname: "/" }} />;
    return <Route {...props} component={renderComponent} render={undefined} />;
  }
};

export default ProtectedRoute;
