Stimulus.register("select-badges", class extends Controller {
    static targets = ["select", "badges"]
    static classes = ["selected", "unselected"]
    static values = {
      type: { type: String, default: 'single' }
    }

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
    badge.dataset.selected = false
    badge.dataset.selectBadgesValueParam = option.value
    badge.id = `badge-${option.value}`
    badge.dataset.action = "click->select-badges#toggle"
    badge.innerHTML = option.label

    if (option.selected === true) {
      this.select_badge(badge)
    }

    this.badgesTarget.appendChild(badge)
  }

  toggle(event){
    var value = event.params.value
    var badge = document.getElementById(`badge-${value}`)
    if (badge.dataset.selected == "true") {
      this.unselect_value(value)
    } else {
      this.select_value(value);
    }
  }


  unselect_value(value){
    var badge = document.getElementById(`badge-${value}`)

    if (this.typeValue == "single") {
      this.unselect_all_badges()  
      this.selectTarget.value = "__None";
    } else {
      this.unselect_badge(badge)
      this.remove_option(value)
    }
  }

  select_value(value){
    var badge = document.getElementById(`badge-${value}`)

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
    badge.classList.add(this.selectedClass)
  }

  unselect_badge(badge){
    badge.dataset.selected = false
    badge.classList.add(this.unselectedClass)
    badge.classList.remove(this.selectedClass)
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