Stimulus.register("clicker", class extends Controller {
    static get targets() {
      return ["area"]
    }

  connect() {
    for (let i = 0, item; item = this.areaTarget.querySelectorAll(".clickable")[i]; i++) {
      item.classList.add("cursor-clickable")
    }
  }

  activateLink(event) {
    var clickable_parent = event.target.closest(".clickable")
    var first_link = clickable_parent.getElementsByTagName("a")[0];
    first_link.click();
  }

})
