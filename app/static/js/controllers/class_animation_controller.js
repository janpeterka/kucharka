import { Controller } from "../../node_modules/@hotwired/stimulus"

export default class extends Controller {
    static classes = ["added"]
    static values = { timeout: { type: Number, default: 3000 } }

    connect() {
        this.element.classList.add(this.addedClass)

        setTimeout(() => {
            this.element.classList.remove(this.addedClass)
        }, this.timeoutValue)
    }
}
