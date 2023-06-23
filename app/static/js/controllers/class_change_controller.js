import { Controller } from "../../node_modules/@hotwired/stimulus"

export default class extends Controller {
  static classes = ["added", "removed"]
  static values = { timeout: { type: Number, default: 2000 } }

  connect() {
    if (this.hasAddedClass) {
      this.addBriefly()
    }

    if (this.hasRemovedClass) {
      this.removeBriefly()
    }
  }

  addBriefly() {
    this.element.classList.add(this.addedClass)
    setTimeout(() => {
      this.element.classList.remove(this.addedClass)
    }, this.timeoutValue)
  }

  removeBriefly() {
    this.element.classList.remove(this.removedClass)
    setTimeout(() => {
      this.element.classList.add(this.removedClass)
    }, this.timeoutValue)
  }
}
