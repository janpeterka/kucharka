import { Controller } from "../../node_modules/@hotwired/stimulus"

export default class extends Controller {
  static targets = ["area"]

  connect() {
    for (let i = 0, item; item = this.areaTarget.querySelectorAll(".clickable")[i]; i++) {
      item.classList.add("cursor-clickable")
    }
  }

  activateLink(event) {
    if (event.target.dataset.bsToggle == "modal") { return; } // prevent this when clicking modal button

    var clickable_parent = event.target.closest(".clickable")
    var first_link = clickable_parent.getElementsByTagName("a")[0];
    first_link.click();
  }

}
