import { Client, isPlatformSupported, isBrowserSupported, isAutofillSupported } from '../../node_modules/@passwordlessdev/passwordless-client';
import { Controller } from "../../node_modules/@hotwired/stimulus"

export default class extends Controller {
  static targets = ["passwordlessButton", "normalButton", "username", "password", "debug"];

  async connect() {
    this.client = new Client({
      apiKey: "skautskkuchaka:public:36bd9184a88e4a05a2db8af12a2f87d4"
    });
  }

  async debugTargetConnected() {
    this.debugTarget.innerHTML = `plaftorm: ${await isPlatformSupported()}, browser: ${isBrowserSupported()}, autofill: ${await isAutofillSupported()}`
  }

  async registerUser(e) {
    e.preventDefault();

    try {
      let response = await fetch(`/passwordless/register-user?username=${this.usernameTarget.value}`, { method: "POST" });

      if (response.redirected) {
        // this happens when user is already registered
        window.location.href = response.url;
        return;
      } else if (response.error) {
        console.log("Error registering user from BE")
        window.location.reload();
        return;
      }

      response = await response.json();

      const { token, error } = await this.client.register(response.token);

      if (token) {
        console.log("Successfully registered user")
        window.location.href = "/"
          // Successfully registered!
      } else {
        console.log("Error registering user")
        console.error(error);
      }

    } catch (error) {
      console.log("Error in flow")
      console.error(error);
    }
  }

  async signIn(e) {
    // if (await isPlatformSupported() === false || await isAutofillSupported() === false) {
    //   console.log("not supported")
    //   return;
    // }

    try {
      const promise = this.client.signinWithAutofill();

      const { token, error } = await promise
      if (!token) {
        return;
      }

      const response = await fetch(`/passwordless/signin?token=${token}`, { method: "POST" });
      if (response.redirected) {
        window.location.href = response.url;
      } else {
        const verifiedUser = await response.json();

        if (verifiedUser.success === true) {

          // If successful, proceed!
          console.log(verifiedUser)
          console.log(`Successfully signed in user`)
        } else {
          console.log("Oh no, something went wrong!")
          window.location.reload();
        }
      }
    } catch (error) {
      console.error(error);
    }
  }

  async linkToken(e) {
    // do this after you get token on BE
    e.preventDefault();

    try {
      const registerToken = await fetch("/passwordless/register-token").then(r => r.json());

      const { token, error } = await this.client.register(registerToken.token);

      if (token) {
        console.log("Successfully registered user")
          // Successfully registered!
      } else {
        console.log("Error linking token")
        console.error(error);
        window.location.reload();
      }
    } catch (error) {
      console.log("Error in flow")
      console.error(error);
    }
  }

}
