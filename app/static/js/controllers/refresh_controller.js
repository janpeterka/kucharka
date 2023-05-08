import { Controller } from "../../node_modules/@hotwired/stimulus"

export default class extends Controller {
  refresh(event) {
  	window.location.reload();
  }

}
