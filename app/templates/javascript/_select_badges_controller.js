Stimulus.register("select-badges", class extends Controller {
    static targets = ["select", "badges"]
    static classes = ["selected", "unselected"]

  connect() {
    this.add_badges();
    this.hide_select();
  }

  hide_select(){
    this.selectTarget.style.display = "none";
  }

  add_badges(){
    for (let i = 0, option; option = this.selectTarget.options[i]; i++) {
      if (option.value > 0) {
        this.add_badge(option)
      }
    }
  }

  add_badge(option){
    var badge = document.createElement("span")
    badge.className = "select-badge btn ms-1 me-1 bg-color-grey"
    badge.dataset.label = option.label
    badge.dataset.selectBadgesValueParam = option.value
    badge.id = `badge-${option.value}`
    badge.dataset.action = "click->select-badges#select"
    badge.innerHTML = option.label

    if (option.selected === true) {
      this.set_selected_badge(badge)
    }

    this.badgesTarget.appendChild(badge)
  }

  select(event){
    this.set_select_value(event.params.value)
  }

  set_select_value(value){
    if (this.selectTarget.value == value) {
      this.unset_all_badges()
      this.selectTarget.value = "__None";
    } else {
    this.selectTarget.value = value;

    this.unset_all_badges()

    var badge = document.getElementById(`badge-${value}`)
    this.set_selected_badge(badge)
    }
  }

  set_selected_badge(badge){
    badge.dataset.selected = true
    badge.classList.remove(this.unselectedClass)
    badge.classList.add(this.selectedClass)
  }

  unset_all_badges(){
    var badges = document.getElementsByClassName("select-badge")
    for (let i = 0, badge; badge = badges[i]; i++) {
      badge.classList.remove(this.selectedClass)
      badge.classList.add(this.unselectedClass)
      badge.dataset.selected = false
    }
  }
})