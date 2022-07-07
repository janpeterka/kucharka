Stimulus.register("select-badges", class extends Controller {
    static targets = ["select", "badges"]
    static classes = ["selected", "unselected"]
    static values = {
      type: { type: String, default: 'single' }
    }

  connect(){
    this.add_badges();
    this.hide_select();
  }

  hide_select(){
    this.selectTarget.style.display = "none";
  }

  add_badges(){
    for (let i = 0, option; option = this.selectTarget.options[i]; i++) {
      // this prevents adding None - empty option from allow_blank
      if (option.value != "__None" && option.value != "0") {
        this.add_badge(option)
      }
    }
  }

  add_badge(option){
    if (this.element.querySelector(`#badge-${option.value}`)) {
      return;
    }

    var badge = document.createElement("span")
    badge.className = "select-badge lh-3 ms-1 me-1 p-2 cursor-clickable rounded-pill text-nobreak"
    
    if (option.dataset.color == "None" || option.dataset.color == null || option.dataset.color.length === 0) {
      badge.dataset.color = this.selectedClass.replace("bg-color-", "")
    } else {
      badge.dataset.color = option.dataset.color
    }

    badge.dataset.colorClass = "bg-color-" + badge.dataset.color
    badge.className = badge.className + " bg-color-" + badge.dataset.color
    badge.dataset.label = option.label
    badge.dataset.selected = false
    badge.dataset.selectBadgesValueParam = option.value
    badge.id = `badge-${option.value}`
    badge.dataset.action = "click->select-badges#toggle"
    badge.innerHTML = option.label

    if (option.selected === true) {
      this.select_badge(badge)
    } else {
      this.unselect_badge(badge)
    }

    this.badgesTarget.appendChild(badge)
  }

  toggle(event){
    var value = event.params.value
    var badge = this.element.querySelector(`#badge-${value}`)
    if (badge.dataset.selected == "true") {
      this.unselect_value(value)
    } else {
      this.select_value(value);
    }
  }


  unselect_value(value){
    var badge = this.element.querySelector(`#badge-${value}`)

    if (this.typeValue == "single") {
      this.unselect_all_badges()
      this.selectTarget.value = "__None";
    } else {
      this.unselect_badge(badge)
      this.remove_option(value)
    }
  }

  select_value(value){
    var badge = this.element.querySelector(`#badge-${value}`)

    if (this.typeValue == "single") {
        this.unselect_all_badges()
        this.selectTarget.value = value;
        this.select_badge(badge)
    } else {
        this.add_option(value)
        this.select_badge(badge)
    }
  }

  add_option(value){
    var current_values = $(this.selectTarget).val()
    current_values.push(value.toString())
    
    $(this.selectTarget).val(current_values)
  }

  remove_option(value){
    var current_values = $(this.selectTarget).val()
    current_values = this._removeItem(current_values, value.toString())

    $(this.selectTarget).val(current_values)
  }

  select_badge(badge){
    badge.dataset.selected = true
    badge.classList.remove(this.unselectedClass)
    badge.classList.add(badge.dataset.colorClass)
  }

  unselect_badge(badge){
    badge.dataset.selected = false
    badge.classList.add(this.unselectedClass)
    badge.classList.remove(badge.dataset.colorClass)
  }

  unselect_all_badges(){
    var badges = this.badgesTarget.querySelectorAll(".select-badge")

    for (let i = 0, badge; badge = badges[i]; i++) {
      this.unselect_badge(badge)
    }
  }

  _removeItem(arr, value) {
    var index = arr.indexOf(value);
    if (index > -1) {
      arr.splice(index, 1);
    }
    return arr;
  }
})