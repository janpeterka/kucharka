import { Client, isPlatformSupported, isBrowserSupported, isAutofillSupported } from '../../node_modules/@passwordlessdev/passwordless-client';
import { Controller } from "../../node_modules/@hotwired/stimulus"

export default class extends Controller {
  static targets = ["passwordlessButton", "normalButton" ,"username", "password", "debug"];
  static values = {
    isPlatformSupported: Boolean,
    isBrowserSupported: Boolean,
    isAutofillSupported: Boolean
  }

  async connect() {
    this.client = new Client({
      apiKey: "skautskkuchaka:public:36bd9184a88e4a05a2db8af12a2f87d4"
    });

    this.isPlatformSupportedValue = await isPlatformSupported();
    this.isBrowserSupportedValue = isBrowserSupported();
    this.isAutofillSupportedValue = await isAutofillSupported();
  }

  debugTargetConnected() {
    this.debugTarget.innerHTML = `plaftorm: ${this.isPlatformSupportedValue}, browser: ${this.isBrowserSupportedValue}, autofill: ${this.isAutofillSupportedValue}`
  }

  async registerUser(e){
    e.preventDefault();
    try {
      const registerToken = await fetch(`/passwordless/register-user?username=${this.usernameTarget.value}`, {method: "POST"}).then(r => r.json());

      if (registerToken.error) {
        console.log("Error registering user from BE")
        window.location.reload();
      } else {
        const { token, error } = await this.client.register(registerToken.token);

        if (token) {
          console.log("Successfully registered user")
          window.location.href = "/"
          // Successfully registered!
        } else {
          console.log("Error registering user")
          console.error(error);
        }
      }

    } catch (error) {
      console.log("Error in flow")
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
        console.log("Error registering user")
        console.error(error);
        window.location.reload();
      }
    } catch (error) {
      console.log("Error in flow")
      console.error(error);
    }
  }

  async signIn(e) {
    e.preventDefault();

    try {
      const { token, error } = await this.client.signinWithDiscoverable();

      const response = await fetch(`/passwordless/signin?token=${token}`, {method: "POST"});
      if (response.redirected){
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
}
