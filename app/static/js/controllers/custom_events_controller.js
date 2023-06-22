import { Controller } from "../../node_modules/@hotwired/stimulus"

export default class extends Controller {
  static values = { "event": String }

  dispatch() {
    const event = new CustomEvent(this.eventValue)
    window.dispatchEvent(event)
  }

}
