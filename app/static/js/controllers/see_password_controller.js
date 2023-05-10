import { Controller } from "../../node_modules/@hotwired/stimulus"

export default class extends Controller {
  static targets = ["passwordDiv", "passwordField"]

  connect() {
    this._add_icon()
  }

  _add_icon(){
    var eye_icon='<span class="fa fa-fw fa-eye field-icon" data-action="mouseover->see-password#turnOnVisibility mouseout->see-password#turnOffVisibility"></span>'

    this.passwordDivTarget.innerHTML += eye_icon;
  }

  turnOnVisibility() {
    this.passwordFieldTarget.setAttribute("type", "text")
  }

  turnOffVisibility() {
    this.passwordFieldTarget.setAttribute("type", "password")
  }

}
