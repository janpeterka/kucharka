Stimulus.register("clicker", class extends Controller {
    static get targets() {
      return ["area"]
    }

  connect() {
    for (let i = 0, badge; badge = this.areaTarget.querySelectorAll(".day-badge")[i]; i++) {
      // if (badge.value > 0) {
        badge.classList.add("cursor-clickable")
      // }
    }
  }

  activateLink(event) {
    var first_child_link = event.target.getElementsByTagName("a")[0];
    first_child_link.click();
    // console.log(event.target.getElementsByTagName("a")[0])
  }

})
