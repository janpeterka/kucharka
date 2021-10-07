Stimulus.register("enable-summernote", class extends Controller {
    static get targets() {
      return ["summernote"]
    }

  connect() {
    if (this.hasSummernoteTarget) {
      $(this.summernoteTarget).summernote();
    }
  }

})
