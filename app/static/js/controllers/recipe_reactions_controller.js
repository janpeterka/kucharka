import { Controller } from "../../node_modules/@hotwired/stimulus"

export default class extends Controller {
    static targets = ["recipe"]

    connect() {
    }

    empty(event) {
        event.target.classList.remove('fas')
        event.target.classList.add('far')
        event.target.dataset.action = "click->recipe-reactions#fill"
    }

    fill(event) {
        event.target.classList.remove('far')
        event.target.classList.add('fas')
        event.target.dataset.action = "click->recipe-reactions#empty"
    }
};
