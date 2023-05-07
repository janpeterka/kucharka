import { Controller } from "../../node_modules/@hotwired/stimulus"
import select2 from '../../node_modules/select2';
window.select2 = select2();

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
