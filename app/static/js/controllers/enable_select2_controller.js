import { Controller } from "../../node_modules/@hotwired/stimulus"

export default class extends Controller {
  static targets = ["select"]

  connect() {
    if (this.hasSelectTarget) {
      $(this.selectTarget).select2(
        {theme: 'bootstrap-5'}
      );
    }

  }

}
