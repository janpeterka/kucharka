Stimulus.register("enable-select2", class extends Controller {
    static get targets() {
      return ["select"]
    }

  connect() {
    if (this.hasSelectTarget) {
      $(this.selectTarget).select2(
        {theme: 'bootstrap-5'}
      );
    }

  }
})
