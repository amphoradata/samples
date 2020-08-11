# Glaze Tutorial: Sample Dashboard

In this tutorial, we're going to build a data driven dashboard, fron scratch, using [Amphora Glaze](https://www.amphoradata.com/glaze/).

> This tutorial requires a subscription to Amphora `Glaze`.

> If you aren't registed, head to [the app](https://app.amphoradata.com/) to register.

## Clone this Repository

To begin, clone this repo, and open this directory:

```sh
git clone https://github.com/amphoradata/samples.git
cd samples/glaze_dashboard
```

## Create an Amphora Application

Amphora Applications allow you to connect external apps to Amphora Data services. It enables OAuth logins to your app with the Amphora Identity system, and it allows the Amphora backend to response (via CORS) to requests from the app.

### Creating the application

We are going to need the Amphora Data python SDK installed.

#### Install the Python SDK

In a terminal:

```sh
cd python
pip install -r requirements.txt
```

#### Run the create-application.py script

[This helpful script](python/scripts/create-application.py) enables you to create a new Amphora application.

```sh
> python create-application.py

Enter your Amphora username:rian@amphoradata.com
Password:
https://app.amphoradata.com
Enter a name for your app (default: my_app):sample_glaze_dashboard
Enter a logout callback URL (default: http://localhost:3000/logout):
Enter the deployed URL for your app (default: http://localhost:3000):
Enter an allowed redirect path (default: /#/callback):
You are about to register an app named sample_glaze_dashboard. Press any key to continue, or ctrl+c to cancel...
Your Application ID is f48fed4f-569e-4524-8432-b5ae4444eca4   # <-- copy this id
```

## Creating a react app

For this dashboard, we're going to use [react-amphora](https://github.com/xtellurian/react-amphora), a frontend react library that removes a lot of boilerplate code.

> You can see the final version of the app in `/app`

### Create an app with create-react-app

We're going to make a new typescript-based react app.

```sh
cd samples/glaze_dashboard
yarn create react-app app --template typescript
```

### Install react-amphora

`react-amphora` is an open source front-end react component library for building Amphora data driven apps. Install it like so:

```sh
cd app
yarn add react-amphora
```

#### Create a user manager

Amphora used OIDC and OAuth to authenticate users in client applications. We need to setup our user manager (from [oidc-client-js](https://github.com/IdentityModel/oidc-client-js)). Once done, it allows _any_ Amphora user to sign into our app!

[amphora/userManager.ts](app/src/amphora/userManager.ts)

```ts
import { createUserManager } from "react-amphora";

let redirectUri = `${window.location.href}/#/callback`; // this matched the callback path we defined above.
const userManager = createUserManager({
  clientId: "f48fed4f-569e-4524-8432-b5ae4444eca4", // replace this with your ID
  redirectUri,
});

export { userManager };
```

#### Create an Amphora Configuration

This enables some customisation of the Amphora API client, but we're just going to use defaults.

[amphora/configuration.ts](app/src/amphora/configuration.ts)

```ts
import { Configuration } from "amphoradata";
export const initalConfiguration = new Configuration();
```

### Setup the react-amphora provider

To use `react-amphora`, you wrap a react component in an `<AmphoraProvider>` component, like so:

[index.tsx](app/src/index.tsx)

```tsx
import { AmphoraProvider } from "react-amphora";
import { userManager } from "./amphora/userManager";
import { initalConfiguration } from "./amphora/configuration";

ReactDOM.render(
  <React.StrictMode>
    <AmphoraProvider
      userManager={userManager}
      configuration={initalConfiguration}
    >
      <App />
    </AmphoraProvider>
  </React.StrictMode>,
  document.getElementById("root")
);
```

Now, if you run the app (with `yarn start`), and navigate in your browser to [localhost:3000](http://localhost:3000), you'll should see the normal `create-react-app` bootstrap screen.

Now, we're going to add the sign in callback page, a sign in button, and a user information page.

### Add react-router and a authentication callback route

#### Install react-router

```
yarn add react-router-dom
yarn add -D @types/react-router-dom
```

#### Setup the router and auth callback

Wrap your application component in the BrowserRouter component, then 

[App.tsx](app/src/App.tsx)

```tsx
import {
  BrowserRouter as Router,
  RouteComponentProps,
  withRouter,
} from "react-router-dom";
import { userManager } from "./amphora/userManager";
import { CallbackPage } from "react-amphora";

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
```

#### Add a Sign In button component

The sign in button is a simple component that prompts the user to sign-in with Amphora.

```tsx
import { SignInButton } from "react-amphora";
...

<SignInButton alwaysOn={true} />
```

The Sign In Button, by default, will not render in the DOM if the user is already authenticated. You can override this behaviour using the `alwaysOn` prop.

#### Add a user information panel component

The user information component displays some information about the user, derived from the OIDC identity.

```tsx
import { UserInformationComponent } from "react-amphora";

<UserInformationComponent />
```

### You did it!

Your app is now connected to Amphora! Once you login, you app should look like this:

![](assets/app_1.gif)

