Stimulus.register("bstable", class extends Controller {
    static get targets() {
      return ["table"]
    }

  connect() {
    if (this.hasTableTarget) {
      $(this.tableTarget).bootstrapTable();
    }
  }

  disconnect() {
  	
  }

  _is_activated() {
  	return document.querySelectorAll("div.bootstrap-table").length > 0
  }

  // disconnect() {
  //   if (this.hasTableTarget) {
  //     $(this.tableTarget).bootstrapTable();
  //   }  	
  // }

})
