import { Controller } from "../../node_modules/@hotwired/stimulus"

export default class extends Controller {
  static targets = ["element"]

  hide() {
    this.elementTarget.classList.add("d-none")
  }

  showFor(seconds = 2) {
    this.elementTarget.classList.remove("d-none")
    setTimeout(() => {
      this.elementTarget.classList.add("d-none")
    }, seconds * 1000)
  }
}
