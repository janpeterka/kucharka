import { Controller } from "../../node_modules/@hotwired/stimulus"

export default class extends Controller {
    static targets = ["editor"]

  connect() {
    if (this.hasEditorTarget) {
      $(this.editorTarget).trumbowyg();
    }
  }

}
