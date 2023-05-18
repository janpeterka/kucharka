import { Client, isPlatformSupported, isBrowserSupported, isAutofillSupported } from '../../node_modules/@passwordlessdev/passwordless-client';
import { Controller } from "../../node_modules/@hotwired/stimulus"

export default class extends Controller {
  static targets = ["passwordlessButton", "normalButton" ,"username", "password"];

  async connect() {
    this.client = new Client({
      apiKey: "skautskkuchaka:public:36bd9184a88e4a05a2db8af12a2f87d4"
    });

    // if (await isPlatformSupported() === false){
      // this.element.classList.add("d-none");
    // }

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
      }
    } catch (error) {
      console.log("Error in flow")
      console.error(error);
    }
  }

  async signIn(e) {
    e.preventDefault();

    try {
      // const { token, error } = await this.client.signinWithDiscoverable();

      let token = "debug"

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
        }
      }
    } catch (error) {
      console.error(error);
    }
  }
}
