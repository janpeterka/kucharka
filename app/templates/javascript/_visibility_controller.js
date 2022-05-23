Stimulus.register("visibility", class extends Controller {
  static targets = ["element"]

  connect() {}

  hide() {
    this.elementTarget.classList.add("d-none")
  }

})
