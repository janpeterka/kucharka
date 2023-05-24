import { Controller } from "../../node_modules/@hotwired/stimulus"

export default class extends Controller {

  reset() {
    this.element.reset()
  }

  submit() {
    this.element.requestSubmit()
  }

}
