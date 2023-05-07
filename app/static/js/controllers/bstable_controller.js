import { Controller } from "../../node_modules/@hotwired/stimulus"

export default class extends Controller {
  static targets = ["table"]

  connect() {
    if (this.hasTableTarget) {
      $(this.tableTarget).bootstrapTable();
    }
  }

  _is_activated() {
  	return document.querySelectorAll("div.bootstrap-table").length > 0
  }

}
