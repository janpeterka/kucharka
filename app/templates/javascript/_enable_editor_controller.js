Stimulus.register("enable-editor", class extends Controller {
    static get targets() {
      return ["editor"]
    }

  connect() {
    if (this.hasEditorTarget) {
      $(this.editorTarget).trumbowyg();
    }
  }

})
