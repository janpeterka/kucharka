import { Controller } from "../../node_modules/@hotwired/stimulus"

export default class extends Controller {
  static targets = ["element"]

  connect() {}

  hide() {
    this.elementTarget.classList.add("d-none")
  }
}
