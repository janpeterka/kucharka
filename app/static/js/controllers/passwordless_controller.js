import { Client, isPlatformSupported, isBrowserSupported } from '../../node_modules/@passwordlessdev/passwordless-client';
import { Controller } from "../../node_modules/@hotwired/stimulus"

export default class extends Controller {
  static targets = ["passwordlessButton", "normalButton" ,"username", "password"];

  connect() {
    this.client = new Client({
      apiKey: "skautskkuchaka:public:36bd9184a88e4a05a2db8af12a2f87d4"
    });

    if (isBrowserSupported() === false || isPlatformSupported() === false){
      console.log("Passwordless not supported")
      this.passwordTarget.classList.remove("d-none");
      this.normalButtonTarget.classList.remove("d-none");
    } else {
      console.log("Passwordless supported, cool!")
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

  // async signIn() {
  //   try {
  //     const alias = document.getElementById("username").innerHTML;

  //     const { token, error } = await this.client.signinWithAlias(alias);

  //     const backendUrl = "https://skautskakucharka.cz"; // Your backend.
  //     const response = await fetch(`${backendUrl}/signin?token=${token}`);
  //     const verifiedUser = await response.json();

  //     if (verifiedUser.success === true) {
  //       // If successful, proceed!
  //     }
  //   } catch (error) {
  //     console.error(error);
  //   }
  // }
}
