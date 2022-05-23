Stimulus.register("flashing", class extends Controller {
  static targets = ["flashes"]

  connect() {}

  deleteOldMessage(){}

  getMessage() {
    fetch("{{ url_for('SupportView:flashing') }}",{
      method: 'GET',
    }).then((response) => {
      return response.json();
    }).then((response) => {
      if (response.length > 0) {
        this.flashesTarget.innerHTML += response[0]
      }
    });
  }

})
