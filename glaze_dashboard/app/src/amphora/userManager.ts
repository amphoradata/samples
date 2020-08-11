import { createUserManager } from "react-amphora";

let redirectUri = `${window.location.href}/#/callback`;

const userManager = createUserManager({
  clientId: "f48fed4f-569e-4524-8432-b5ae4444eca4", // replace this with your ID
  redirectUri,
});

export { userManager };
