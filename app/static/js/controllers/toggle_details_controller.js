import { Controller } from "../../node_modules/@hotwired/stimulus"

export default class extends Controller {
  static targets = ["buttons"]

  connect() {
    this.buttonsTarget.innerHTML = '\
      <button class="btn" data-action="click->toggle-details#show_all">Zobrazit vše</button>\
      <button class="btn" data-action="click->toggle-details#hide_all">Skrýt vše</button>'
  }

  show_all() {
    this._set_value_for_details(true)
  }

  hide_all() {
    this._set_value_for_details(false)
  }

  _details(){
    return document.querySelectorAll("details");
  }

  _set_value_for_details(value){
    for (let i = 0, detail; detail = this._details()[i]; i++) {
      detail.open = value;
    }
  }

}
