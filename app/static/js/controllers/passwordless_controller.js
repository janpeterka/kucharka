import { Client, isPlatformSupported, isBrowserSupported } from '../../node_modules/@passwordlessdev/passwordless-client';
import { Controller } from "../../node_modules/@hotwired/stimulus"

export default class extends Controller {
  static targets = ["passwordlessButton", "normalButton" ,"username", "password"];

  async connect() {
    this.client = new Client({
      apiKey: "skautskkuchaka:public:36bd9184a88e4a05a2db8af12a2f87d4"
    });

    if (isBrowserSupported() === true){
      if (await isPlatformSupported() === true){
        console.log("Passwordless supported, cool!")
        this.passwordTarget.classList.add("d-none");
        this.normalButtonTarget.classList.add("d-none");
        this.passwordlessButtonTarget.classList.remove("d-none");
      } else {
        console.log("Passwordless (platform) not supported, that's sad :(")
        this.passwordlessButtonTarget.disabled = true;
      }
    } else {
      console.log("Passwordless (browser) not supported, that's sad :(")
      this.passwordlessButtonTarget.disabled = true;
    }
  }

  async registerUser(e) {
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

  async signIn() {
    try {
      const alias = this.usernameTarget.innerHTML;

      const { token, error } = await this.client.signinWithAlias(alias);

      const response = await fetch(`https://skautskakucharka.cz/signin?token=${token}`);
      const verifiedUser = await response.json();

      this.passwordlessButtonTarget.innerHTML = verifiedUser

      if (verifiedUser.success === true) {

        // If successful, proceed!
        console.log("Successfully signed in user")
      }
    } catch (error) {
      console.error(error);
    }
  }
}
