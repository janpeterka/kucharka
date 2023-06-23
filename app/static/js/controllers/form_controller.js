import { Controller } from "../../node_modules/@hotwired/stimulus"

export default class extends Controller {
  static values = { autoSubmit: { type: Boolean, default: false } }

  connect() {
    this.debounceTimeout = false;

    if (this.autoSubmitValue) {
      this.element.dataset.action = this.element.getAttribute("data-action") || "" + " change->form#submit keydown.enter->form#submit"
    }
  }

  reset() {
    this.element.reset()
    this.debounceTimeout = false
  }

  submit(e) {
    e.preventDefault();
    if (!this.debounceTimeout === true) {
      console.log("submitting form");
      this.element.requestSubmit();
      this.debounceTimeout = true;
      setTimeout(() => {
        this.debounceTimeout = false;
        console.log("debounce timeout reset")
      }, 200)
    }
  }

}
